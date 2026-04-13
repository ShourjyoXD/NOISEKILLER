class NoiseKillerError(Exception):
    """Base exception for all NOISEKILLER engine errors."""
    def __init__(self, message: str, metadata: dict = None):
        super().__init__(message)
        self.metadata = metadata or {}

class AgentFailure(NoiseKillerError):
    """Raised when a specific AI agent (Generator/Critic) fails."""
    pass

class SafetyViolation(NoiseKillerError):
    """Raised when the SafetyGuard blocks dangerous code."""
    pass

class ExecutionTimeout(NoiseKillerError):
    """Raised when code execution exceeds the allowed time limit."""
    pass

class ConfigurationError(NoiseKillerError):
    """Raised when required environment variables are missing."""
    pass