import sys, os
INTERP = os.path.join(os.environ['HOME'], 'zw143976.truro-it.com', 'venv', 'bin', 'python')
if sys.executable != INTERP:
    os.execl(INTERP, INTERP, *sys.argv)
sys.path.append(os.getcwd())


sys.path.append('other_main')
from other_main import create_app as application