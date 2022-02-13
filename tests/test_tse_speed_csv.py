import pytest
from sqlalchemy import false
from timeseriesencoder  import TimeSeriesEncoder, JSONEncoder, CSVEncoder
from copy import deepcopy
from numpyencoder import NumpyEncoder
import json
from datetime import datetime
import time
import pandas as pd
import hashlib


def get_sample_file():
    df = pd.read_csv("./tests/sample.csv")
    df = df.sort_values('date')
    return df.to_csv(index=False)

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

def evalWithTime(f):
    start_time = time.time()
    r = f() 
    return r, (time.time() - start_time)

def test_64bit_speed():
    assert sample == JSONEncoder.decode_json(JSONEncoder.encode_json(sample_copy, ts_key = 'UTC', ts_value = 'Value', sort_values = False, encoding_size = 64)) 

if __name__ == '__main__':
    import cProfile, pstats
    e = CSVEncoder.encode_csv(sample, time_column = 'date', key_columns=["ent_code", "tag"], sort_values = False, encoding_size = 64, gzip=False)
    with cProfile.Profile() as pr:
        d = CSVEncoder.decode_csv(e)
    from pstats import SortKey
    ps = pstats.Stats(pr).sort_stats(SortKey.TIME)
    ps.print_stats(0.05)
    


def test_get_speed():
    rows = []
    for s in [True, False]:
        for k in [64]:
            for z in [False, True]:
                encoded = None
                for f in [CSVEncoder.encode_csv, CSVEncoder.decode_csv]:
                    print(f.__name__, s, k, z)
                    if encoded is None:
                        encoded, t = evalWithTime(lambda: f(sample, time_column = 'date', key_columns=["ent_code", "tag"], encoding_size = k, gzip=z))
                    else:
                        decoded, t = evalWithTime(lambda: f(encoded, gzip=z))
                    rows.append(pd.DataFrame([[f.__name__, s, k, z, t]]))

    df = pd.concat(rows)
    df.columns=["Function", "Sort", "Size", "Zip", "Time"]
    df = df.sort_values(by="Time")
    s = df.to_csv(index=False)
    print(s)