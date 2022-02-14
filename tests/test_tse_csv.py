from gc import get_count
import hashlib
from io import StringIO
import json
import numpy as np
import pandas as pd
from src.timeseriesencoder import CSVEncoder

def test_encode_keys():
    csv = get_csv_sample()
    df = pd.read_csv(StringIO(csv))
    key_columns = ["Attribute"]
    enc = CSVEncoder()
    encoded_keys = enc.encode_keys(df, key_columns=key_columns)
    assert encoded_keys.shape == (9143, 1)

def test_encode_test():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
    with open("./tests/encoded_csv.json", 'w') as ofile:
        ofile.write(encoded)
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"], gzip=True)
    with open("./tests/encoded_csv.gzip", 'wb') as ofile:
        ofile.write(encoded)

def test_decode_csv():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
    # print(encoded)
    decoded = CSVEncoder.decode_csv(encoded)
    # print(decoded)

def test_decode_word_size():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"], functional_compression=True)
    json_data = json.loads(encoded)
    enc = CSVEncoder()
    ws = enc.decode_calculate_token_size(json_data)
    assert np.sum(ws) == 4

def test_decode_tokenize():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
    json_data = json.loads(encoded)
    decoder = CSVEncoder(encoding_size=64)
    time_size, key_size, value_size = decoder.decode_calculate_token_size(json_data)
    data = json_data["data"]
    times, keys, values = decoder.tokenize(data, time_size, key_size, value_size)
    assert len(times) == len(keys)
    assert len(keys) == len(values)


def test_decode_time():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
    json_data = json.loads(encoded)
    decoder = CSVEncoder(encoding_size=64)
    time_size, key_size, value_size = decoder.decode_calculate_token_size(json_data)
    data = json_data["data"]
    times, keys, values = decoder.tokenize(data, time_size, key_size, value_size)
    times = decoder.decode_time(json_data, times)

def test_decode_keys():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
    json_data = json.loads(encoded)
    decoder = CSVEncoder(encoding_size=64)
    time_size, key_size, value_size = decoder.decode_calculate_token_size(json_data)
    data = json_data["data"]
    times, keys, values = decoder.tokenize(data, time_size, key_size, value_size)
    keys = decoder.decode_key(json_data, keys)
    assert "Attribute" in keys.columns
    assert keys.shape == (9143, 1)

def test_decode_values():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
    json_data = json.loads(encoded)
    decoder = CSVEncoder(encoding_size=64)
    time_size, key_size, value_size = decoder.decode_calculate_token_size(json_data)
    data = json_data["data"]
    times, keys, values = decoder.tokenize(data, time_size, key_size, value_size)
    decoder.decode_time(json_data, times)
    values = decoder.decode_values(json_data, values)
    assert np.all(set(values.columns) == set(["AsOfDateUTC", "AverageNumericValue", "ForecastHorizonHour"]))
    assert values.shape == (9143, 3)

def test_encode_decode_nogzip():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"], sort_values=False)
    with open('./tests/test.json', 'w') as ofile:
        ofile.write(encoded) 
    decoded = CSVEncoder.decode_csv(encoded)
    assert csv == decoded
    m = hashlib.sha256()
    m.update(csv.encode("utf-8"))
    encoded_hash = m.hexdigest()

    k = hashlib.sha256()
    k.update(decoded.encode("utf-8"))
    decoded_hash = k.hexdigest()
    assert encoded_hash == decoded_hash

def test_encode_sample2_decode_nogzip():
    csv = get_csv_sample2()
    encoded = CSVEncoder.encode_csv(csv, time_column="date", key_columns=["ent_code", "tag"], sort_values=False)
    with open('./tests/test.json', 'w') as ofile:
        ofile.write(encoded) 
    decoded = CSVEncoder.decode_csv(encoded)
    with open('./tests/test.csv', 'w') as ofile:
        ofile.write(decoded) 
        
    m = hashlib.sha256()
    m.update(csv.encode("utf-8"))
    encoded_hash = m.hexdigest()

    k = hashlib.sha256()
    k.update(decoded.encode("utf-8"))
    decoded_hash = k.hexdigest()
    assert encoded_hash == decoded_hash

def test_encode_decode_gzip():
    csv = get_csv_sample()
    encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"], sort_values=False, gzip=True)
    with open('./tests/test.gzip', 'wb') as ofile:
        ofile.write(encoded) 
    decoded = CSVEncoder.decode_csv(encoded, gzip=True)
    assert csv == decoded
    m = hashlib.sha256()
    m.update(csv.encode("utf-8"))
    encoded_hash = m.hexdigest()

    k = hashlib.sha256()
    k.update(decoded.encode("utf-8"))
    decoded_hash = k.hexdigest()
    assert encoded_hash == decoded_hash


def get_count_of_key(obj, key):
    if type(obj) == dict:
        n = 0
        for k in obj:
            if k == key:
                n += 1
            else:
                n += get_count_of_key(obj[k], key)
        return n
    elif type(obj) == list:
        n = 0
        for i, _ in enumerate(obj):
            n += get_count_of_key(obj[i], key)
        return n
    else:
        return 0
    

def get_csv_sample():
    with open("./tests/bebez.csv", 'r') as ifile:
        return ifile.read()

def get_csv_sample2():
    with open("./tests/export-3.csv", 'r') as ifile:
        return ifile.read()


def get_json_file():
    import json
    with open('./tests/sample.json', 'r') as ifile:
        return json.load(ifile)


def get_csv_random_sample():
    df = pd.read_csv("./tests/bebez.csv")
    df = df.sample(frac=1, axis=0)
    return df.to_csv(index=False)