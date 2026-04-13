from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schema import VerificationRequest, VerificationResponse
from app.services.verifier_service import VerifierService
from app.utils.exceptions import SafetyViolation, AgentFailure
from app.utils.logger import logger
from app.config import Settings, get_settings

router = APIRouter()

@router.post(
    "/verify", 
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    tags=["Core Engine"],
    summary="NOISEKILLER Verification Endpoint"
)
async def verify_ai_output(
    request: VerificationRequest, 
    service: VerifierService = Depends(VerifierService),
    config: Settings = Depends(get_settings)
):
    """
    High-performance, armored endpoint for AI Verification.
    Balanced for throughput and enterprise-grade error handling.
    """
    try:
        # The 'Service' remains the orchestrator for the Multi-Agent flow
        return await service.verify_output(request)

    except SafetyViolation as sv:
        # Triggered by SafetyGuard (Forbidden code/keywords)
        logger.warning(f"NOISEKILLER Security Alert: {str(sv)}")
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=f"Safety Protocol: {str(sv)}"
        )

    except AgentFailure as af:
        # Triggered if Gemini/OpenAI is down or returns garbage
        logger.error(f"NOISEKILLER Agent Failure: {str(af)}")
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Upstream AI agents failed to respond."
        )

    except Exception as e:
        # The ultimate fail-safe for unexpected crashes
        logger.critical(f"System Crash: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal engine error occurred."
        )