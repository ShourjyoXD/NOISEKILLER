import uuid
import re
from typing import Optional
from app.models.schema import AgentInternalResult

class CodeGenerator:
    def __init__(self, model_name: str = "Gemini 2.5 Flash"):
        self.model_name = model_name

    async def generate(self, query: str, context: Optional[str] = None) -> AgentInternalResult:
        """
        Generates a structured response by prompting the LLM to separate 
        the answer from the reasoning.
        """
        
        # 1. System Prompt Engineering
        # We define a 'Contract' with the AI to ensure parsable output.
        system_instructions = (
            f"You are the Generator Agent for TrustLayer AI. "
            f"Use the following context if provided: {context if context else 'No context provided.'}\n"
            f"Provide your response in the following strict format:\n"
            f"[[ANSWER]]: <your final answer>\n"
            f"[[REASONING]]: <step-by-step logic, comma-separated>"
        )

        # 2. Simulated LLM Call 
        simulated_llm_raw_output = (
            f"[[ANSWER]]: Based on the query '{query}', the result is optimal. "
            f"[[REASONING]]: Identified user intent, cross-referenced context, verified logic"
        )

        # 3. Robust Parsing (Using Regex instead of .split)
        # This is more space-efficient and less prone to character collisions
        answer_match = re.search(r"\[\[ANSWER\]\]:\s*(.*?)(?=\[\[|$)", simulated_llm_raw_output, re.DOTALL)
        reasoning_match = re.search(r"\[\[REASONING\]\]:\s*(.*)", simulated_llm_raw_output, re.DOTALL)

        raw_answer = answer_match.group(1).strip() if answer_match else "Error: Could not parse answer."
        
        # Handle the reasoning steps as a list
        if reasoning_match:
            reasoning_steps = [step.strip() for step in reasoning_match.group(1).split(",") if step.strip()]
        else:
            reasoning_steps = ["No explicit reasoning provided by model."]

        # 4. Return the standard internal contract
        return AgentInternalResult(
            generation_id=str(uuid.uuid4()),
            raw_answer=raw_answer,
            reasoning_steps=reasoning_steps,
            suggested_sources=["Internal Knowledge"] if not context else ["Provided Context"]
        )