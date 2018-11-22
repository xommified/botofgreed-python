import sys
import os

sys.path.insert(0, os.path.abspath('.'))
from botofgreed.ygoprices import utils

utils.check_for_new_sets()
    # utils.get_card_names()
