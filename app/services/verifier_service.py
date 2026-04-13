import time
from app.models.schema import VerificationRequest, VerificationResponse
from app.core.generator.code_generator import CodeGenerator
from app.core.evaluator.result_evaluator import ResultEvaluator

class VerifierService:
    def __init__(self):
        # Initialize your Multi-Agent team
        self.generator = CodeGenerator()
        self.evaluator = ResultEvaluator()
        self.min_trust_threshold = 0.7

    async def verify_output(self, request: VerificationRequest) -> VerificationResponse:
        start_time = time.perf_counter()

        # 1. GENERATION PHASE
        # The Generator creates the answer and its reasoning steps
        agent_internal = await self.generator.generate(
            query=request.query, 
            context=request.context
        )

        # 2. EVALUATION PHASE (The Critic)
        # The Evaluator audits the internal reasoning of the Generator
        audit_results = await self.evaluator.evaluate(agent_internal)

        # 3. VERIFICATION LOGIC
        # We decide if the answer is 'Verified' based on the score and specific red flags
        confidence_score = audit_results["confidence_score"]
        risk_flags = audit_results["flags"]
        
        is_verified = (
            confidence_score >= self.min_trust_threshold and 
            "uncertainty_in_answer" not in risk_flags
        )

        # 4. FINAL PACKAGING
        execution_ms = int((time.perf_counter() - start_time) * 1000)

        return VerificationResponse(
            final_answer=agent_internal.raw_answer,
            confidence_score=confidence_score,
            sources=agent_internal.suggested_sources,
            risk_flags=risk_flags,
            verified=is_verified,
            execution_time_ms=execution_ms
        )