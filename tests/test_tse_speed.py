import pytest
from src.timeseriesencoder  import TimeSeriesEncoder
from copy import deepcopy
from numpyencoder import NumpyEncoder
import json
from datetime import datetime
import time
import pandas as pd

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

def evalWithTime(f):
    start_time = time.time()
    r = f() 
    return r, (time.time() - start_time)


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


def test_get_speed():
    rows = []
    for s in [True, False]:
        for k in [16,64,91]:
            for z in [True, False]:
                encoded = None
                for f in [TimeSeriesEncoder.encode_json, TimeSeriesEncoder.decode_json]:
                    key = f"Function: {f.__name__}, Sort: {s}, Size: {k}, Zip: {z}"
                    if encoded is None:
                        encoded, t = evalWithTime(lambda: f(sample, ts_key = 'UTC', ts_value = 'Value', sort_values = s, encoding_size = k, gzip=z))
                    else:
                        _, t = evalWithTime(lambda: f(encoded, gzip=z))
                    rows.append(pd.DataFrame([[f.__name__, s, k, z, t]]))

    df = pd.concat(rows)
    df.columns=["Function", "Sort", "Size", "Zip", "Time"]
    df = df.sort_values(by="Time")
    s = df.to_csv(index=False)
    print(s)