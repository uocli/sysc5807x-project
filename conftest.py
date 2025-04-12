import sys
from pathlib import Path

# Get the project root directory
project_root = Path(__file__).parent.absolute()

# Add the src directory to Python's module search path
sys.path.append(str(project_root / "src"))
