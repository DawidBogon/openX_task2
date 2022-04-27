from .tests.test_find_avalible_slot import *
import pytest

files = ["test_find_avalible_slot.py"]
#pytest.main([file for file files])
pytest.main([os.path.realpath(os.path.join(os.path.dirname(__file__), "tests", file)) for file in files])
