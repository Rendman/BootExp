"""Compatibility entry point for the continuing construction checks."""
from pathlib import Path
import runpy,sys
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/"qa/toolchain"))
runpy.run_path(str(ROOT/'qa/toolchain/bootstrap_chain.py'),run_name="__main__")
