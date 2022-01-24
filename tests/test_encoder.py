from src.timeseriesencoder  import NumericEncoder
import pytest
import numpy as np

def runner(encoder, verbose=False):
    if encoder.signed:
        min_state = encoder.get_max_state() * -1
    else:
        min_state = 0
    if encoder.numeric_type == 'float':
        max_value = encoder.get_max_state() / (10 ** encoder.float_precision)
        min_value = min_state / (10 ** encoder.float_precision)
    else:
        max_value = encoder.get_max_state()
        min_value = min_state

    if encoder.numeric_type == 'float': 
        c = np.arange(min_value, max_value, 10 ** (-1 * encoder.float_precision)).round(encoder.float_precision)
    else:
        c = np.arange(min_value, max_value, 1).round(encoder.float_precision)

    encoded = encoder.encode(c)
    result = encoder.decode(encoded)
    if verbose:
        print(f'Input: {c}, Encoded: {encoded}, Decoded: {result}')

    for i in range(len(c)):
        assert c[i] == result[i]
            

def test_signed_1bit_int():
    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int')
    runner(encoder)

def test_unsigned_1bit_int():
    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int')
    runner(encoder)

def test_signed_1bit_float_1():
    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_unsigned_1bit_float_1():
    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_signed_1bit_float_2():
    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2)
    runner(encoder)

def test_unsigned_1bit_float_2():
    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2)
    runner(encoder)


def test_signed_2bit_int():
    encoder = NumericEncoder(signed = True, encoding_depth = 2, numeric_type = 'int')
    runner(encoder)

def test_unsigned_2bit_int():
    encoder = NumericEncoder(signed = False, encoding_depth = 2, numeric_type = 'int')
    runner(encoder)

def test_signed_2bit_float_1():
    encoder = NumericEncoder(signed = True, encoding_depth = 2, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_unsigned_2bit_float_1():
    encoder = NumericEncoder(signed = False, encoding_depth = 2, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_signed_2bit_float_1():
    encoder = NumericEncoder(signed = True, encoding_depth = 2, numeric_type = 'float', float_precision = 2)
    runner(encoder)

def test_unsigned_2bit_float_1():
    encoder = NumericEncoder(signed = False, encoding_depth = 2, numeric_type = 'float', float_precision = 2)
    runner(encoder)

def test_all():
    for depth in range(2):
        encoder = NumericEncoder(signed = False, encoding_depth = depth+1, numeric_type = 'int')
        runner(encoder)
        encoder = NumericEncoder(signed = True, encoding_depth = depth+1, numeric_type = 'int')
        runner(encoder)
        for prec in range(2):
            encoder = NumericEncoder(signed = False, encoding_depth = depth+1, numeric_type = 'float', float_precision = prec+1)
            runner(encoder)
            encoder = NumericEncoder(signed = True, encoding_depth = depth+1, numeric_type = 'float', float_precision = prec+1)
            runner(encoder)

def test_base16():
    encoding_size = 16
    encoder = NumericEncoder(signed = True, encoding_depth = 3, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)
    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2, encoding_size = encoding_size)
    runner(encoder)

def test_base64():
    encoding_size = 64
    encoder = NumericEncoder(signed = True, encoding_depth = 3, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)
    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2, encoding_size = encoding_size)
    runner(encoder)

def test_base91():
    encoding_size = 91
    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)
    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int', encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2, encoding_size = encoding_size)
    runner(encoder)

    encoder = NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2, encoding_size = encoding_size)
    runner(encoder)