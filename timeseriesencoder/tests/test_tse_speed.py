import pytest
from ..encoders.time_series_encoder import TimeSeriesEncoder
from copy import deepcopy
from numpyencoder import NumpyEncoder
import json
from datetime import datetime

def get_sample_file():
    import json
    with open('./tests/sample.json', 'r') as ifile:
        return json.load(ifile)

def sortvalues(json, time_key):
    if type(json) == dict:
        for k in json:
            json[k] = sortvalues(json[k], time_key)
        return json
    elif type(json) == list:
        if type(json[0]) == dict:
            if time_key in json[0]:
                json.sort(key = lambda x: x[time_key])
                return json

        for i, k in enumerate(json):
            json[i] = sortvalues(json[i], time_key)
        return json
    else:
        return json

sample = get_sample_file()
sample_copy = deepcopy(sample)
sample_sorted = sortvalues(deepcopy(sample), 'UTC')



def test_16bit_speed():
    assert sample == TimeSeriesEncoder.decode_json(TimeSeriesEncoder.encode_json(sample_copy, ts_key = 'UTC', ts_value = 'Value', sort_values = False, encoding_size = 16)) 

def test_64bit_speed():
    assert sample == TimeSeriesEncoder.decode_json(TimeSeriesEncoder.encode_json(sample_copy, ts_key = 'UTC', ts_value = 'Value', sort_values = False, encoding_size = 64)) 

def test_91bit_speed():
    assert sample == TimeSeriesEncoder.decode_json(TimeSeriesEncoder.encode_json(sample_copy, ts_key = 'UTC', ts_value = 'Value', sort_values = False, encoding_size = 91)) 


def test_16bit_speed_sorted():
    assert sample_sorted == TimeSeriesEncoder.decode_json(TimeSeriesEncoder.encode_json(deepcopy(sample_sorted), ts_key = 'UTC', ts_value = 'Value', sort_values = True, encoding_size = 16))

def test_64bit_speed_sorted():
    assert sample_sorted == TimeSeriesEncoder.decode_json(TimeSeriesEncoder.encode_json(deepcopy(sample_sorted), ts_key = 'UTC', ts_value = 'Value', sort_values = True, encoding_size = 64)) 

def test_91bit_speed_sorted():
    assert sample_sorted == TimeSeriesEncoder.decode_json(TimeSeriesEncoder.encode_json(deepcopy(sample_sorted), ts_key = 'UTC', ts_value = 'Value', sort_values = True, encoding_size = 91))

if __name__ == '__main__':
    import cProfile, pstats
    with cProfile.Profile() as pr:
        assert sample == TimeSeriesEncoder.decode_json(TimeSeriesEncoder.encode_json(sample_copy, ts_key = 'UTC', ts_value = 'Value', sort_values = False, encoding_size = 91)) 

    from pstats import SortKey
    ps = pstats.Stats(pr).sort_stats(SortKey.CUMULATIVE)
    ps.print_stats(0.5)