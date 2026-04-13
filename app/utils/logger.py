import logging
import sys
from app.config import get_settings

settings = get_settings()

def setup_logger(name: str = "NOISEKILLER"):
    """
    Configures a centralized logger with stream handling.
    """
    logger = logging.getLogger(name)
    
    # Avoid duplicate logs if the logger is already initialized
    if not logger.handlers:
        logger.setLevel(settings.log_level)
        
        # Professional Format: [Timestamp] [Level] [Logger Name]: Message
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Output to standard console (stdout)
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger

# Create a global instance for convenience
logger = setup_logger()