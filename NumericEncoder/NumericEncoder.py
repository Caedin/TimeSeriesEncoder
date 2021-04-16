
import math
import numpy as np
from . import NumpyNumericEncoder

class NumericEncoder:
    def __init__(self, numeric_type = None, float_precision = None, signed = None, encoding_depth = None, character_set = None):
        self.numeric_type = numeric_type or 'float'
        self.encoding_depth = encoding_depth or 1
        self.float_precision = float_precision or 0
        self.signed = signed or False

        # Default to base64, but accept an input character set
        self.set_encoding_character_set(character_set)

        if numeric_type == 'int':
            self.float_precision = 0

        number_of_states = self.encoding_size ** self.encoding_depth

        if self.signed:
            self.max_state = int(number_of_states / 2)
            self.min_state = -1 * self.max_state
        else:
            self.max_state = (number_of_states)
            self.min_state = 0 

        if self.numeric_type == 'float':
            self.max_value = self.max_state / (10 ** self.float_precision)
            self.min_value = self.min_state / (10 ** self.float_precision)
        else:
            self.max_value = self.max_state
            self.min_value = self.min_state

    @staticmethod
    def get_base_64():
        character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 91, 1, dtype=np.uint8), np.arange(97, 123, 1, dtype=np.uint8), np.asarray([45, 95], dtype=np.uint8)])
        return character_set

    @staticmethod
    def get_base_16():
        character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 71, 1, dtype=np.uint8)])
        return character_set

    @staticmethod
    def get_base_91():
        character_set = np.concatenate([np.arange(48, 58, 1, dtype=np.uint8), np.arange(65, 91, 1, dtype=np.uint8), np.arange(97, 123, 1, dtype=np.uint8), np.asarray([45, 33, 35, 36, 37, 38, 40, 41, 42, 43, 44, 46, 47, 58, 59, 60, 61, 62, 63, 64, 91, 93, 94, 95, 96, 123, 124, 125, 126], dtype=np.uint8)])
        return character_set
        
    def set_encoding_character_set(self, character_set):
        if character_set is None:
            self.encoding_table = NumericEncoder.get_base_64()
        else:
            self.encoding_table = character_set
        
        self.encoding_size = len(self.encoding_table)
        self.decoding_table = np.zeros(256, dtype=np.uint8)
        for i, idx in enumerate(self.encoding_table):
            self.decoding_table[idx] = i
        
    def encode(self, numeric_data):
        return NumpyNumericEncoder.encode_vector(numeric_data, self.encoding_table, numeric_type = self.numeric_type, float_precision = self.float_precision, signed = self.signed, encoding_depth = self.encoding_depth, encoding_base = self.encoding_size)

    def decode(self, encoded_data):
        return NumpyNumericEncoder.decode_vector(encoded_data, self.decoding_table, numeric_type = self.numeric_type, float_precision = self.float_precision, signed = self.signed, encoding_depth = self.encoding_depth, encoding_base = self.encoding_size)
