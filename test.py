import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent/'.packages'))
import pytest
raise SystemExit(pytest.main(['tests','-q']))
