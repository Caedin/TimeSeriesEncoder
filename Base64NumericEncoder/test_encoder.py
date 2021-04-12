from Base64NumericEncoder import Base64NumericEncoder
import pytest

def runner(encoder, verbose=False):
    c = encoder.min_value
    while c < encoder.max_value:
        if verbose:
            print(f'Input: {c}, Encoded: {encoder.encode(c)}, Decoded: {encoder.decode(encoder.encode(c))}')

        if encoder.numeric_type == float:
            assert c == encoder.decode(encoder.encode(c))
            c += 10 ** (-1 * encoder.float_precision)
            c = round(c, encoder.float_precision)
        else:
            assert c == encoder.decode(encoder.encode(c))
            c += 1

def test_encode_range_errors():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 7)
    with pytest.raises(ValueError):
        encoder.encode(50000000000000)
    with pytest.raises(ValueError):
        encoder.encode(-50000000000000)

def test_encode_valid():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 7)
    encoder.encode(50000)
    encoder.encode(-50000)

def test_signed_1bit_int():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = int)
    runner(encoder)

def test_unsigned_1bit_int():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = int)
    runner(encoder)

def test_signed_1bit_float_1():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = float, float_precision = 1)
    runner(encoder)

def test_unsigned_1bit_float_1():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = float, float_precision = 1)
    runner(encoder)

def test_signed_1bit_float_2():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = float, float_precision = 2)
    runner(encoder)

def test_unsigned_1bit_float_2():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = float, float_precision = 2)
    runner(encoder)


def test_signed_2bit_int():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 2, numeric_type = int)
    runner(encoder)

def test_unsigned_2bit_int():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 2, numeric_type = int)
    runner(encoder)

def test_signed_2bit_float_1():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 2, numeric_type = float, float_precision = 1)
    runner(encoder)

def test_unsigned_2bit_float_1():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 2, numeric_type = float, float_precision = 1)
    runner(encoder)

def test_signed_2bit_float_1():
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 2, numeric_type = float, float_precision = 2)
    runner(encoder)

def test_unsigned_2bit_float_1():
    encoder = Base64NumericEncoder(signed = False, encoding_depth = 2, numeric_type = float, float_precision = 2)
    runner(encoder)

def test_all():
    for depth in range(2):
        encoder = Base64NumericEncoder(signed = False, encoding_depth = depth+1, numeric_type = int)
        runner(encoder)
        encoder = Base64NumericEncoder(signed = True, encoding_depth = depth+1, numeric_type = int)
        runner(encoder)
        for prec in range(2):
            encoder = Base64NumericEncoder(signed = False, encoding_depth = depth+1, numeric_type = float, float_precision = prec+1)
            runner(encoder)
            encoder = Base64NumericEncoder(signed = True, encoding_depth = depth+1, numeric_type = float, float_precision = prec+1)
            runner(encoder)

def test_base16():
    character_set = [Base64NumericEncoder.get_base_16()
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 3, numeric_type = int, character_set = character_set)
    runner(encoder)
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = int, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = int, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = float, float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = float, float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = float, float_precision = 2, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = float, float_precision = 2, character_set = character_set)
    runner(encoder)

def test_base90():
    character_set = Base64NumericEncoder.get_base_90()
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 3, numeric_type = int, character_set = character_set)
    runner(encoder, verbose=True)
    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = int, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = int, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = float, float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = float, float_precision = 1, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = True, encoding_depth = 1, numeric_type = float, float_precision = 2, character_set = character_set)
    runner(encoder)

    encoder = Base64NumericEncoder(signed = False, encoding_depth = 1, numeric_type = float, float_precision = 2, character_set = character_set)
    runner(encoder)