"""Verify the required native IR and compiler through the published DOS batch."""
from pathlib import Path
import runpy
if __name__=="__main__":runpy.run_path(str(Path(__file__).with_name("verify_toolchain_dos.py")),run_name="__main__")
