import sys

import core
from gui import mainboard
import inspectors

if __name__ == "__main__":
    if len(sys.argv) == 1:
        mainboard.show()