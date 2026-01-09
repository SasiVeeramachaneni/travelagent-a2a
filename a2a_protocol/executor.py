"""
Travel Agent Executor for A2A Protocol
Handles incoming A2A requests and processes them using the Travel Agent
"""
import asyncio
import uuid
from typing import Any

from a2a.server.agent_execution.agent_executor import AgentExecutor
from a2a.server.agent_execution.context import RequestContext
from a2a.server.events.event_queue import EventQueue
from a2a.server.tasks.task_updater import TaskUpdater
from a2a.utils.message import new_agent_text_message
from a2a.types import (
    Part,
    TextPart,
    TaskState,
    TaskStatus,
    Message,
    Role,
)

# Import our travel agent
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agent.travel_agent import TravelAgent


class TravelAgentExecutor(AgentExecutor):
    """
    A2A Agent Executor that wraps the Travel Agent
    
    This class implements the A2A AgentExecutor interface, allowing other agents
    to interact with our Travel Agent via the A2A protocol.
    """
    
    def __init__(self):
        """Initialize the executor with a Travel Agent instance"""
        self.travel_agent = TravelAgent()
        # Dictionary to store conversation contexts by context_id
        self._contexts: dict[str, dict] = {}
    
    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue
    ) -> None:
        """
        Execute a request from another agent
        
        This method is called when an A2A request comes in. It processes
        the request using the Travel Agent and sends back the response.
        
        Args:
            context: The request context containing the message and metadata
            event_queue: Queue for sending events/responses back
        """
        # Create a task updater for sending status updates
        task_updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        
        # Get or create conversation context for this context_id
        conversation_context = self._get_or_create_context(context.context_id)
        
        try:
            # Update status to working
            await task_updater.update_status(
                TaskState.working,
                message=new_agent_text_message("Processing your travel request...")
            )
            
            # Extract the user's message text from the request
            user_message = self._extract_message_text(context.message)
            
            if not user_message:
                # No valid message received
                await task_updater.update_status(
                    TaskState.completed,
                    message=new_agent_text_message(
                        "I didn't receive a message. Please send your travel question or request."
                    )
                )
                return
            
            # Process the message using Travel Agent
            # Run in thread pool since travel_agent methods are synchronous
            response = await asyncio.get_event_loop().run_in_executor(
                None,
                self._process_message,
                user_message,
                conversation_context
            )
            
            # Send the response back
            await task_updater.update_status(
                TaskState.completed,
                message=new_agent_text_message(response)
            )
            
        except Exception as e:
            # Handle errors gracefully
            error_message = f"I encountered an error processing your request: {str(e)}"
            await task_updater.update_status(
                TaskState.failed,
                message=new_agent_text_message(error_message)
            )
    
    async def cancel(self, context: RequestContext, event_queue: EventQueue) -> None:
        """
        Handle cancellation of a request
        
        Args:
            context: The request context
            event_queue: Event queue for sending cancellation confirmation
        """
        from a2a.server.tasks import TaskUpdater
        task_updater = TaskUpdater(event_queue, context.task_id, context.context_id)
        
        await task_updater.update_status(
            TaskState.canceled,
            message=new_agent_text_message("Request cancelled.")
        )
    
    def _extract_message_text(self, message: Message) -> str:
        """
        Extract text content from an A2A Message
        
        Args:
            message: The A2A Message object
            
        Returns:
            str: The extracted text content
        """
        if not message or not message.parts:
            return ""
        
        text_parts = []
        for part in message.parts:
            # Handle Part which contains root (TextPart, DataPart, or FilePart)
            if hasattr(part, 'root') and part.root:
                root = part.root
                if hasattr(root, 'text'):
                    text_parts.append(root.text)
            elif hasattr(part, 'text'):
                text_parts.append(part.text)
        
        return " ".join(text_parts).strip()
    
    def _get_or_create_context(self, context_id: str | None) -> dict:
        """
        Get or create a conversation context for a given context_id
        
        This allows maintaining conversation state across multiple A2A requests
        
        Args:
            context_id: The A2A context ID
            
        Returns:
            dict: The conversation context
        """
        if not context_id:
            context_id = str(uuid.uuid4())
        
        if context_id not in self._contexts:
            self._contexts[context_id] = {
                "context_id": context_id,
                "history": [],
                "user_context": {}
            }
        
        return self._contexts[context_id]
    
    def _process_message(self, user_message: str, conversation_context: dict) -> str:
        """
        Process a message using the Travel Agent
        
        This is a synchronous method that wraps the Travel Agent's process_message
        
        Args:
            user_message: The user's message
            conversation_context: The conversation context
            
        Returns:
            str: The agent's response
        """
        # Store the message in history
        conversation_context["history"].append({
            "role": "user",
            "content": user_message
        })
        
        # Update travel agent's context if we have stored context
        if conversation_context.get("user_context"):
            self.travel_agent.user_context.update(conversation_context["user_context"])
        
        # Process the message
        response = self.travel_agent.process_message(user_message)
        
        # Save the updated context
        conversation_context["user_context"] = self.travel_agent.user_context.copy()
        
        # Store response in history
        conversation_context["history"].append({
            "role": "agent",
            "content": response
        })
        
        return response
    
    def clear_context(self, context_id: str) -> None:
        """
        Clear a conversation context
        
        Args:
            context_id: The context ID to clear
        """
        if context_id in self._contexts:
            del self._contexts[context_id]
        self.travel_agent.reset_conversation()


# Convenience function to create an executor instance
def create_executor() -> TravelAgentExecutor:
    """Create a new TravelAgentExecutor instance"""
    return TravelAgentExecutor()
