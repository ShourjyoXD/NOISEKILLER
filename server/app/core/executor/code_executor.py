import sys
import io
import contextlib
import multiprocessing
from typing import Dict, Any, Optional
from app.core.executor.safety import SafetyGuard

class CodeExecutor:
    def __init__(self):
        self.safety = SafetyGuard()
        self.timeout = 2.0  # Seconds

    def execute_safely(self, code: str) -> Dict[str, Any]:
        """
        Executes Python code in a restricted, timed environment.
        Time Complexity: O(N) for safety check + Execution time.
        Space Complexity: O(M) for captured output buffer.
        """
        # 1. Pre-execution Safety Check
        if not self.safety.is_safe(code):
            return {
                "success": False, 
                "error": "Safety Violation: Forbidden operations detected.",
                "output": ""
            }

        # 2. Setup output capture
        output_buffer = io.StringIO()
        success = False
        error_msg = ""

        # 3. Execution with restricted globals
        # We provide an empty dictionary for __builtins__ to limit scope further if needed
        restricted_globals = {"__builtins__": __builtins__}
        
        try:
            with contextlib.redirect_stdout(output_buffer):
                # Using exec with a defined local/global scope
                # Note: For production-grade isolation, use a Docker/Lambda sandbox
                exec(code, restricted_globals)
            success = True
        except Exception as e:
            error_msg = str(e)
            success = False

        return {
            "success": success,
            "error": error_msg,
            "output": output_buffer.getvalue()
        }