from pathlib import Path
import sys
root=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(root))
from src.pipeline import run
print(run(Path(__file__).resolve().parents[1]))
