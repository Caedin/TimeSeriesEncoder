
import ciso8601, time
from Base64NumericEncoder import Base64NumericEncoder
import numpy as np
import pandas as pd
import math
import datetime

def precision_and_scale(x):
    max_digits = 14
    int_part = int(abs(x))
    magnitude = 1 if int_part == 0 else int(math.log10(int_part)) + 1
    if magnitude >= max_digits:
        return (magnitude, 0)
    frac_part = abs(x) - int_part
    multiplier = 10 ** (max_digits - magnitude)
    frac_digits = multiplier + int(multiplier * frac_part + 0.5)
    while frac_digits % 10 == 0:
        frac_digits /= 10
    scale = int(math.log10(frac_digits))
    return (magnitude + scale, scale)

class TimeSeriesEncoder:
    regular = False

    @staticmethod
    def get_character_set(encoding_size):
        # Check encoding size
        if encoding_size == 16:
            character_set = Base64NumericEncoder.get_base_16()
        elif encoding_size == 64:
            character_set = Base64NumericEncoder.get_base_64()
        elif encoding_size == 91:
            character_set = Base64NumericEncoder.get_base_91()
        else:
            raise ValueError(f'Unsupported encoding size: {encoding_size}, currently we only support base 16, 64, and 90.')
        return character_set

    @staticmethod
    def encode_json(json_data, ts_key, ts_value, sort_values = False, encoding_size = 64):
        if type(json_data) == dict:
            for key in json_data:
                json_data[key] = TimeSeriesEncoder.encode_json(json_data[key], ts_key, ts_value, sort_values, encoding_size)
            return json_data
        elif type(json_data) == list:
            is_ts = True
            for item in json_data:
                if type(item) == dict:
                    if ts_key not in item or ts_value not in item:
                        is_ts = False
                else:
                    is_ts = False
                
            if is_ts == False:
                for i, j in enumerate(json_data):
                    json_data[i] = TimeSeriesEncoder.encode_json(j, ts_key, ts_value, sort_values, encoding_size)
            else:
                if sort_values:
                    json_data.sort(key = lambda x: x[ts_key])

                encoder = TimeSeriesEncoder(json_data, encoding_size = encoding_size)

                # Add encoded information to the json
                json_data = {
                    "encoder" : "TimeSeriesEncoder",
                    "start" : encoder.start,
                    "ts_key": ts_key,
                    "ts_value": ts_value,
                    "encoding_size": encoding_size,
                    "data" : encoder.encode(json_data)
                }

                # Add encoding metadata for decoding later
                if encoder.regular:
                    json_data['interval'] = encoder.interval
                else:
                    json_data['time_encoding_depth'] = encoder.timeEncoder.encoding_depth
                
                if encoder.static is not None:
                    json_data['static_value'] = encoder.static['value']
                    json_data['static_count'] = encoder.static['count']
                    
                    if encoder.regular:
                        del json_data['data']
                        del json_data['encoding_size']
                else:
                    json_data["encoding_depth"] = encoder.encoder.encoding_depth
                    json_data["float_precision"] = encoder.encoder.float_precision
                    json_data["signed"] = encoder.encoder.signed
                
            return json_data
        else:
            return json_data

    @staticmethod
    def decode_json(json_data):
        if type(json_data) != dict:
            if type(json_data) == list:
                for i, j in enumerate(json_data):
                    json_data[i] = TimeSeriesEncoder.decode_json(j)
            return json_data
        else:
            encoded_ts = False
            if 'encoder' in json_data:
                if json_data['encoder'] == 'TimeSeriesEncoder':
                    encoded_ts = True
                    
            if encoded_ts == False:
                for k in json_data:
                    json_data[k] = TimeSeriesEncoder.decode_json(json_data[k])
                return json_data
            else:
                encoder = TimeSeriesEncoder()
                encoder.start = json_data['start']
                encoder.ts_key = json_data['ts_key']
                encoder.ts_value = json_data['ts_value']

                if 'static_value' not in json_data:
                    character_set = TimeSeriesEncoder.get_character_set(json_data['encoding_size'])
                    encoder.signed = json_data['signed']
                    if json_data['float_precision'] == 0:
                        numeric_type = int
                    else:
                        numeric_type = float

                    encoder.encoder = Base64NumericEncoder(encoding_depth = json_data['encoding_depth'], signed=json_data['signed'], numeric_type=numeric_type, float_precision=json_data['float_precision'], character_set = character_set)
                else:
                    encoder.static = { 'value' : json_data['static_value'], 'count' : json_data['static_count']}

                if 'time_encoding_depth' in json_data:
                    character_set = TimeSeriesEncoder.get_character_set(json_data['encoding_size'])
                    encoder.timeEncoder = Base64NumericEncoder(encoding_depth = json_data['time_encoding_depth'], signed=False, numeric_type=int, character_set = character_set)
                    encoder.regular = False
                else:
                    encoder.regular = True
                    encoder.interval = json_data['interval']

                if 'data' in json_data:
                    json_data = encoder.decode(json_data['data'])
                else:
                    json_data = encoder.decode()
                return json_data


    def __init__(self, timeseries = None, encoding_size = 64):
        # Save raw timeseries
        self.timeseries = timeseries
        self.encoding_size = encoding_size
        self.ts_key = 'UTC'
        self.ts_value = 'Value'
        self.static = None

        if timeseries is not None:
            # Check encoding size
            character_set = TimeSeriesEncoder.get_character_set(encoding_size)

            # Create the optimal encoder
            self.np_timeseries = self.get_np_timeseries(timeseries)
            self.start = np.min(self.np_timeseries[0, 0])

            # Determine regularity of data
            gaps = np.diff(self.np_timeseries[:, 0], axis=0)
            if np.all(gaps == gaps[0]):
                # Series is regular
                self.regular = True
                self.interval = gaps[0]
            else:
                self.regular = False
                offsets = self.np_timeseries[:, 0] - self.start
                largest_offset = np.max(offsets)

                timebitsize = 0
                while largest_offset >= 1:
                    largest_offset /= encoding_size
                    timebitsize += 1

            # Determine value bounds
            values = self.np_timeseries[:, 1]
            max_value = np.max(values)
            min_value = np.min(values)

            # Determine data precision
            precision = np.vectorize(precision_and_scale)
            _, values = precision(values)
            maximum_precision = np.max(values)

            max_value = max(abs(max_value), abs(min_value))

            signed = False
            if min_value < 0:
                signed = True
                max_value *= 2

            if maximum_precision == 0:
                numeric_type = int
            else:
                numeric_type = float
                max_value *= 10 ** maximum_precision

            valuebitsize = 0
            while max_value >= 1:
                max_value /= encoding_size
                valuebitsize += 1

            # Create encoders
            if self.regular == False:
                self.timeEncoder = Base64NumericEncoder(encoding_depth = timebitsize, signed=False, numeric_type=int, character_set = character_set)

            if valuebitsize != 0:
                self.encoder = Base64NumericEncoder(encoding_depth = valuebitsize, signed=signed, numeric_type=numeric_type, float_precision=maximum_precision, character_set = character_set)
            else:
                self.static = {}
                self.static['value'] = max_value
                self.static['count'] = self.np_timeseries.shape[0]

    def get_np_timeseries(self, timeseries):
        raw = np.zeros((len(timeseries), 2))
        for i, k in enumerate(timeseries):
            unix_time = ciso8601.parse_datetime(k['UTC']).timestamp()
            raw[i][0] = int(unix_time)
            raw[i][1] = float(k['Value'])
        return raw

    def encode(self, timeseries):
        encoding = ''
        raw = self.get_np_timeseries(timeseries)

        if self.regular == False:
            data = raw.copy()
            data[:, 0] = data[:, 0] - self.start

            for row in data:
                encoded_time = self.timeEncoder.encode(row[0])
                if self.static is None:
                    encoded_data = self.encoder.encode(row[1])
                else:
                    encoded_data =  ''

                encoded = encoded_time + encoded_data
                encoding += encoded
        else:
            for row in raw:
                if self.static is None:
                    encoded_data = self.encoder.encode(row[1])
                else:
                    encoded_data =  ''
                encoded = encoded_data
                encoding += encoded
        return encoding

    def decode(self, data = None):
        json_values = []
        
        if self.regular == True:
            time_index = self.start
            if self.static is None:
                wordsize = self.encoder.encoding_depth
                for idx in range(0, len(data), wordsize):
                    word = data[idx:idx+wordsize]
                    decoded_word = self.encoder.decode(word)
                    json_values.append({
                        self.ts_key: datetime.datetime.utcfromtimestamp(time_index).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        self.ts_value : decoded_word
                    })
                    time_index += self.interval
            else:
                for d in range(0, self.static['count']):
                    json_values.append({
                        self.ts_key: datetime.datetime.utcfromtimestamp(time_index).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        self.ts_value : self.static['value']
                    })
                    time_index += self.interval
        else:
            time_index = self.start
            if self.static is None:
                wordsize = self.timeEncoder.encoding_depth + self.encoder.encoding_depth
                for idx in range(0, len(data), wordsize):
                    offset = data[idx:idx+self.timeEncoder.encoding_depth]
                    word = data[idx+self.timeEncoder.encoding_depth:idx+wordsize]

                    decoded_offset = self.timeEncoder.decode(offset)
                    decoded_word = self.encoder.decode(word)
                    timestamp = decoded_offset + self.start
                    json_values.append({
                        self.ts_key: datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        self.ts_value : decoded_word
                    })
            else:
                wordsize = self.timeEncoder.encoding_depth
                for idx in range(0, len(data), wordsize):
                    offset = data[idx:idx+wordsize]
                    decoded_offset = self.timeEncoder.decode(offset)
                    timestamp = decoded_offset + self.start
                    json_values.append({
                        self.ts_key: datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ'),
                        self.ts_value : self.static['value']
                    })

        return json_values

if __name__ == '__main__':
    pass