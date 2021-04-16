from Base64NumericEncoder import Base64NumericEncoder
import pytest
import numpy as np

def runner(encoder, verbose=False):
    if encoder.numeric_type == 'float': 
        c = np.arange(encoder.min_value, encoder.max_value, 10 ** (-1 * encoder.float_precision)).round(encoder.float_precision)
    else:
        c = np.arange(encoder.min_value, encoder.max_value, 1).round(encoder.float_precision)

    encoded = encoder.encode(c)
    result = encoder.decode(encoded)
    if verbose:
        print(f'Input: {c}, Encoded: {encoded}, Decoded: {result}')

    for i in range(len(c)):
        assert c[i] == result[i]
            

def test_signed_1bit_int():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int')
    runner(encoder)

def test_unsigned_1bit_int():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int')
    runner(encoder)

def test_signed_1bit_float_1():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_unsigned_1bit_float_1():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_signed_1bit_float_2():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2)
    runner(encoder)

def test_unsigned_1bit_float_2():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2)
    runner(encoder)


def test_signed_2bit_int():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 2, numeric_type = 'int')
    runner(encoder)

def test_unsigned_2bit_int():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 2, numeric_type = 'int')
    runner(encoder)

def test_signed_2bit_float_1():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 2, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_unsigned_2bit_float_1():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 2, numeric_type = 'float', float_precision = 1)
    runner(encoder)

def test_signed_2bit_float_1():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 2, numeric_type = 'float', float_precision = 2)
    runner(encoder)

def test_unsigned_2bit_float_1():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 2, numeric_type = 'float', float_precision = 2)
    runner(encoder)

def test_all():
    for depth in range(2):
        encoder = Base64NumericEncoder(signed = False, encoding_depth = depth+1, numeric_type = 'int')
        runner(encoder)
        encoder = Base64NumericEncoder(signed = True, encoding_depth = depth+1, numeric_type = 'int')
        runner(encoder)
        for prec in range(2):
            encoder = Base64NumericEncoder(signed = False, encoding_depth = depth+1, numeric_type = 'float', float_precision = prec+1)
            runner(encoder)
            encoder = Base64NumericEncoder(signed = True, encoding_depth = depth+1, numeric_type = 'float', float_precision = prec+1)
            runner(encoder)

def test_base16():
    character_set = Base64NumericEncoder.get_base_16()
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 3, numeric_type = 'int', character_set = character_set)
    runner(encoder)
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int', character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2, character_set = character_set)
    runner(encoder)

def test_base64():
    character_set = Base64NumericEncoder.get_base_64()
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 3, numeric_type = 'int', character_set = character_set)
    runner(encoder)
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int', character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2, character_set = character_set)
    runner(encoder)

def test_base91():
    character_set = Base64NumericEncoder.get_base_91()
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', character_set = character_set)
    runner(encoder)
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'int', character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'int', character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = 'float', float_precision = 2, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = 'float', float_precision = 2, character_set = character_set)
    runner(encoder)