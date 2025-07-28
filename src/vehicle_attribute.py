from dataclasses import dataclass, field
from typing import List


@dataclass
class VehicleAttribute:
    name: str
    aliases: List[str] = field(default_factory=list)
    
    def get_all_terms(self) -> List[str]:
        """Return all terms (name + aliases) for this attribute."""
        return [self.name] + self.aliases
    
    def matches(self, text: str) -> bool:
        """Check if any term (name or alias) appears in the given text."""
        text_lower = text.lower()
        return any(term.lower() in text_lower for term in self.get_all_terms()) 