from numpy import zeros
import pytest
from copy import deepcopy
from numpyencoder import NumpyEncoder
import json
import numpy as np

from src.timeseriesencoder import TimeSeriesEncoder
import sys

def test_mock():
    csv = get_csv_sample()
    

def get_csv_sample():
    with open("./tests/bebez.csv", 'r') as ifile:
        return ifile.read()