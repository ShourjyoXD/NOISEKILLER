import ast
from typing import Set

class SafetyGuard:
    """
    Advanced AST-based safety checker. 
    Instead of searching for strings, it parses the code structure.
    """
    # Specifically forbidden function calls and imports
    FORBIDDEN_NODES: Set[str] = {
        "os", "subprocess", "shutil", "sys", "builtins", 
        "eval", "exec", "getattr", "setattr", "open"
    }

    def is_safe(self, code: str) -> bool:
        """
        Analyze code safety using Abstract Syntax Trees.
        Time Complexity: O(N) where N is the number of nodes in the code tree.
        Space Complexity: O(N) for the tree representation.
        """
        try:
            # Parse the code into a tree structure
            tree = ast.parse(code)
            
            for node in ast.walk(tree):
                # 1. Check for forbidden imports (e.g., 'import os')
                if isinstance(node, (ast.Import, ast.ImportFrom)):
                    for alias in node.names:
                        if alias.name.split('.')[0] in self.FORBIDDEN_NODES:
                            return False
                
                # 2. Check for forbidden function calls (e.g., 'eval()')
                if isinstance(node, ast.Call):
                    if isinstance(node.func, ast.Name):
                        if node.func.id in self.FORBIDDEN_NODES:
                            return False
                    # Catch 'os.system()' style calls
                    elif isinstance(node.func, ast.Attribute):
                        if isinstance(node.func.value, ast.Name):
                            if node.func.value.id in self.FORBIDDEN_NODES:
                                return False
            
            return True

        except SyntaxError:
            # If the AI produces code that doesn't even compile, it's unsafe/invalid
            return False
        except Exception:
            return False