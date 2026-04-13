from app.models.schema import AgentInternalResult

class ResultEvaluator:
    def __init__(self):
        # Expanded markers for a tougher audit
        self.uncertainty_markers = {"maybe", "possibly", "i think", "likely", "unclear", "guess", "not sure"}

    async def evaluate(self, internal_result: AgentInternalResult) -> dict:
        """
        Exhaustive audit of the Generator's output. 
        Complexity: O(N*M) where N is steps and M is markers.
        """
        flags = set()
        base_score = 1.0
        
        # 1. Logic Depth & Quality Check
        steps = internal_result.reasoning_steps
        if len(steps) < 3:
            flags.add("insufficient_logic_depth")
        
        # Check if steps are too short (low quality)
        avg_step_length = sum(len(s) for s in steps) / len(steps) if steps else 0
        if avg_step_length < 10:
            flags.add("low_quality_reasoning")

        # 2. Uncertainty Detection (Single Pass)
        raw_answer_lower = internal_result.raw_answer.lower()
        
        # Scan reasoning steps
        for step in steps:
            step_lower = step.lower()
            if any(marker in step_lower for marker in self.uncertainty_markers):
                flags.add("uncertainty_in_reasoning")
                break # One hit is enough to flag

        # Scan final answer
        if any(marker in raw_answer_lower for marker in self.uncertainty_markers):
            flags.add("uncertainty_in_answer")

        # 3. Final Scoring Logic (Deductive Model)
        # Instead of hardcoding scores, we deduct weight for each flag
        deductions = {
            "insufficient_logic_depth": 0.3,
            "low_quality_reasoning": 0.2,
            "uncertainty_in_reasoning": 0.4,
            "uncertainty_in_answer": 0.5
        }

        for flag in flags:
            base_score -= deductions.get(flag, 0.1)

        return {
            "flags": list(flags),
            "confidence_score": max(0.0, round(base_score, 2))
        }