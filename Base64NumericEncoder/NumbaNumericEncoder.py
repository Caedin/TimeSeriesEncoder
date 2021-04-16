
import math
import numpy as np

def encode_vector(vector, encoding_table, numeric_type, float_precision, signed, encoding_depth, encoding_base):
    encoding_size = encoding_base
    vector = np.copy(vector)
    if numeric_type == 'float':
        vector = vector * (10 ** float_precision)

    if signed:
        number_of_states = encoding_size ** encoding_depth
        max_state = int(number_of_states / 2)
        vector = vector + max_state

    vector = np.rint(vector).astype(np.uint64)
    encoded_bytes = np.zeros((vector.shape[0], encoding_depth), dtype=np.uint8)

    for i in range(encoding_depth):
        place_value = (encoding_size ** (encoding_depth - i - 1))
        encoded_bytes[:, i][vector >= place_value] = np.floor_divide(vector[vector >= place_value], place_value)
        vector[vector >= place_value] = vector[vector >= place_value] % place_value
    codes = np.vectorize(encoding_table.item)(encoded_bytes.astype(np.uint8))

    encoded = np.vectorize(chr)(codes.flatten())
    return ''.join(encoded)

def decode_vector(string, decoding_table, numeric_type, float_precision, signed, encoding_depth, encoding_base):
    encoding_size = encoding_base
    vector = np.frombuffer(string.encode('utf-8'), dtype=f'S1').reshape(int(len(string) / encoding_depth),encoding_depth)
    vector = np.vectorize(ord)(vector)
    vector = np.vectorize(decoding_table.item)(vector)

    for i in range(encoding_depth):
        offset = (encoding_size ** (encoding_depth - i - 1))
        vector[:, i] = vector[:, i] * offset
    vector = np.sum(vector, axis=1)

    # Adjust for signage
    if signed:
        number_of_states = encoding_size ** encoding_depth
        max_state = int(number_of_states / 2)
        vector = vector - max_state

    if numeric_type == 'float':
        vector =  np.divide(vector, (10 ** float_precision))

    return vector