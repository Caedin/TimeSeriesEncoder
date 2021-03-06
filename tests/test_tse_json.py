import os
from copy import deepcopy
from numpyencoder import NumpyEncoder
import json
import numpy as np

from src.timeseriesencoder import JSONEncoder
import sys

def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    # Important mark as seen *before* entering recursion to gracefully handle
    # self-referential objects
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size

def test_encode_decode_json_all_sizes():
    sample = get_sample_file()
    sample_sorted = sortvalues(deepcopy(sample), 'UTC')
    sort_values = [True, False]
    encoding_sizes = [16, 64, 91]
    for k in sort_values:
        for s in encoding_sizes:
            if k == True:
                assert sample_sorted == JSONEncoder.decode_json(JSONEncoder.encode_json(deepcopy(sample), ts_key = 'UTC', ts_value = 'Value', sort_values = k, encoding_size = s))
            else:
                encoded = JSONEncoder.encode_json(deepcopy(sample), ts_key = 'UTC', ts_value = 'Value', sort_values = k, encoding_size = s)
                decoded = JSONEncoder.decode_json(encoded)
                try:
                    assert sample == decoded
                except AssertionError:
                    print(encoded)
                    raise

def test_encode_decode_json_all_sizes_gzip():
    sample = get_sample_file()
    sample_sorted = sortvalues(deepcopy(sample), 'UTC')
    sort_values = [True, False]
    encoding_sizes = [16, 64, 91]
    for k in sort_values:
        for s in encoding_sizes:
            if k == True:
                encoded = JSONEncoder.encode_json(deepcopy(sample), ts_key = 'UTC', ts_value = 'Value', sort_values = k, encoding_size = s, gzip=True)
                decoded = JSONEncoder.decode_json(encoded, gzip=True)
                assert sample_sorted == decoded
            else:
                encoded = JSONEncoder.encode_json(deepcopy(sample), ts_key = 'UTC', ts_value = 'Value', sort_values = k, encoding_size = s, gzip=True)
                decoded = JSONEncoder.decode_json(encoded, gzip=True)
                try:
                    assert sample == decoded
                except AssertionError:
                    print(encoded)
                    raise


def test_sizes_gzip():
    sample = get_sample_file()
    sample_size = os.path.getsize('./tests/sample.json')
    sample_sorted = sortvalues(deepcopy(sample), 'UTC')
    sort_values = [True, False]
    encoding_sizes = [16, 64, 91]
    sizes = { "Raw" : sample_size }
    for k in sort_values:
        for s in encoding_sizes:
            for z in [True, False]:
                if z == True:
                    fmt = 'wb'
                else:
                    fmt = 'w'
                encoded = JSONEncoder.encode_json(deepcopy(sample), ts_key = 'UTC', ts_value = 'Value', sort_values = k, encoding_size = s, gzip=z)
                decoded = JSONEncoder.decode_json(deepcopy(encoded), gzip=z)

                with open('./tests/sztst.json', fmt) as ofile:
                    if fmt == 'w':
                        encoded = json.dumps(encoded)
                    ofile.write(encoded)
                size = os.path.getsize('./tests/sztst.json')
                os.remove('./tests/sztst.json')

                sizes[f"Sorted: {k}, Encoding_Size: {s}, Gzip: {z}"] = size
                if k == True:
                    assert sample_sorted == decoded
                else:
                    try:
                        assert sample == decoded
                    except AssertionError:
                        print(encoded)
                        raise
    for k in sizes:
        if k == "Raw":
            continue
        assert sizes[k] < sizes["Raw"]

def check_numpy_types(obj):
    if isinstance(obj, np.generic):
        return True
    elif type(obj) == dict:
        numpyFound = False
        for key in obj:
            numpyFound = numpyFound or check_numpy_types(obj[key])
        return numpyFound
    elif type(obj) == list:
        numpyFound = False
        for i, _ in enumerate(obj):
            numpyFound = numpyFound or check_numpy_types(obj[i])
        return numpyFound
    else:
        return False

def get_dict_types(obj):
    if type(obj) == dict:
        for key in obj:
            obj[key] = get_dict_types(obj[key])
        return obj
    elif type(obj) == list:
        for i, _ in enumerate(obj):
            obj[i] = get_dict_types(obj[i])
        return obj
    else:
        return type(obj)

def test_no_numpy_types():
    sample = get_sample_file()
    sample_sorted = sortvalues(deepcopy(sample), 'UTC')
    sort_values = [True, False]
    encoding_sizes = [16, 64, 91]
    for k in sort_values:
        for s in encoding_sizes:
            for z in [True, False]:
                if k == True:
                    encoded = JSONEncoder.encode_json(deepcopy(sample), ts_key = 'UTC', ts_value = 'Value', sort_values = k, encoding_size = s, gzip=z)
                    decoded = JSONEncoder.decode_json(encoded, gzip=z)
                    assert sample_sorted == decoded
                    assert check_numpy_types(decoded) == False
                else:
                    encoded = JSONEncoder.encode_json(deepcopy(sample), ts_key = 'UTC', ts_value = 'Value', sort_values = k, encoding_size = s, gzip=z)
                    decoded = JSONEncoder.decode_json(encoded, gzip=z)
                    try:
                        assert sample == decoded
                    except AssertionError:
                        print(encoded)
                        raise
                    assert check_numpy_types(decoded) == False

def test_save_best_encoding():
    encoded = JSONEncoder.encode_json(get_sample_file(), ts_key = "UTC", ts_value = "Value", sort_values = True, encoding_size=64, gzip=True)
    with open ("./tests/encoded.gzip", "wb") as ofile:
        ofile.write(encoded)
    encoded = JSONEncoder.encode_json(get_sample_file(), ts_key = "UTC", ts_value = "Value", sort_values = True, encoding_size=64, gzip=False)
    with open ("./tests/encoded.json", "w") as ofile:
        ofile.write(json.dumps(encoded, cls=NumpyEncoder))
    with open ("./tests/encoded.gzip", "rb") as ifile:
        bytes = ifile.read()
        decoded = JSONEncoder.decode_json(bytes, gzip=True)
        assert decoded == sortvalues(get_sample_file(), 'UTC')

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

def test_static_value_zero():
    sample = get_sample()
    for x, y in enumerate(sample):
        if y == "Values":
            for i, packet in enumerate(sample[y]):
                sample[y][i]["Value"] = 0.0
    encoded = JSONEncoder.encode_json(sample, ts_key="UTC", ts_value="Value", sort_values=True, encoding_size=64)
    assert "data" not in encoded["Values"]
    assert "static" in encoded["Values"]

def test_static_value_nonzero():
    sample = get_sample()
    for x, y in enumerate(sample):
        if y == "Values":
            for i, packet in enumerate(sample[y]):
                sample[y][i]["Value"] = 400.0
    encoded = JSONEncoder.encode_json(sample, ts_key="UTC", ts_value="Value", sort_values=True, encoding_size=64)
    assert "data" not in encoded["Values"]
    assert "static" in encoded["Values"]

def test_static_value_neg_nonzero():
    sample = get_sample()
    for x, y in enumerate(sample):
        if y == "Values":
            for i, packet in enumerate(sample[y]):
                sample[y][i]["Value"] = -400.0
    encoded = JSONEncoder.encode_json(sample, ts_key="UTC", ts_value="Value", sort_values=True, encoding_size=64)
    assert "data" not in encoded["Values"]
    assert "static" in encoded["Values"]




def get_encoded_sample_unsorted_base91():
    import json
    return json.loads('''{
    "AttributeName":"relative_humidity_100m:p",
    "AttributeUnitOfMeasure":"%",
    "AttributeDescription":"relative humidity at 100m [%]",
    "AttributeDataType":"Numeric",
    "Values":{
        "encoder":"TimeSeriesEncoder",
        "start":1618192800.0,
        "signed":false,
        "ts_key":"UTC",
        "ts_value":"Value",
        "encoding_depth":2,
        "encoding_size":91,
        "float_precision":1,
        "time_encoding_depth":3,
        "data":"0008M0dp860=B7`A=15}BRq6pB%C7DCF_7#CtN7!D3.7_DhY7_D@^6`EVj6JE*55jFJu5mFxG5pG7%5sGlR5{G`<6XHZc6)H.|6,INn6;I_96>JBy6!JpK6mJ~*6V1R-7.1%M7_2F,7D2tX6u33]6A3hi5#3[45U4Vt4`4*F4x5J$4V5xQ4467;4j6lb4{6`{5f7Zm5v7/85.8Nx608_J5+9B)5q9pU5V9~?5nAdf5&KdV6QK<@6MLRg6HL%26DMFr68MtD64N3!5;NhO5yN@/5hOVZ5RO)`5CPJk4{Px652Q7v58QlH5DQ`&5JRZS5PR.=5VSNd5iS-~5wTBo5*TpA5^T~z68UdL6MU<+6LVRW6LV$[6LWFh6LWt36LX3s6KXhE69X@#5|YVP5;Y):5$ZJa5tZw}5ia7l5xal75/a`w5~bZI6Eb.(6UcNT6kc->6:dBe7Gdp07ld~p7<edB8Ie<-8ofRM8uf$,8-gFX8&gs]8.h3i8>hh48^h@t8iiVF84i)$7tjJQ7Hjw;6)k7b6Xkk{6lk`m6-lZ86;l.x70mNJ7Fm-)7UnBU7,no?8Pn~f8(od19Mo<q9$pRCAJp$_ASqFNAbqs.Ajr3YAsrg^A-r@jA)sV5Afs)uACtJG9.tw%9ju7R9Huk<8=u`c8pvY|8Ov.n7}wN97xw-y7WxBK74xo*7Gx~V7Tyc@7fy<g7rzR27#z$r7;"
    }
}''')

def get_sample_file():
    import json
    with open('./tests/sample.json', 'r') as ifile:
        return json.load(ifile)

def get_sample():
    import json
    return json.loads('''{
                    "AttributeName": "relative_humidity_100m:p",
                    "AttributeUnitOfMeasure": "%",
                    "AttributeDescription": "relative humidity at 100m [%]",
                    "AttributeDataType": "Numeric",
                    "Values": [
                        {
                            "UTC": "2021-04-12T02:00:00Z",
                            "Value": 75.0
                        },
                        {
                            "UTC": "2021-04-12T03:00:00Z",
                            "Value": 73.4
                        },
                        {
                            "UTC": "2021-04-12T04:00:00Z",
                            "Value": 72.3
                        },
                        {
                            "UTC": "2021-04-13T03:00:00Z",
                            "Value": 54.2
                        },
                        {
                            "UTC": "2021-04-13T04:00:00Z",
                            "Value": 59.7
                        },
                        {
                            "UTC": "2021-04-13T05:00:00Z",
                            "Value": 65.0
                        },
                        {
                            "UTC": "2021-04-13T06:00:00Z",
                            "Value": 70.2
                        },
                        {
                            "UTC": "2021-04-13T07:00:00Z",
                            "Value": 70.1
                        },
                        {
                            "UTC": "2021-04-13T08:00:00Z",
                            "Value": 70.0
                        },
                        {
                            "UTC": "2021-04-13T09:00:00Z",
                            "Value": 70.0
                        },
                        {
                            "UTC": "2021-04-13T10:00:00Z",
                            "Value": 63.2
                        },
                        {
                            "UTC": "2021-04-13T11:00:00Z",
                            "Value": 56.5
                        },
                        {
                            "UTC": "2021-04-13T12:00:00Z",
                            "Value": 50.0
                        },
                        {
                            "UTC": "2021-04-13T13:00:00Z",
                            "Value": 50.3
                        },
                        {
                            "UTC": "2021-04-13T14:00:00Z",
                            "Value": 50.6
                        },
                        {
                            "UTC": "2021-04-13T15:00:00Z",
                            "Value": 50.9
                        },
                        {
                            "UTC": "2021-04-13T16:00:00Z",
                            "Value": 54.3
                        },
                        {
                            "UTC": "2021-04-13T17:00:00Z",
                            "Value": 57.9
                        },
                        {
                            "UTC": "2021-04-13T18:00:00Z",
                            "Value": 61.6
                        },
                        {
                            "UTC": "2021-04-13T19:00:00Z",
                            "Value": 61.9
                        },
                        {
                            "UTC": "2021-04-13T20:00:00Z",
                            "Value": 62.3
                        },
                        {
                            "UTC": "2021-04-13T21:00:00Z",
                            "Value": 62.6
                        },
                        {
                            "UTC": "2021-04-13T22:00:00Z",
                            "Value": 61.0
                        },
                        {
                            "UTC": "2021-04-13T23:00:00Z",
                            "Value": 59.4
                        },
                        {
                            "UTC": "2021-04-14T00:00:00Z",
                            "Value": 57.7
                        },
                        {
                            "UTC": "2021-04-12T05:00:00Z",
                            "Value": 71.1
                        },
                        {
                            "UTC": "2021-04-12T06:00:00Z",
                            "Value": 70.0
                        },
                        {
                            "UTC": "2021-04-12T07:00:00Z",
                            "Value": 65.0
                        },
                        {
                            "UTC": "2021-04-12T08:00:00Z",
                            "Value": 60.2
                        },
                        {
                            "UTC": "2021-04-12T09:00:00Z",
                            "Value": 55.6
                        },
                        {
                            "UTC": "2021-04-12T10:00:00Z",
                            "Value": 52.0
                        },
                        {
                            "UTC": "2021-04-12T11:00:00Z",
                            "Value": 48.5
                        },
                        {
                            "UTC": "2021-04-12T12:00:00Z",
                            "Value": 45.0
                        },
                        {
                            "UTC": "2021-04-12T13:00:00Z",
                            "Value": 42.3
                        },
                        {
                            "UTC": "2021-04-12T14:00:00Z",
                            "Value": 39.5
                        },
                        {
                            "UTC": "2021-04-12T15:00:00Z",
                            "Value": 36.8
                        },
                        {
                            "UTC": "2021-04-12T16:00:00Z",
                            "Value": 40.9
                        },
                        {
                            "UTC": "2021-04-12T17:00:00Z",
                            "Value": 45.2
                        },
                        {
                            "UTC": "2021-04-12T18:00:00Z",
                            "Value": 49.6
                        },
                        {
                            "UTC": "2021-04-12T19:00:00Z",
                            "Value": 51.2
                        },
                        {
                            "UTC": "2021-04-12T20:00:00Z",
                            "Value": 52.9
                        },
                        {
                            "UTC": "2021-04-12T21:00:00Z",
                            "Value": 54.6
                        },
                        {
                            "UTC": "2021-04-12T22:00:00Z",
                            "Value": 52.7
                        },
                        {
                            "UTC": "2021-04-12T23:00:00Z",
                            "Value": 50.7
                        },
                        {
                            "UTC": "2021-04-13T00:00:00Z",
                            "Value": 48.6
                        },
                        {
                            "UTC": "2021-04-13T01:00:00Z",
                            "Value": 50.4
                        },
                        {
                            "UTC": "2021-04-13T02:00:00Z",
                            "Value": 52.3
                        },
                        {
                            "UTC": "2021-04-14T01:00:00Z",
                            "Value": 57.2
                        },
                        {
                            "UTC": "2021-04-14T02:00:00Z",
                            "Value": 56.8
                        },
                        {
                            "UTC": "2021-04-14T03:00:00Z",
                            "Value": 56.3
                        },
                        {
                            "UTC": "2021-04-14T04:00:00Z",
                            "Value": 55.9
                        },
                        {
                            "UTC": "2021-04-14T05:00:00Z",
                            "Value": 55.4
                        },
                        {
                            "UTC": "2021-04-14T06:00:00Z",
                            "Value": 55.0
                        },
                        {
                            "UTC": "2021-04-14T07:00:00Z",
                            "Value": 53.2
                        },
                        {
                            "UTC": "2021-04-14T08:00:00Z",
                            "Value": 51.5
                        },
                        {
                            "UTC": "2021-04-14T09:00:00Z",
                            "Value": 49.8
                        },
                        {
                            "UTC": "2021-04-14T10:00:00Z",
                            "Value": 48.2
                        },
                        {
                            "UTC": "2021-04-14T11:00:00Z",
                            "Value": 46.7
                        },
                        {
                            "UTC": "2021-04-14T12:00:00Z",
                            "Value": 45.2
                        },
                        {
                            "UTC": "2021-04-14T13:00:00Z",
                            "Value": 45.7
                        },
                        {
                            "UTC": "2021-04-14T14:00:00Z",
                            "Value": 46.3
                        },
                        {
                            "UTC": "2021-04-14T15:00:00Z",
                            "Value": 46.8
                        },
                        {
                            "UTC": "2021-04-14T16:00:00Z",
                            "Value": 47.4
                        },
                        {
                            "UTC": "2021-04-14T17:00:00Z",
                            "Value": 48.0
                        },
                        {
                            "UTC": "2021-04-14T18:00:00Z",
                            "Value": 48.6
                        },
                        {
                            "UTC": "2021-04-14T19:00:00Z",
                            "Value": 49.9
                        },
                        {
                            "UTC": "2021-04-14T20:00:00Z",
                            "Value": 51.3
                        },
                        {
                            "UTC": "2021-04-14T21:00:00Z",
                            "Value": 52.6
                        },
                        {
                            "UTC": "2021-04-14T22:00:00Z",
                            "Value": 54.0
                        },
                        {
                            "UTC": "2021-04-14T23:00:00Z",
                            "Value": 55.4
                        },
                        {
                            "UTC": "2021-04-15T00:00:00Z",
                            "Value": 56.8
                        },
                        {
                            "UTC": "2021-04-15T01:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T02:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T03:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T04:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T05:00:00Z",
                            "Value": 56.7
                        },
                        {
                            "UTC": "2021-04-15T06:00:00Z",
                            "Value": 56.6
                        },
                        {
                            "UTC": "2021-04-15T07:00:00Z",
                            "Value": 55.5
                        },
                        {
                            "UTC": "2021-04-15T08:00:00Z",
                            "Value": 54.4
                        },
                        {
                            "UTC": "2021-04-15T09:00:00Z",
                            "Value": 53.2
                        },
                        {
                            "UTC": "2021-04-15T10:00:00Z",
                            "Value": 52.1
                        },
                        {
                            "UTC": "2021-04-15T11:00:00Z",
                            "Value": 51.0
                        },
                        {
                            "UTC": "2021-04-15T12:00:00Z",
                            "Value": 49.9
                        },
                        {
                            "UTC": "2021-04-15T13:00:00Z",
                            "Value": 51.4
                        },
                        {
                            "UTC": "2021-04-15T14:00:00Z",
                            "Value": 53.0
                        },
                        {
                            "UTC": "2021-04-15T15:00:00Z",
                            "Value": 54.5
                        },
                        {
                            "UTC": "2021-04-15T16:00:00Z",
                            "Value": 56.0
                        },
                        {
                            "UTC": "2021-04-15T17:00:00Z",
                            "Value": 57.6
                        },
                        {
                            "UTC": "2021-04-15T18:00:00Z",
                            "Value": 59.2
                        },
                        {
                            "UTC": "2021-04-15T19:00:00Z",
                            "Value": 62.2
                        },
                        {
                            "UTC": "2021-04-15T20:00:00Z",
                            "Value": 65.3
                        },
                        {
                            "UTC": "2021-04-15T21:00:00Z",
                            "Value": 68.4
                        },
                        {
                            "UTC": "2021-04-15T22:00:00Z",
                            "Value": 71.5
                        },
                        {
                            "UTC": "2021-04-15T23:00:00Z",
                            "Value": 74.6
                        },
                        {
                            "UTC": "2021-04-16T00:00:00Z",
                            "Value": 77.8
                        },
                        {
                            "UTC": "2021-04-16T01:00:00Z",
                            "Value": 78.4
                        },
                        {
                            "UTC": "2021-04-16T02:00:00Z",
                            "Value": 79.0
                        },
                        {
                            "UTC": "2021-04-16T03:00:00Z",
                            "Value": 79.6
                        },
                        {
                            "UTC": "2021-04-16T04:00:00Z",
                            "Value": 80.2
                        },
                        {
                            "UTC": "2021-04-16T05:00:00Z",
                            "Value": 80.8
                        },
                        {
                            "UTC": "2021-04-16T06:00:00Z",
                            "Value": 81.3
                        },
                        {
                            "UTC": "2021-04-16T07:00:00Z",
                            "Value": 77.2
                        },
                        {
                            "UTC": "2021-04-16T08:00:00Z",
                            "Value": 73.2
                        },
                        {
                            "UTC": "2021-04-16T09:00:00Z",
                            "Value": 69.2
                        },
                        {
                            "UTC": "2021-04-16T10:00:00Z",
                            "Value": 65.4
                        },
                        {
                            "UTC": "2021-04-16T11:00:00Z",
                            "Value": 61.6
                        },
                        {
                            "UTC": "2021-04-16T12:00:00Z",
                            "Value": 57.9
                        },
                        {
                            "UTC": "2021-04-16T13:00:00Z",
                            "Value": 59.3
                        },
                        {
                            "UTC": "2021-04-16T14:00:00Z",
                            "Value": 60.8
                        },
                        {
                            "UTC": "2021-04-16T15:00:00Z",
                            "Value": 62.3
                        },
                        {
                            "UTC": "2021-04-16T16:00:00Z",
                            "Value": 63.7
                        },
                        {
                            "UTC": "2021-04-16T17:00:00Z",
                            "Value": 65.2
                        },
                        {
                            "UTC": "2021-04-16T18:00:00Z",
                            "Value": 66.7
                        },
                        {
                            "UTC": "2021-04-16T19:00:00Z",
                            "Value": 71.0
                        },
                        {
                            "UTC": "2021-04-16T20:00:00Z",
                            "Value": 75.3
                        },
                        {
                            "UTC": "2021-04-16T21:00:00Z",
                            "Value": 79.7
                        },
                        {
                            "UTC": "2021-04-16T22:00:00Z",
                            "Value": 84.1
                        },
                        {
                            "UTC": "2021-04-16T23:00:00Z",
                            "Value": 88.5
                        },
                        {
                            "UTC": "2021-04-17T00:00:00Z",
                            "Value": 92.9
                        },
                        {
                            "UTC": "2021-04-17T01:00:00Z",
                            "Value": 93.8
                        },
                        {
                            "UTC": "2021-04-17T02:00:00Z",
                            "Value": 94.7
                        },
                        {
                            "UTC": "2021-04-17T03:00:00Z",
                            "Value": 95.5
                        },
                        {
                            "UTC": "2021-04-17T04:00:00Z",
                            "Value": 96.4
                        },
                        {
                            "UTC": "2021-04-17T05:00:00Z",
                            "Value": 97.2
                        },
                        {
                            "UTC": "2021-04-17T06:00:00Z",
                            "Value": 98.0
                        },
                        {
                            "UTC": "2021-04-17T07:00:00Z",
                            "Value": 95.1
                        },
                        {
                            "UTC": "2021-04-17T08:00:00Z",
                            "Value": 92.2
                        },
                        {
                            "UTC": "2021-04-17T09:00:00Z",
                            "Value": 89.3
                        },
                        {
                            "UTC": "2021-04-17T10:00:00Z",
                            "Value": 86.4
                        },
                        {
                            "UTC": "2021-04-17T11:00:00Z",
                            "Value": 83.6
                        },
                        {
                            "UTC": "2021-04-17T12:00:00Z",
                            "Value": 80.7
                        },
                        {
                            "UTC": "2021-04-17T13:00:00Z",
                            "Value": 77.9
                        },
                        {
                            "UTC": "2021-04-17T14:00:00Z",
                            "Value": 75.2
                        },
                        {
                            "UTC": "2021-04-17T15:00:00Z",
                            "Value": 72.4
                        },
                        {
                            "UTC": "2021-04-17T16:00:00Z",
                            "Value": 69.6
                        },
                        {
                            "UTC": "2021-04-17T17:00:00Z",
                            "Value": 66.9
                        },
                        {
                            "UTC": "2021-04-17T18:00:00Z",
                            "Value": 64.1
                        },
                        {
                            "UTC": "2021-04-17T19:00:00Z",
                            "Value": 65.3
                        },
                        {
                            "UTC": "2021-04-17T20:00:00Z",
                            "Value": 66.6
                        },
                        {
                            "UTC": "2021-04-17T21:00:00Z",
                            "Value": 67.8
                        },
                        {
                            "UTC": "2021-04-17T22:00:00Z",
                            "Value": 69.0
                        },
                        {
                            "UTC": "2021-04-17T23:00:00Z",
                            "Value": 70.2
                        },
                        {
                            "UTC": "2021-04-18T00:00:00Z",
                            "Value": 71.4
                        }
                    ]
                }''')