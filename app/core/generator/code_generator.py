import re
import uuid
import asyncio
from google import genai
from app.config import settings 
from app.constants.prompts import GENERATOR_SYSTEM_PROMPT
from app.models.schema import AgentInternalResult
from app.utils.logger import logger
from app.utils.exceptions import AgentFailure

class CodeGenerator:
    def __init__(self):
        """
        Initializes the Gemini 2.5 Flash Client using the 
        validated key from our global settings object.
        """
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model_id = "gemini-2.5-flash"

    async def generate(self, query: str, context: str = None) -> AgentInternalResult:
        # 1. Format the professional prompt
        prompt = GENERATOR_SYSTEM_PROMPT.format(context_data=context or "No context provided.")
        
        try:
            # 2. Run the Gemini call in a separate thread to keep FastAPI async
            response = await asyncio.to_thread(
                self.client.models.generate_content,
                model=self.model_id,
                contents=f"{prompt}\n\nUser Query: {query}"
            )
            
            if not response or not response.text:
                raise AgentFailure("Gemini 2.5 Flash returned an empty response.")

            raw_text = response.text

            # 3. Robust Extraction (Regex)
            answer_match = re.search(r"\[\[ANSWER\]\]:\s*(.*?)(?=\[\[|$)", raw_text, re.DOTALL)
            reasoning_match = re.search(r"\[\[REASONING\]\]:\s*(.*)", raw_text, re.DOTALL)

            # 4. Final Packaging
            return AgentInternalResult(
                generation_id=str(uuid.uuid4()),
                raw_answer=answer_match.group(1).strip() if answer_match else raw_text.strip(),
                reasoning_steps=[s.strip() for s in reasoning_match.group(1).split(",") if s.strip()] if reasoning_match else ["No reasoning provided."],
                suggested_sources=["Gemini 2.5 Flash Internal Knowledge"]
            )

        except Exception as e:
            logger.error(f"Gemini API Error: {str(e)}")
            raise AgentFailure(f"AI Generation Failed: {str(e)}")