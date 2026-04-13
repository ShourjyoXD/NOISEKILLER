from pydantic import BaseModel, Field, field_validator
from typing import Optional, List, Dict, Any
import uuid

class VerificationRequest(BaseModel):
    """The entry point for the API."""
    query: str = Field(..., min_length=1, max_length=5000)
    context: Optional[str] = Field(None, max_length=20000)
    metadata: Dict[str, Any] = Field(default_factory=dict)

class AgentInternalResult(BaseModel):
    """The internal handshake between Generator and Critic."""
    generation_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    raw_answer: str = Field(..., min_length=1)
    reasoning_steps: List[str] = Field(default_factory=list)
    suggested_sources: List[str] = Field(default_factory=list)
    
    @field_validator('raw_answer')
    @classmethod
    def check_not_empty(cls, v):
        if not v.strip():
            raise ValueError("Agent returned an empty answer.")
        return v

class VerificationResponse(BaseModel):
    """The final verified package sent to the user."""
    final_answer: str
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0)
    sources: List[str] = Field(default_factory=list)
    risk_flags: List[str] = Field(default_factory=list)
    verified: bool = False
    execution_time_ms: Optional[int] = None

    @field_validator('confidence_score')
    @classmethod
    def round_score(cls, v):
        return round(v, 4)