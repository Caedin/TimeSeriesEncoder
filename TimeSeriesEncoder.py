
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

    def __init__(self, timeseries, encoding_size = 64):
        # Save raw timeseries
        self.timeseries = timeseries

        # Check encoding size
        if encoding_size == 16:
            character_set = Base64NumericEncoder.get_base_16()
        elif encoding_size == 64:
            character_set = Base64NumericEncoder.get_base_64()
        elif encoding_size == 90:
            character_set = Base64NumericEncoder.get_base_90()
        else:
            raise ValueError(f'Unsupported encoding size: {encoding_size}, currently we only support base 16, 64, and 90.')

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
        
        self.encoder = Base64NumericEncoder(encoding_depth = valuebitsize, signed=signed, numeric_type=numeric_type, float_precision=maximum_precision, character_set = character_set)

        # Save raw timeseries
        self.timeseries = timeseries

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
                encoded_data = self.encoder.encode(row[1])
                encoded = encoded_time + encoded_data
                encoding += encoded
        else:
            for row in raw:
                encoded_data = self.encoder.encode(row[1])
                encoded = encoded_data
                encoding += encoded
        return encoding

    def decode(self, data):
        json_values = []
        
        if self.regular == True:
            time_index = self.start
            wordsize = self.encoder.encoding_depth
            for idx in range(0, len(data), wordsize):
                word = data[idx:idx+wordsize]
                decoded_word = self.encoder.decode(word)
                json_values.append({
                    "UTC": datetime.datetime.utcfromtimestamp(time_index).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "Value" : decoded_word
                })
                time_index += self.interval
        else:
            time_index = self.start
            wordsize = self.timeEncoder.encoding_depth + self.encoder.encoding_depth
            for idx in range(0, len(data), wordsize):
                offset = data[idx:idx+self.timeEncoder.encoding_depth]
                word = data[idx+self.timeEncoder.encoding_depth:idx+wordsize]

                decoded_offset = self.timeEncoder.decode(offset)
                decoded_word = self.encoder.decode(word)
                timestamp = decoded_offset + self.start
                json_values.append({
                    "UTC": datetime.datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%dT%H:%M:%SZ'),
                    "Value" : decoded_word
                })

        return json_values

if __name__ == '__main__':
    pass