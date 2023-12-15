from abc import ABC, abstractmethod
from typing import Any

from .url import Url

class Connectin(ABC):
    """The Connection to database."""
    @abstractmethod
    def connect(self, url: Url) -> Any:
        """Connect to database.

        Args:
            url: The url for the database connection. 

        Returns:
            Any: Database connection.
        """
        pass
    
    @abstractmethod
    def close(self):
        """Close database connection."""
        pass
