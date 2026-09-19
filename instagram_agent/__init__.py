"""
Standalone Instagram Specialist Agent Package.
Supports: Carousels, Static Posts, Stories, Content Calendars.
Reels: Coming Soon (architecture reserved).
"""

from .agent.instagram_agent import InstagramSpecialistAgent
from .schemas.input_contract import InstagramAgentInput
from .schemas.output_contract import InstagramAgentOutput

__all__ = [
    "InstagramSpecialistAgent",
    "InstagramAgentInput",
    "InstagramAgentOutput",
]
