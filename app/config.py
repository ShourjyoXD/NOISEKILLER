from app.models.schema import AgentInternalResult
from app.core.executor.safety import SafetyGuard
from app.constants.prompts import FIXER_SYSTEM_PROMPT # We'll define this below
import uuid

class CodeFixer:
    def __init__(self):
        self.safety = SafetyGuard()
        self.max_retries = 3

    async def fix_code(self, original_code: str, error_msg: str, query: str) -> AgentInternalResult:
        """
        Attempts to repair broken code using the error traceback.
        Time Complexity: O(LLM_Latency)
        Space Complexity: O(N) for the new code string.
        """
        
        # 1. Prompt Construction
        # We explicitly show the AI what went wrong so it can "debug"
        repair_instruction = (
            f"Original Query: {query}\n"
            f"Broken Code:\n{original_code}\n"
            f"Error Message: {error_msg}\n"
            f"Task: Fix the code so it executes successfully and satisfies the query."
        )

        # 2. Simulated LLM Repair Call
        # (In Phase 3, this becomes a call to Gemini)
        fixed_code_simulated = f"# Fixed logic\nprint('Fixed output for {query}')"
        
        # 3. Safety First
        # Never trust a 'fix' without re-scanning it
        is_safe = self.safety.is_safe(fixed_code_simulated)
        
        if not is_safe:
            return AgentInternalResult(
                raw_answer="Safety violation detected in suggested fix.",
                reasoning_steps=["Fixer suggested unsafe code", "SafetyGuard blocked result"],
                suggested_sources=["Security Engine"]
            )

        # 4. Logical Check
        # If the AI just returned the same code, it didn't fix anything
        if fixed_code_simulated.strip() == original_code.strip():
            return AgentInternalResult(
                raw_answer="The engine was unable to resolve the code error.",
                reasoning_steps=["Attempted fix produced identical results", "Aborting fix loop"],
                suggested_sources=["Fixer Logic"]
            )

        return AgentInternalResult(
            generation_id=str(uuid.uuid4()),
            raw_answer=fixed_code_simulated,
            reasoning_steps=["Analyzed traceback", "Identified logic error", "Generated patch"],
            suggested_sources=["Self-Healing Agent"]
        )