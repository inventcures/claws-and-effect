import subprocess
import os
from typing import Tuple

class ShellTool:
    @staticmethod
    def execute(command: str, cwd: str = None) -> Tuple[int, str, str]:
        """
        Executes a shell command and returns the exit code, stdout, and stderr.
        This provides full access to the local filesystem and terminal.
        """
        try:
            result = subprocess.run(
                command, 
                shell=True, 
                cwd=cwd or os.getcwd(), 
                capture_output=True, 
                text=True
            )
            return result.returncode, result.stdout, result.stderr
        except Exception as e:
            return 1, "", str(e)

    @staticmethod
    def write_file(filepath: str, content: str):
        """Utility to write files directly to the filesystem."""
        # Ensure directory exists
        os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)
        with open(filepath, 'w') as f:
            f.write(content)
