A module for encoding timeseries data, with helper functions for parsing JSON and CSV files into smaller sizes for caching and transmitting through APIs.

# Installation
```
pip install timeseriesencoder
```

# Use
## JSON
To use pass any json into TimeSeriesEncoder.encode_json(data, ts_key, ts_value) where ts_key and ts_value are the timestamp key and the value key in the json.

```python
from timeseriesencoder import *
encoded = JSONEncoder.encode_json(myJson, ts_key='UTC', ts_value='Value')
```

To decode you can apply the reverse:
```python
decoded = JSONEncoder.decode_json(encoded)
```

The encoder will encode all time series it finds in the json or csv file. Each will get their own encoding that is optimal for the data sparsity and values. Sorting the data before encoding can improve compression. If you'd like the encoder to sort for you, you can include sort_values = True on the encode_json call. This will sort each time series by the timeseries key before encoding.

## CSV
```python
from timeseriesencoder import *
csv = get_csv_sample()
encoded = CSVEncoder.encode_csv(csv, time_column="UTC", key_columns=["Attribute"])
```

To decode you can apply the reverse:
```python
decoded = CSVEncoder.decode_csv(encoded)
```

Additionally, non time series data will be encoded in CSV files as able. Static columns will be compressed, and string value columns will be replaced with encoded lookups if it saves space in the encoded file size. 

# Updates

## 0.2.0 

    - Released a csv module that allows encoding of CSV time series files, it is accessible on CSVEncoder.
    - Migrated JSON function from TimeSeriesEncoder to JSONEncoder, which extends TimeSeriesEncoder
    - Fixed a few bugs, added more tests

## 0.1.17

    - Added gzip compression as an optional output for all encoding and decoding calls
    - Added tests for gzip


# Tests
To run tests call pytests on the tests folder from the base package folder.
```
pytest ./tests/ -v -s
```

![image](https://user-images.githubusercontent.com/8877753/115096228-d00ccb00-9ee9-11eb-815a-8d837ffc66f3.png)


# Examples
Example of encoding a json file, with the inputs/outputs below.

*Note: The numpyencoder module is not required, but is used in the example to read/write the json to a file easily.*
```python
from timeseriesencoder import *
import json
from numpyencoder import NumpyEncoder

with open('sample.json', 'r') as rfile:
    data = json.load(rfile)

data['Response'][0]['ForecastWeather'] = data['Response'][0]['ForecastWeather'][:3]

with open('data.json', 'w') as rfile:
    json.dump(data, rfile, cls=NumpyEncoder)

encoded = TimeSeriesEncoder.encode_json(data, ts_key='UTC', ts_value='Value', sort_values=True)

with open('encoded.json', 'w') as rfile:
    json.dump(encoded, rfile, cls=NumpyEncoder)
```

# Size

Size before and after encoding. Encoding reduced package size by 10x.

![image](https://user-images.githubusercontent.com/8877753/115103478-d023bf80-9f17-11eb-9681-b03835097da1.png)

In 0.1.17 the optional gzip parameter was added to encode_json and decode_json. This allows the final package to be smaller, which allows for lower data size for sending across networks, or storing in a cache system like Redis.

![image](https://user-images.githubusercontent.com/8877753/151123735-66a13683-3319-4ba8-89c5-303a888da40d.jpeg)

The raw sample.json had a size of 281KB. 
The encoded json that is output from the program that is sorted and is using base64 style encoding is 27KB. 
The raw zipped sample.json is 26KB
The programs gzipped, encoded file is just 8KB. This is 1/3rd the size of the regular zip file, and just 1/35th of the original data size.

Data
Output
```json
{
	"Request": {
		"locations": [
			"WIT_BEBEZ_SS001_WT001"
		],
		"attributes": null,
		"aggregate": true,
		"startDate": "2021-04-12T01:46:08.8622635Z"
	},
	"Response": [
		{
			"LocationName": "WIT_BEBEZ_SS001_WT001",
			"EntityType": "WIND_TURBINE",
			"DisplayName": "BEZ_E01",
			"Latitude": 50.82426,
			"Longitude": 3.32744,
			"Timezone": "Europe/Brussels",
			"PlanId": "14d14980-306a-40c8-a784-579022ec9d49",
			"HistoricalPlanId": "0d0fb8b5-a00b-4546-925f-0a7e7b72503b",
			"DataSource": "ECMWF-IFS",
			"AsOfDateUTC": "2021-04-08T00:00:00Z",
			"ForecastWeather": [
				{
					"AttributeName": "fresh_snow_6h:cm",
					"AttributeUnitOfMeasure": "cm",
					"AttributeDescription": "fresh snow of previous 6h [cm]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"static": {
							"value": 0.0,
							"count": 143
						},
						"encoding_start": 1618192800.0,
						"interval": 3600.0
					}
				},
				{
					"AttributeName": "precip_1h:mm",
					"AttributeUnitOfMeasure": "mm",
					"AttributeDescription": "amount of precipitation in the previous 1h [mm]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 1,
							"float_precision": 2
						},
						"data": "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000KKKKKK888888TTTTTT888888000000"
					}
				},
				{
					"AttributeName": "relative_humidity_100m:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "relative humidity at 100m [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "BkBUBJB7AyAA9Q8i887b726d6B5m6P747m808H8Y8F7x7c7u8B8U9LAAA-AzAyAy9u8r7q7t7w7z8V939e9h9l9o9Y9I918y8u8p8l8g8c8K837o7Y7J74797F7K7Q7W7c7p818E8S8g8u8t8t8t8t8t8s8h8W8K897-7p828I8X8m909G9kADAiBBBgCACGCMCSCYCeCjC4BSAqAE9e939H9W9l9zACARB6BnCTD9DrEXEgEpExF4FCFKEtEQDzDWD4CdCBBmBKAuATA1ADAQAcAoA-BA"
					}
				},
				{
					"AttributeName": "relative_humidity_50m:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "relative humidity at 50m [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "CDB-BrBhBYAT9U8b837Z736g6H5v6b7K878X8z9Q9K9C929H9X9nALAtBLB6AuAh9h8j7o7q7t7v8c9NABALAVAfAZATAMAEA79_9t9m9e998h8G7r7T757D7L7T7c7k7t848H8U8h8u9695949291908-8o8b8P8D817s888Q8i8_9I9bA3AXB0BVB_CWCaCeChClCoCsCABVAsAE9d929J9a9rA7AQAiBKByCaDEDuEZEhEqEyF5FDFLEwEWE6DjDJCwCSB-BWB3AdAAALAWAhAsB1BC"
					}
				},
				{
					"AttributeName": "t_100m:C",
					"AttributeUnitOfMeasure": "\u00b0C",
					"AttributeDescription": "temperature at 100m [C]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0R0S0S0S0S0Y0d0j0o0s0x0z0_110z0u0q0n0j0f0d0b0Z0Y0X0W0Z0c0e0m0u0_1A1K1U1W1X1Z1W1S1P1N1K1H1F1D1A181613110_0z131A1H1N1U1b1c1d1e1f1g1h1a1T1M1E17100z0w0t0q0n0k0y191M1a1n1_2225282C2F2I2C26201x1r1l1k1k1j1j1i1h1t232F2R2d2p2q2q2r2s2s2t2l2e2W2O2H292623201z1x1u1w1y1-212325221_1y1u1r1o1n1l1k1j1i1h"
					}
				},
				{
					"AttributeName": "wind_dir_100m:d",
					"AttributeUnitOfMeasure": "\u00b0",
					"AttributeDescription": "wind direction at 100m",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "1V0x0s0m0f1I1s2L1Q0RtduC0Z1C0s0Y0D0l1c3CsfnGjtfBbFYqY1XMWnX9XgYRZbbDdPcscGbeiH0T3IB1GyJLL4MpOPOfOtP5PHPSPdP2ORNoN9MVLrLGKlKHJrJTJ7JvKfLLL-MZN5MzMqMiMZMQMHMpNOO1OjPUQIQUQhQvR8RORfRPRAQ-QpQfQWQLQ9PzPnPaPNPdPvQEQdR3RaQyQLPmPEOkOGPXQlRuSxTsUfUXUOUEU4TvTjUjW1XlZucIefebeYeUeReOeMcvblaqa5ZVZ0"
					}
				},
				{
					"AttributeName": "wind_dir_120m:d",
					"AttributeUnitOfMeasure": "\u00b0",
					"AttributeDescription": "wind direction at 120m",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "1f15110y0t1Q1w2M1R0RteuD0b1E0u0Z0F0n1f3MsWn8jsfObdZEYQXjX7XQXrYUZebFdScvcJbhh-023DBVHOJfLLN0OYOnO_PBPNPYPiP7OWNtNDMXLrLGKlKHJtJVJ9JyKiLPM2MeNAN2MwMoMgMXMPMvNSO3OlPUQIQUQkQzRDRTRlRVRIR5QxQnQfQTQIQ6PwPjPWPlQ0QJQgR5RaQzQOPqPJOqONPeQsR_T1TyUlUdUUULUBU1TsUtWBXtZzcKeeebeYeVeSePeNcxboata8ZXZ2"
					}
				},
				{
					"AttributeName": "wind_dir_80m:d",
					"AttributeUnitOfMeasure": "\u00b0",
					"AttributeDescription": "wind direction at 80m",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "150T0G02u20u1i2K1P0PtcuC0b1F0v0Y090n1j3GsZmbj6ecaZXwXEWgWBWkXRYLZYbBdOcscHbfhq0M3PAgGUI_KiMQO3OLOaOpP0PCPOOoOCNbM_MQLqLHKmKHJqJQJ0JpKYLELsMRMzMqMhMYMPMHM8MjNLN_OjPUQHQQQaQkQvR5RHR2QsQgQWQNQGQ4PuPiPVPIP5PPPlQ7QYR1RZQxQJPiP5OVNvPEQVRgSiTdUQUHU8T_TqTfTTUYVzXmZycKeceXeSeNeJeFeBckbaagZyZNYv"
					}
				},
				{
					"AttributeName": "wind_gusts_100m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "wind gusts at 100m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "1N1H1D1813120_0_0z0y0w0v0t0s0t0u0v0l0b0R0T0V0W0c0h0m0q0u0y0q0i0a0W0S0O0O0N0N0P0R0T0b0i0q0r0s0t0v0x0z0_111513121110100_141A1G1M1S1Z1i1s202A2K2U2R2O2L2I2F2C221t1j1Y1S1M1L1K1J1I1H1F1G1H1I1K1O1T1S1Q1P1O1M1L1G1F1G1H1I1I1H1G1F1F1F1G1K1N1S1W1b1g1W1M1D1A1815110z0v0r0n0o0u0-151D1K1R1c1j1p1w2027"
					}
				},
				{
					"AttributeName": "wind_gusts_80m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "wind gusts at 80m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "1L1F1A1611110_100_0z0x0w0u0t0s0r0q0i0a0S0T0V0X0b0f0j0n0q0u0o0i0b0X0T0P0P0O0N0P0R0S0Z0f0m0m0n0n0p0r0u0y111512100_0_101014191F1L1R1X1h1q1-282I2S2P2M2J2G2D2A201s1i1Y1S1N1L1K1I1H1F1D1E1E1F1H1J1L1K1J1I1H1H1H1E1E1F1G1H1H1G1F1D1D1D1E1I1L1Q1V1a1e1V1L1B1614110-0w0t0p0n0o0u0-141B1I1P1Z1h1o1u1-25"
					}
				},
				{
					"AttributeName": "wind_speed_100m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "wind speed at 100m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0t0q0m0j0f0i0k0n0m0k0j0i0h0g0g0h0i0a0R0J0L0M0O0S0W0a0e0h0k0e0X0R0O0K0H0G0G0F0H0J0L0R0X0e0e0f0g0i0j0l0n0p0q0q0p0p0o0n0n0q0t0w0y0_1215181B1E1H1K1J1J1J1I1I1I1F1B1815120_0z0x0v0t0r0p0t0x0-12161A1918171514130_0x0t0p0l0h0i0k0l0n0o0q0s0v0x0-1013110_0z0x0u0s0p0m0i0f0b0Y0a0b0c0e0f0h0n0u0-151B1I"
					}
				},
				{
					"AttributeName": "wind_speed_120m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "wind speed at 120m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0w0t0p0k0g0j0l0o0m0l0j0i0h0g0h0i0j0a0R0J0L0M0O0S0W0a0d0h0k0e0X0R0O0K0H0G0G0F0H0I0K0Q0X0d0e0f0g0i0k0m0o0q0s0s0r0q0p0o0n0q0u0x0-1114181B1E1H1K1O1N1N1N1M1M1L1I1E1B17130_0z0x0w0u0s0q0t0x0_13161A191817161514100y0u0p0l0h0j0k0m0n0p0q0t0w0y0_1214120_0z0x0u0s0p0l0i0f0c0Z0a0c0e0f0h0i0p0v10161D1J"
					}
				},
				{
					"AttributeName": "wind_speed_80m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "wind speed at 80m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0o0l0i0e0b0g0k0o0n0l0k0j0i0g0g0f0e0X0Q0K0L0N0O0R0U0Y0b0e0h0c0X0S0O0L0I0H0G0G0H0J0K0Q0V0a0b0b0c0d0f0h0j0k0m0m0n0n0n0o0o0q0s0u0w0y0-101316191C1E1E1E1E1E1E1D1B19171412100z0w0t0q0n0k0o0r0v0y1014131211100_0_0x0u0r0o0l0h0i0j0j0k0k0l0o0q0t0w0y0_0z0x0v0t0r0p0m0j0g0d0b0Y0Z0a0b0c0d0e0k0r0x11181E"
					}
				},
				{
					"AttributeName": "direct_rad:W",
					"AttributeUnitOfMeasure": " W/m\u00b2",
					"AttributeDescription": "direct radiation [W]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 3,
							"float_precision": 1
						},
						"data": "0000000000000780LI0XF0be0a80Wm0TQ0O90Ox0SX0Pd0E902h00000000000000000000000000000000007J0PE0jI0x_16I14b0sG0af0Pm0Kl0ER06j01600000000000000000000000000000000008d0Qq0mw17n1Lr1UF1WJ1Rs1HG11L0fl0J-04200000000000000000000000000000000006M0JD0Yn0ot0-p17B1B219q13K0tp0YK0Fk03600000000000000000000000000000000001P04Z08s0Dk0Hw0LM0NY0O80Ms0Jd0D306d01X00000000000000000000000000000000001e04l08X0CU0Er0GG0Gc0Fs0E30BN09d06501m000000000000000000"
					}
				},
				{
					"AttributeName": "global_rad:W",
					"AttributeUnitOfMeasure": " W/m\u00b2",
					"AttributeDescription": "global radiation [W]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 3,
							"float_precision": 1
						},
						"data": "0000000000000Db0ab0uE16G1Cy1Ea1CI14v10b0yT0lo0SB06e0000000000000000000000000000000000Dd0cg0_E1Iw1W61Xw1O018R0xC0lw0XW0IQ04M0000000000000000000000000000000000Fo0gz1571P_1hX1rw1uN1oj1bN1HR0wn0V-07Q0000000000000000000000000000000000Df0Ze0u417i1Nc1YJ1ch1a71QY1AT0qN0Rz06a0000000000000000000000000000000070990N20Zb0ir0tr0_q13t13K0zw0po0cB0LS05S00000000000000000000000000000000K0AJ0P70cH0ll0sb0vN0u60pD0hL0XM0ST0I505E000000000000000000"
					}
				},
				{
					"AttributeName": "relative_humidity_2m:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "relative humidity at 2m [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "DND9D4C_CwB99e8M7v7T736m6T6B6-7u8w9lAgBgC9CgDCDLDTDcD5CaC7BPAlA89G8S7k7l7m7o8sA3BRBsCJCmD8DXDwDfDOD7CtCcCMBEAD9J8V7n767K7Y7m7_8E8U8f8r919D9Q9d9Z9V9R9O9K9G908n8Y8L877x8I8h949V9wANApBGBlCFCmDKDHDEDCD9D7D4CIBZAuAG9h989U9rADAcB0BQBvCQCyDVE4EhEnEtEzF4FAFGExEcEID-DhDPCuCNBuBQAzAWAfAnAvB2BABJ"
					}
				},
				{
					"AttributeName": "wind_dir_10m:d",
					"AttributeUnitOfMeasure": "\u00b0",
					"AttributeDescription": "wind direction at 10m",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "tvt7sTrnr1tk1A2G1L0LtYuC0f1O120au90u233UsCkGgQceYBUmUUUFU2VFWbY2ZLb4dLcscKbkgGuE3p9QErHoJNL5MrNDNZNrO6OKOXNvNMMuMTM6LnLJKqKJJnJEIhJSKAKqLRL-MUMKMBM2LuLlLcMNN9NyOkPUQDQCQAQ8Q5Q2PzPqPjPcPWPRPNP9OxOkOWOIO5OcP9PkQJQvRWQvQEPSOcNgMfOCPcQsRwSpTZTRTIT8S-SpSeT-ViXpa9cReQeHe8e0dtdkdbc5aya5ZRYvYV"
					}
				},
				{
					"AttributeName": "t_2m:F",
					"AttributeUnitOfMeasure": "\u00b0F",
					"AttributeDescription": "temperature at 2m [F]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "5P5Q5R5R5S5u6L6o6w737C7D7E7E6z6j6S675n5S5D4z4k4f4b4X4m4_5F5x6c7I7b7t898A8B8C7y7j7T7C6w6e6Q6C5-5y5v5s5q5n5k6B6e747X7z8Q8L8G8B86817y7k7X7J756u6g6e6b6Z6W6T6R6t7J7m8C8e949493939292918r8e8S8F837t7v7x7z7_82848T8s9F9eA0APAMAIAEABA7A39t9h9V9J978x8s8n8i8c8X8S8Y8e8k8q8w8_8v8o8i8b8U8O8L8I8F8C8986"
					}
				},
				{
					"AttributeName": "prob_rr_3h:p",
					"AttributeUnitOfMeasure": "mm",
					"AttributeDescription": "probability of amount of precipitation in the previous 3h [mm]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A0A1E2F3C3G3K3O2p281O1I1D1822344B4b4_5N4Q3D1g1Y1Q1I0t0W0A0A0A0A"
					}
				},
				{
					"AttributeName": "dew_point_2m:C",
					"AttributeUnitOfMeasure": "\u00b0C",
					"AttributeDescription": "[MET] dew point temperature at 2m height [C]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1,
							"signed": true
						},
						"data": "VuVtVsVsVrVnViVdVaVXVUVPVJVEVLVTVbVcVdVdVbVYVVVUVTVSVVVYVbVrW4WJWGWDWAWBWBWCWMWWWgWcWXWTWPWMWIWEWAW6W1VzVvVxV-W0W2W4W7W8WAWBWDWEWGWCW7W3V_VxVtVrVoVmVkViVfVrW0WBWMWXWiWoWuW-X5XBXHXGXGXFXFXEXEXEXFXGXHXHXIXNXRXVXaXeXiXmXqXuXxX_Y3Y3Y2Y2Y2Y2Y2Y0X-XyXwXuXtXtXtXtXsXsXsXjXZXQXGX7WzWzWzW-W-W-W-"
					}
				},
				{
					"AttributeName": "diffuse_rad:W",
					"AttributeUnitOfMeasure": " W/m\u00b2",
					"AttributeDescription": "[MET] diffuse radiation [W]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "000000006TFJN0WeeqjqkvimdgVyMBE23y00000000000000000000006KDSHyMxPqTKXmZoXSRBJ5Bi3G00000000000000000000007BGAKDIELhNhO5MsK7G5H2C03O00000000000000000000007JGQLIKrOpR8RfQJNEIgI3CF3U00000000000000000000077mIVQlV7bxgViLhDd4WAP8Er3x000000000000000000000K8gKOTmZHdmf7dWZNTHL_IrC03U000000000000"
					}
				},
				{
					"AttributeName": "effective_cloud_cover:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "[MET] effective cloud cover [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "7N7d7d7d7dAfC-EbDhCkBjA68E644F2F050402000001013E638X8R8b8-71502y8ICBEdEwF9FKFJFIFJEJCmAhBnD6EfDVCCAm9A7S5Z5E4u4Y4B3q3T2_2W221Z150c1i2n3t4y62778eA6BYCxEIFcENCnAr8Y5u2v4o6i8dAXCQEHCiBOAJ9T8s8T9fAqC0DCEOFaFXFUFRFOFLFIEODaCsCFBkBKBUBgBuC9CRCmBxB7AK9a8s8B9XAqC4DIEUFdEjDfCVBIA58xAABHCGD7DtEU"
					}
				},
				{
					"AttributeName": "snow_depth:cm",
					"AttributeUnitOfMeasure": "cm",
					"AttributeDescription": "[MET] snow depth  [cm]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"static": {
							"value": 0.0,
							"count": 143
						},
						"encoding_start": 1618192800.0,
						"interval": 3600.0
					}
				},
				{
					"AttributeName": "sfc_pressure:hPa",
					"AttributeUnitOfMeasure": "hPa",
					"AttributeDescription": "[MET] surface preasure [hPa]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 3,
							"float_precision": 1
						},
						"data": "2Vt2Vw2W02W62WB2WG2WK2WP2WP2WP2WP2WP2WO2WO2WR2WV2WY2Wd2Wh2Wm2Wm2Wm2Wm2Wm2Wm2Wm2Wo2Wq2Ws2Wt2Wt2Wt2Wq2Wn2Wj2Wg2Wc2WZ2WY2WX2WW2WY2Wa2Wc2Wa2WX2WV2WT2WR2WO2WM2WK2WI2WD2W82W32V-2Vv2Vq2Vk2Vd2VW2VQ2VJ2VC2VA2V72V42V12U_2Uy2Uu2Uq2Um2Uj2Uf2Ub2UY2UV2US2UP2UM2UJ2UH2UF2UD2UC2UA2U82U72U72U62U62U52U52U42U32U22U12U02T_2T-2Ty2Tx2Tv2Tu2Ts2Tq2To2Tm2Tk2Ti2Tg2Th2Tj2Tk2Tl2Tn2To2To2To2Tn2Tn2Tn2Tn2Tm2Tl2Tk2Tj2Ti2Th2Tl2To2Tr2Tu2Tx2T-2U02U12U32U42U62U7"
					}
				},
				{
					"AttributeName": "total_cloud_cover:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "[MET] total cloud cover [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "7N7d7d7d7dAfC-EbDhCkBjA68E644F2F050402000001013E638X8R8b8-71502y8ICBEdF2FMFaFbFcFdFaFXFVFXFZFcFLEqE2D1BkAA9f978b827U6w5z5043372A1D3O5Z7k9vC4EFEgF0FIFUFbFeFHECCR9z6n2v597J9MBGD1EbDdD5C_DJE0F5FBFHFNFSFYFeFdFdFcFcFbFaFRFJFCF6F2E-EgEREFE7E4E4DuDqDxEFEmFXFYFaFbFcFdFeFNEeDYCAAb8xAABHCGD7DtEU"
					}
				},
				{
					"AttributeName": "visibility:km",
					"AttributeUnitOfMeasure": "km",
					"AttributeDescription": "[MET] visibility [km]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "4B4I4N4S4X4s5B5V5h5t626M6f6z6X655f5R5E514s4i4X4S4O4J4T4d4l4u525B56504w4y4-50565D5K594z4n4Z4L474E4L4S4Z4h4p4-595K5U5f5p5o5n5l5k5i5g5c5Z5W5T5Q5N5N5O5P5P5R5R5V5Z5c5g5k5o5h5a5T5M5F584z4o4e4T4J48494A4A4B4D4E4R4d4q515E5R5O5K5G5C59554M3e2x2D1W0o151N1f1y2F2X291n1P110e0G141u2h3V4J5653514_4y4w4u"
					}
				},
				{
					"AttributeName": "wet_bulb_t_2m:C",
					"AttributeUnitOfMeasure": "\u00b0C",
					"AttributeDescription": "[MET] wet bulb temperature at 2m [C]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1,
							"signed": true
						},
						"data": "W7W7W7W7W7WGWOWUWVWWWXWVWTWRWQWPWNWHWAW2VyVrVkViVgVeVlVsVzWIWcWuWxW-X0X1X1X2X3X4X4WzWtWlWfWZWTWRWOWMWKWHWFWQWaWiWqWxX2X2X1X1X1X1X0WxWtWoWiWdWYWWWVWTWSWQWPWbWmWxX6XHXUXXXaXdXgXjXmXiXfXbXYXUXRXSXTXUXVXWXXXfXoXxY4YDYMYNYOYPYQYQYRYOYKYHYDYAY6Y4Y2Y0XzXxXvXwXyXzX_Y1Y2XxXrXkXeXYXSXRXQXQXPXPXO"
					}
				},
				{
					"AttributeName": "wind_dir_20m:d",
					"AttributeUnitOfMeasure": "\u00b0",
					"AttributeDescription": "[MET] wind direction at 20m",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "u6tLsms8rStx1F2H1L0LtYuC0e1N110auC0t203SsFkbgpcwYXVDUtUbUMVTWjY5ZMb5dLcscJbjgV023l9bF4HzJZLHN0NONiN-OEOSOfO1NUM-MYM9LoLJKpKJJnJGIkJVKDKuLVM2MYMPMFM6LzLqLhMQNBNyOjPUQDQEQEQDQDQCQ9P_PtPmPfPaPVPHP4OsOfOROEOjPFPnQLQwRXQwQEPVOgNnMrOLPkQzS1SwTgTYTQTGT6SxSlU3VlXpa7cQeReJeBe3dxdodgcBb2aBZWY-YY"
					}
				},
				{
					"AttributeName": "wind_dir_50m:d",
					"AttributeUnitOfMeasure": "\u00b0",
					"AttributeDescription": "[MET] wind direction at 50m",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0Tu1tetDsl0H1U2J1N0NtauC0c1J0z0Z020q1s3MsPlbhydmZYWZW3VdVGW5X4YDZSb8dNcscIbhh90C3aA8FnIUK7LsNYNsO8OPOdOqP0OPNrNIMnMHLpLIKnKIJpJLItJfKOL3LgMFMlMcMTMKMBM2LvMaNGN-OjPUQFQKQPQUQZQeQjQXQMQDQ5P-PtPhPUPHP4OtOfP3PVPyQSQ-RYQwQHPbOuO8NNOoQ7RJSNTHU2TwTnTdTTTIT6UJVsXoa2cNeXeQeKeDe7e1dwcSbJaQZkZAYj"
					}
				},
				{
					"AttributeName": "wind_gusts_10m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "[MET] wind gusts at 10m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "1A15110z0v0w0v0t0r0p0m0m0l0k0k0m0n0c0R0L0M0O0T0U0W0a0d0g0k0d0X0T0Q0N0K0K0J0I0I0J0L0R0X0d0e0e0f0j0n0r0w0-12100z0x0u0t0t0y11161C1H1M1V1e1o1x242D2B282623201-1r1i1Z1Q1I1E1C1A18161514141313131518171615161718151213151617151312121314181D1H1M1Q1V1M1C130w0u0r0o0l0i0i0j0k0q0v0-14191E1O1V1a1g1l1s"
					}
				},
				{
					"AttributeName": "wind_gusts_20m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "[MET] wind gusts at 20m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "1C17130_0x0y0x0w0u0r0q0p0n0m0l0n0o0c0R0O0Q0R0T0V0W0a0d0h0k0e0Z0X0U0R0N0N0M0L0L0M0M0R0X0d0e0f0g0k0o0s0w0_13100-0y0w0w0w0_14191E1K1P1Y1i1r1-282H2F2C292724221u1l1c1T1M1I1G1E1C191716161616161619181718191A1B181517181A1A1816151515161B1F1K1O1T1Y1O1F160y0u0s0p0l0j0k0l0m0r0x10161B1H1Q1Y1e1k1q1w"
					}
				},
				{
					"AttributeName": "wind_gusts_50m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "[MET] wind gusts at 50m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "1H1B17130-100-100-0z0x0v0u0t0p0n0p0d0X0S0T0V0W0Z0b0d0h0k0o0k0f0b0Y0U0Q0P0O0N0O0P0Q0V0a0f0f0f0h0l0p0u0y1014120_0z0z0-1013181D1I1O1U1d1n1x242E2O2L2I2F2D2A271z1q1g1X1R1M1K1I1G1E1C1A1A1B1B1C1D1F1E1C1C1D1E1F1C1B1C1D1E1F1D1B1A191A1A1E1J1O1S1X1c1S1J19100y0v0t0r0o0m0m0n0t0z13191F1L1V1e1k1q1x21"
					}
				},
				{
					"AttributeName": "wind_speed_20m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "[MET] wind speed at 20m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 1,
							"float_precision": 1
						},
						"data": "TRQPOUbhgfedcbWSOMJHIJKLMNPRTSQOMJGFFEEFFIKNMMLNOQSTVXZbdfhhhggffhjlnprrsssstttssssojfbWSUWZbegggggggfedccbZYXVUTVXacehfedbaYXWVTSRRRRRRRWbglqv"
					}
				},
				{
					"AttributeName": "wind_speed_50m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "[MET] wind speed at 50m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0e0c0a0Y0W0c0i0o0m0l0k0i0h0g0d0a0X0S0O0J0L0M0O0P0R0T0W0Z0c0Z0V0S0O0L0I0H0H0G0H0I0J0N0R0V0V0U0U0W0Y0a0b0d0f0g0i0j0l0m0o0o0p0q0q0r0s0u0x0z10121515151515151514131211100_0x0t0p0k0g0c0f0i0m0p0s0v0v0u0u0t0t0s0q0p0n0l0j0h0g0g0f0e0e0d0g0j0l0o0r0t0r0q0o0m0k0i0g0e0c0a0Y0W0X0X0Y0Y0Z0Z0f0l0r0x1117"
					}
				},
				{
					"AttributeName": "wind_speed_10m:ms",
					"AttributeUnitOfMeasure": "m/s",
					"AttributeDescription": "[MET] wind speed at 10m [m/s]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 1,
							"float_precision": 1
						},
						"data": "MLKJJOUaZYXWVURNJHGEFGHHIIKMNMLKIGDDCCCCCEGIHHHIJKMNOQSUWYaaZYYXXYacdfhhhhiiiiijjjjfbXTQMOPRTVXXXXXXXXWWVVVTSRPONPRSUWYXWVUTRRQPONMMMMMMMQUYcgk"
					}
				},
				{
					"AttributeName": "t_2m:C",
					"AttributeUnitOfMeasure": "\u00b0C",
					"AttributeDescription": "temperature at 2m [C]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1,
							"signed": true
						},
						"data": "WEWEWFWFWFWVWlW_X4X9XEXEXFXFX6WyWpWdWRWGW7V-VsVpVnVlVtW0W8WXWvXHXSXcXmXmXnXnXfXWXNXEX4WwWoWgWZWXWWWUWTWRWQWgWwX9XPXfXvXsXpXnXkXhXeXXXPXIXAX3WxWwWuWtWrWqWoX2XIXYXnY1YHYGYGYGYGYFYFY8Y1XwXpXiXbXdXeXfXgXiXjXxY9YMYaYoZ0Y-YyYwYuYsYqYjYcYVYPYIYBY9Y6Y3Y0XzXwX-Y1Y4Y7YBYEYAY7Y3X_XyXuXsXrXpXnXmXk"
					}
				},
				{
					"AttributeName": "air_density_100m:kgm3",
					"AttributeUnitOfMeasure": "kg/m\u00b3",
					"AttributeDescription": "The density of air at any height level above ground up to 10 km",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 3
						},
						"data": "JvJvJwJxJyJwJuJsJqJoJmJlJkJkJmJoJqJsJuJwJxJyJzJ-J-J-JzJyJxJuJqJnJiJdJYJXJWJVJWJXJYJZJbJcJdJeJfJgJgJhJiJjJkJgJdJZJVJSJOJNJMJKJJJIJGJJJMJPJSJVJYJYJZJaJbJcJdJWJQJKJDJ7J1I_IzIxIwIuIsIuIxIzJ0J2J4J4J5J5J5J5J5J0IwIrImIhIcIbIaIaIZIYIYIbIeIhIkIoIrIsIuIvIwIxIzIyIxIwIvIuItIvIxIzI_J1J3J4J4J5J6J6J7"
					}
				},
				{
					"AttributeName": "high_cloud_cover:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "high cloud cover [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "00000000000000000000000000000000000000000000000000000000000000000000004e9GDvELEmFCFHFMFQFQFPFOETDXCcBgAl9q9L8s8N7u7P6w5z5043372A1D3O5Z7k9vC4EFEUEjExFAFPFeD1AR7q5D2d000_1_2-3z4z5y7T8-AUB_DWF1F1F1F1F2F2F2EwEoEfEXEPEHEIEIEJEKELEMDcCrC5BKAa9qAmBjCgDdEZFWFXFXFXFYFYFYCzAN7n5B2c00000000000000"
					}
				},
				{
					"AttributeName": "medium_cloud_cover:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "amount of medium cloud cover [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "0000000000356A9G928q8d725T3u2c1J000000000001011n3W5F3k2C0h0T0E003r7fBUBtCHChCyDEDVA06W316ZA4DcBV9O7H5A330y0o0e0U0K0A000000000000000000000000002c5C7oAOC-FaDTBL9E77502v2V241g1G0s0S0f0s131H1U1h3-6I8cAvDDFWFRFLFGFAF5E_DCBP9b7o5-4B57636_7x8t9p8A6Y4v3H1e002c5D7pAPD0FcDhBn9s7x60465M6c7t97ANBe"
					}
				},
				{
					"AttributeName": "low_cloud_cover:p",
					"AttributeUnitOfMeasure": "%",
					"AttributeDescription": "low cloud cover [%]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 2,
							"float_precision": 1
						},
						"data": "7N7d7d7d7d9RBFD4B08z6w5b4F2w1-12050402000000001f3I4y6B7R8h6n4s2y5w8uBsC8CPChC5BUAu8R5z3W2Z1d0g0Z0S0L0E07010000000000000000000000000000000000000000000000000000000000002K4e6z9HBbDvBd9K724l2T0A0A0A090909090807070605050t1e2Q3C3z4l4i4e4b4Y4U4R3r3F2f231S0s141I1W1l1z2B2v3e4M555q6Y7K858s9dAOB9"
					}
				},
				{
					"AttributeName": "msl_pressure:hPa",
					"AttributeUnitOfMeasure": "hPa",
					"AttributeDescription": "mean sea level pressure [hPa]",
					"AttributeDataType": "Numeric",
					"Values": {
						"ts_key": "UTC",
						"ts_value": "Value",
						"encoding_start": 1618192800.0,
						"interval": 3600.0,
						"encoder": {
							"numeric_type": "float",
							"encoding_depth": 3,
							"float_precision": 1
						},
						"data": "2W72WA2WG2WM2WS2WW2Wb2Wf2Wf2Wf2Wf2Wf2We2We2Wh2Wl2Wo2Wt2Wx2X02X02X12X12X12X12X12X32X52X72X72X72X82X42X12Wz2Ww2Ws2Wp2Wo2Wn2Wm2Wo2Wq2Ws2Wq2Wo2Wl2Wj2Wh2Wf2Wd2Wa2WY2WT2WO2WJ2WE2W92W42V-2Vt2Vm2Vf2VZ2VS2VP2VN2VK2VH2VF2VC2V82V42V12Uz2Uv2Ur2Uo2Ul2Ui2Uf2Uc2UZ2UX2UV2UT2UR2UP2UO2UN2UN2UM2UM2UL2UL2UK2UJ2UI2UH2UG2UF2UD2UC2UA2U92U72U52U32U12T_2Tz2Ty2Tw2Tx2Ty2T-2T_2U02U22U12U12U12U12U12U02U02T_2T-2Tz2Ty2Tx2T-2U12U42U82UB2UE2UF2UH2UI2UK2UM2UN"
					}
				}
			]
		}
	]
}
```
Input
```json
{
    "Request": {
        "locations": [
            "XXX"
        ],
        "attributes": null,
        "aggregate": true,
        "startDate": "2021-04-12T01:46:08.8622635Z"
    },
    "Response": [
        {
            "LocationName": "XXX",
            "EntityType": "XXX",
            "DisplayName": "BEZ_E01",
            "Latitude": -1,
            "Longitude": -1,
            "Timezone": "Europe/Brussels",
            "DataSource": "ECMWF-IFS",
            "AsOfDateUTC": "2021-04-08T00:00:00Z",
            "ForecastWeather": [
                {
                    "AttributeName": "fresh_snow_6h:cm",
                    "AttributeUnitOfMeasure": "cm",
                    "AttributeDescription": "fresh snow of previous 6h [cm]",
                    "AttributeDataType": "Numeric",
                    "Values": [
                        {
                            "UTC": "2021-04-12T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-18T00:00:00Z",
                            "Value": 0.0
                        }
                    ]
                },
                {
                    "AttributeName": "precip_1h:mm",
                    "AttributeUnitOfMeasure": "mm",
                    "AttributeDescription": "amount of precipitation in the previous 1h [mm]",
                    "AttributeDataType": "Numeric",
                    "Values": [
                        {
                            "UTC": "2021-04-12T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-12T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-13T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-14T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-15T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T00:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T01:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T02:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T03:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T04:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T05:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T06:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T07:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T08:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T09:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T10:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T11:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T12:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T13:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T14:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T15:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T16:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T17:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T18:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-16T19:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T20:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T21:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T22:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-16T23:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-17T00:00:00Z",
                            "Value": 0.2
                        },
                        {
                            "UTC": "2021-04-17T01:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T02:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T03:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T04:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T05:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T06:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T07:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T08:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T09:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T10:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T11:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T12:00:00Z",
                            "Value": 0.29
                        },
                        {
                            "UTC": "2021-04-17T13:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T14:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T15:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T16:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T17:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T18:00:00Z",
                            "Value": 0.08
                        },
                        {
                            "UTC": "2021-04-17T19:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T20:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T21:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T22:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-17T23:00:00Z",
                            "Value": 0.0
                        },
                        {
                            "UTC": "2021-04-18T00:00:00Z",
                            "Value": 0.0
                        }
                    ]
                },
                {
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
                }
            ]
        }
    ]
}
```
