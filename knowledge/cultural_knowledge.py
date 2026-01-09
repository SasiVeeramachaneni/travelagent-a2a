"""
Cultural Knowledge
Contains local customs, etiquette, language basics, and cultural tips
"""
from typing import Dict, List, Optional, Any


class CulturalKnowledge:
    """
    Knowledge base for cultural information and etiquette
    
    This module provides:
    - Local customs and etiquette
    - Basic phrases in local language
    - Tipping customs
    - Dress codes
    - Cultural do's and don'ts
    """
    
    def __init__(self):
        """Initialize cultural knowledge base"""
        self.cultural_data = self._load_cultural_data()
        self.phrases = self._load_basic_phrases()
    
    def _load_cultural_data(self) -> Dict[str, Any]:
        """
        Load cultural information database
        
        Structure:
        {
            'destination': {
                'greetings': {...},
                'etiquette': {...},
                'tipping': {...},
                'dress_code': {...},
                'dos': [...],
                'donts': [...]
            }
        }
        """
        return {
            'france': {
                'greetings': {
                    'style': 'Formal and polite',
                    'handshake': 'Light handshake, direct eye contact',
                    'kiss': 'La bise (cheek kiss) among friends - usually 2 kisses',
                    'address': 'Use Monsieur/Madame until invited to use first name'
                },
                'etiquette': {
                    'dining': [
                        'Keep hands on table (not lap) while eating',
                        'Wait for host to start eating',
                        'Bread on table, not on plate',
                        'Finish everything on your plate',
                        'Say "Bon appétit" before eating'
                    ],
                    'public': [
                        'Speak quietly in public spaces',
                        'Always say "Bonjour" when entering shops',
                        'Dress neatly - French value appearance',
                        'Queue orderly, no cutting in line'
                    ]
                },
                'tipping': {
                    'restaurants': '5-10% (service included, but rounding up appreciated)',
                    'cafes': 'Round up or leave small change',
                    'taxis': 'Round up to nearest euro',
                    'hotels': '1-2 euros per bag for porter'
                },
                'dress_code': {
                    'general': 'Smart casual, avoid athletic wear in city',
                    'religious_sites': 'Modest clothing, cover shoulders',
                    'upscale': 'Jacket for men, no sneakers'
                },
                'dos': [
                    'Learn basic French phrases',
                    'Greet shopkeepers when entering',
                    'Try to speak French first',
                    'Be punctual for appointments',
                    'Enjoy meals slowly - dining is social'
                ],
                'donts': [
                    'Don\'t ask for ketchup in restaurants',
                    'Don\'t eat on the go',
                    'Don\'t speak loudly in public',
                    'Don\'t discuss money openly',
                    'Don\'t expect warm service - it\'s not rudeness'
                ]
            },
            'japan': {
                'greetings': {
                    'style': 'Formal and respectful',
                    'bow': 'Slight bow when greeting (15-30 degrees)',
                    'handshake': 'Light handshake acceptable with foreigners',
                    'address': 'Use last name + -san (e.g., Tanaka-san)'
                },
                'etiquette': {
                    'dining': [
                        'Say "Itadakimasu" before eating',
                        'Say "Gochisousama" after finishing',
                        'Slurp noodles (shows appreciation)',
                        'Don\'t stick chopsticks upright in rice',
                        'Don\'t pass food chopstick to chopstick'
                    ],
                    'public': [
                        'Remove shoes when entering homes/some restaurants',
                        'Be very quiet on trains',
                        'Don\'t eat or drink while walking',
                        'Stand on left of escalators (right in Osaka)',
                        'No phone calls on trains'
                    ]
                },
                'tipping': {
                    'restaurants': 'No tipping - considered rude',
                    'taxis': 'No tipping',
                    'hotels': 'No tipping, but gift envelope acceptable',
                    'general': 'Tipping not part of culture'
                },
                'dress_code': {
                    'general': 'Clean, modest, conservative',
                    'temples': 'Remove shoes, modest clothing',
                    'onsen': 'Completely nude, wash before entering'
                },
                'dos': [
                    'Bow slightly when greeting or thanking',
                    'Remove shoes when indicated',
                    'Be extremely punctual',
                    'Carry cash (many places don\'t take cards)',
                    'Learn basic phrases in Japanese',
                    'Be quiet and respectful in public'
                ],
                'donts': [
                    'Don\'t tip',
                    'Don\'t blow your nose in public',
                    'Don\'t talk on phone in trains',
                    'Don\'t walk and eat',
                    'Don\'t pour your own drink (pour for others)',
                    'Don\'t enter tattoo-friendly onsen with visible tattoos'
                ]
            },
            'usa': {
                'greetings': {
                    'style': 'Friendly and informal',
                    'handshake': 'Firm handshake, direct eye contact',
                    'personal_space': 'Arm\'s length distance',
                    'address': 'First names used quickly'
                },
                'etiquette': {
                    'dining': [
                        'Wait to be seated at restaurants',
                        'Elbows off table while eating',
                        'Tipping is mandatory',
                        'Split checks common and acceptable'
                    ],
                    'public': [
                        'Queue orderly',
                        'Small talk with strangers is normal',
                        'Smile and say "hi" to strangers',
                        'Personal space important'
                    ]
                },
                'tipping': {
                    'restaurants': '15-20% of bill (mandatory)',
                    'bars': '$1-2 per drink',
                    'taxis': '15-20%',
                    'hotels': '$2-5 per bag for porter, $2-5 per day for housekeeping'
                },
                'dress_code': {
                    'general': 'Casual, comfortable',
                    'business': 'Business casual or formal',
                    'upscale_dining': 'Smart casual, check dress code'
                },
                'dos': [
                    'Tip service workers',
                    'Be friendly and make small talk',
                    'Respect personal space',
                    'Stand right on escalators',
                    'Ask for help - Americans are generally helpful'
                ],
                'donts': [
                    'Don\'t skip tipping',
                    'Don\'t discuss politics or religion casually',
                    'Don\'t assume free healthcare',
                    'Don\'t underestimate distances',
                    'Don\'t jaywalk in front of police'
                ]
            },
            'uk': {
                'greetings': {
                    'style': 'Polite but reserved',
                    'handshake': 'Brief handshake',
                    'kiss': 'Not common except among close friends',
                    'address': 'Formal until invited otherwise'
                },
                'etiquette': {
                    'dining': [
                        'Keep elbows off table',
                        'Utensils: fork in left, knife in right',
                        'Tea etiquette important',
                        'Say "Cheers" when toasting'
                    ],
                    'public': [
                        'Queue orderly - very important!',
                        'Stand on right on escalators',
                        'Say "sorry" frequently',
                        'Respect personal space'
                    ]
                },
                'tipping': {
                    'restaurants': '10-15% if service not included',
                    'pubs': 'Not expected at bar, maybe for table service',
                    'taxis': '10-15% or round up',
                    'hotels': '£1-2 per bag'
                },
                'dress_code': {
                    'general': 'Smart casual',
                    'pubs': 'Very casual acceptable',
                    'upscale': 'Jacket and tie for fine dining'
                },
                'dos': [
                    'Queue properly - very important',
                    'Say "please" and "thank you" often',
                    'Apologize even when not at fault',
                    'Stand on right of escalators',
                    'Respect the queue'
                ],
                'donts': [
                    'Don\'t jump the queue - cardinal sin',
                    'Don\'t criticize the Royal Family',
                    'Don\'t be loud in public',
                    'Don\'t ask overly personal questions',
                    'Don\'t confuse England with UK'
                ]
            }
        }
    
    def _load_basic_phrases(self) -> Dict[str, Dict[str, str]]:
        """Load basic phrases in local languages"""
        return {
            'france': {
                'hello': 'Bonjour',
                'goodbye': 'Au revoir',
                'please': 'S\'il vous plaît',
                'thank_you': 'Merci',
                'yes': 'Oui',
                'no': 'Non',
                'excuse_me': 'Excusez-moi',
                'sorry': 'Pardon',
                'help': 'Aidez-moi',
                'bathroom': 'Où sont les toilettes?',
                'english': 'Parlez-vous anglais?',
                'bill': 'L\'addition, s\'il vous plaît'
            },
            'japan': {
                'hello': 'Konnichiwa (こんにちは)',
                'goodbye': 'Sayonara (さようなら)',
                'please': 'Onegaishimasu (お願いします)',
                'thank_you': 'Arigatou gozaimasu (ありがとうございます)',
                'yes': 'Hai (はい)',
                'no': 'Iie (いいえ)',
                'excuse_me': 'Sumimasen (すみません)',
                'sorry': 'Gomen nasai (ごめんなさい)',
                'help': 'Tasukete (助けて)',
                'bathroom': 'Toire wa doko desu ka? (トイレはどこですか)',
                'english': 'Eigo o hanasemasu ka? (英語を話せますか)',
                'bill': 'Okaikei onegaishimasu (お会計お願いします)'
            }
        }
    
    def get_cultural_info(
        self,
        destination: str,
        category: Optional[str] = None
    ) -> Any:
        """
        Get cultural information for destination
        
        Args:
            destination: Destination name
            category: Specific category or None for all
            
        Returns:
            Cultural data
        """
        data = self.cultural_data.get(destination.lower())
        if data and category:
            return data.get(category)
        return data
    
    def get_basic_phrases(self, destination: str) -> Optional[Dict[str, str]]:
        """
        Get basic phrases for destination
        
        Args:
            destination: Destination name
            
        Returns:
            Phrase dictionary or None
        """
        return self.phrases.get(destination.lower())
    
    def get_tipping_guide(self, destination: str) -> Optional[Dict[str, str]]:
        """
        Get tipping customs
        
        Args:
            destination: Destination name
            
        Returns:
            Tipping guide or None
        """
        data = self.cultural_data.get(destination.lower())
        if data:
            return data.get('tipping')
        return None
    
    def get_dos_and_donts(self, destination: str) -> Optional[Dict[str, List[str]]]:
        """
        Get cultural do's and don'ts
        
        Args:
            destination: Destination name
            
        Returns:
            Dict with 'dos' and 'donts' lists
        """
        data = self.cultural_data.get(destination.lower())
        if data:
            return {
                'dos': data.get('dos', []),
                'donts': data.get('donts', [])
            }
        return None
