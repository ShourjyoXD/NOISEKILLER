import time
from app.models.schema import VerificationRequest, VerificationResponse
from app.core.generator.code_generator import CodeGenerator
from app.core.evaluator.result_evaluator import ResultEvaluator
from app.utils.logger import logger
from app.config import settings

class VerifierService:
    def __init__(self):
        # Initializing core agents
        self.generator = CodeGenerator()
        self.evaluator = ResultEvaluator()
        self.min_trust_threshold = 0.7

    async def verify_output(self, request: VerificationRequest) -> VerificationResponse:
        """
        Orchestrates the NOISEKILLER pipeline.
        """
        start_time = time.perf_counter()
        logger.info(f"Initiating NOISEKILLER for query: {request.query[:30]}...")

        try:
            # 1. GENERATION: The Brain creates an answer
            agent_result = await self.generator.generate(
                query=request.query,
                context=request.context
            )

            # 2. EVALUATION: The Critic audits the logic
            audit = await self.evaluator.evaluate(agent_result)

            # 3. VERIFICATION LOGIC
            confidence = audit.get("confidence_score", 0.0)
            risk_flags = audit.get("flags", [])
            
            is_verified = (
                confidence >= self.min_trust_threshold and 
                "uncertainty_in_answer" not in risk_flags
            )

            execution_ms = int((time.perf_counter() - start_time) * 1000)

            return VerificationResponse(
                final_answer=agent_result.raw_answer,
                confidence_score=confidence,
                sources=agent_result.suggested_sources,
                risk_flags=risk_flags,
                verified=is_verified,
                execution_time_ms=execution_ms
            )

        except Exception as e:
            logger.error(f"NOISEKILLER Pipeline Failure: {str(e)}")
            raise e