import pytest
from copy import deepcopy
import json
from datetime import datetime
from . import NumbaNumericEncoder
import numpy as np


def test_mock():
    assert True == True
    
def test_numpy_encode():
    character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 71, 1, dtype=np.uint8)])
    x = np.load('test.npy')
    x = x[:20, 0]
    encoded = '0000000000000E1000001C2000015F9000016DA000017BB0000189C0000197D00001A5E00001B3F00001C2000001D0100001DE200001EC300001FA400002085000021660000224700002328000024090'
    
    result = NumbaNumericEncoder.encode_vector(x, character_set, 'int', 0, False, 8)
    assert encoded == result

def test_numpy_decode():
    character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 71, 1, dtype=np.uint8)])
    x = np.load('test.npy')
    x = x[:20, 0]
    encoded = '0000000000000E1000001C2000015F9000016DA000017BB0000189C0000197D00001A5E00001B3F00001C2000001D0100001DE200001EC300001FA400002085000021660000224700002328000024090'

    decoding_table = np.zeros(256, dtype=np.uint8)
    for i, idx in enumerate(character_set):
        decoding_table[idx] = i
    
    result = NumbaNumericEncoder.decode_vector(encoded, decoding_table, 'int', 0, False, 8)
    for i, r in enumerate(result):
        assert x[i] == r

def test_numpy_rencode():
    character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 71, 1, dtype=np.uint8)])
    x = np.load('test.npy')
    x = x[:20, 0]

    decoding_table = np.zeros(256, dtype=np.uint8)
    for i, idx in enumerate(character_set):
        decoding_table[idx] = i
    
    encoded = NumbaNumericEncoder.encode_vector(x, character_set, 'int', 0, False, 8)
    result = NumbaNumericEncoder.decode_vector(encoded, decoding_table, 'int', 0, False, 8)
    for i, r in enumerate(result):
        assert x[i] == r
   
def test_numpy_rencode_float():
    character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 71, 1, dtype=np.uint8)])
    x = np.load('test.npy')
    x = x[:20, 0]

    decoding_table = np.zeros(256, dtype=np.uint8)
    for i, idx in enumerate(character_set):
        decoding_table[idx] = i
    
    encoded = NumbaNumericEncoder.encode_vector(x, character_set, 'float', 2, False, 8)
    result = NumbaNumericEncoder.decode_vector(encoded, decoding_table, 'float', 2, False, 8)
    for i, r in enumerate(result):
        assert x[i] == r

def test_numpy_rencode_signed():
    character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 71, 1, dtype=np.uint8)])
    x = np.load('test.npy')
    x = x[:20, 0]

    decoding_table = np.zeros(256, dtype=np.uint8)
    for i, idx in enumerate(character_set):
        decoding_table[idx] = i
    
    encoded = NumbaNumericEncoder.encode_vector(x, character_set, 'float', 2, True, 8)
    result = NumbaNumericEncoder.decode_vector(encoded, decoding_table, 'float', 2, True, 8)
    for i, r in enumerate(result):
        assert x[i] == r