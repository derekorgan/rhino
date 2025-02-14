from abc import ABC, abstractmethod
from typing import List, Any

class BaseService(ABC):
    """Base class for all external service integrations"""
    
    @abstractmethod
    async def initialize(self) -> None:
        """Initialize any necessary connections or tokens"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """Check if the service is accessible"""
        pass

class BaseActivityService(BaseService):
    """Base class for services that provide activity data"""
    
    @abstractmethod
    async def get_activities(self, limit: int) -> List[Any]:
        """Get recent activities"""
        pass 