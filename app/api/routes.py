from fastapi import APIRouter, HTTPException, Depends, status
from app.models.schema import VerificationRequest, VerificationResponse
from app.services.verifier_service import VerifierService
import logging

# Set up logging to track errors without exposing them to the user
logger = logging.getLogger(__name__)

router = APIRouter()

# Dependency provider to ensure we use a clean instance of the service
def get_verifier_service():
    return VerifierService()

@router.post(
    "/verify", 
    response_model=VerificationResponse,
    status_code=status.HTTP_200_OK,
    summary="Verify an AI-generated output",
    description="Processes a query through the Multi-Agent Verification pipeline."
)
async def verify_ai_output(
    request: VerificationRequest, 
    service: VerifierService = Depends(get_verifier_service)
):
    """
    Primary endpoint for the TrustLayer AI engine.
    """
    try:
        # Single execution call with await
        response = await service.verify_output(request)
        return response

    except ValueError as ve:
        # Catch validation errors (e.g., empty strings caught by Pydantic)
        logger.warning(f"Validation error: {ve}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail=f"Invalid request data: {str(ve)}"
        )   
     
    except Exception as e:
        logger.error(f"Internal Engine Error: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER__ERROR, 
            detail="An internal error occurred while verifying the output."
        )