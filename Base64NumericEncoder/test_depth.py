from Base64NumericEncoder import *
import pytest

def runner(encoder):
    c = encoder.min_value
    while c < encoder.max_value:
        if encoder.numeric_type == float:
            assert c == encoder.decode(encoder.encode(c))
            c += 10 ** (-1 * encoder.float_precision)
            c = round(c, encoder.float_precision)
        else:
            assert c == encoder.decode(encoder.encode(c))
            c += 1

def test_depth_1():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = float, float_precision = 4)
    runner(encoder)

def test_depth_2():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 2, numeric_type = float, float_precision = 4)
    runner(encoder)

def test_depth_3():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 3, numeric_type = float, float_precision = 4)
    runner(encoder)
