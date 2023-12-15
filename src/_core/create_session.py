from .session import Session
from .engine import Engine
from .drivers.session_factory import SessionFactory

def create_session(engine: Engine) -> Session:
    """Create session.
    
    Args:
        engine: The engine of python_orm.
        
    Returns:
        Session: The database session.
    """
    return SessionFactory.create(engine.driver, engine.connection, engine.adapter)