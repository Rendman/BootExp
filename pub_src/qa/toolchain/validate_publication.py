"""Run the current continuing-ladder checks from this established QA path."""
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'qa'))
from validate_ladder_publication import check

if __name__=='__main__':
 check()
