"""Run the local Hugo binary, including on workspaces mounted without execution."""
from pathlib import Path
import os,sys
binary=Path(__file__).with_name('hugo')
fd=os.memfd_create('bootstrap-hugo',0)
with binary.open('rb') as stream:
 while block:=stream.read(1024*1024):os.write(fd,block)
os.execve(f'/proc/self/fd/{fd}', ['hugo',*sys.argv[1:]],os.environ)
