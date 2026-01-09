"""
A2A (Agent-to-Agent) Protocol Implementation
Enables other agents to interact with the Travel Agent via A2A protocol
"""
from .agent_card import create_agent_card
from .executor import TravelAgentExecutor

__all__ = ['create_agent_card', 'TravelAgentExecutor']
