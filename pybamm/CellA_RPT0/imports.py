import pybamm
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent

sys.path.append(str(root))

from DC1 import DC1
from DFN import DFN
import PARAMS
import ERRORS