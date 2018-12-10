
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .Entry import *

class co2Entry(Entry):
    def printco2Entry(self):
        print("Printing CO2 Entry...")
        super().printEntry()
