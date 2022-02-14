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

## 0.2.4

    - Improved encoding speed for CSV module by up to 12x, improved decode speed for CSV module by up to 3x.
    - Some performance improvements for JSON module as well that shares underlying encoder
    - Added functional_compression parameter to CSVEncoder.encode_csv. The default behavior is to not use functional compression, enabling it can reduce file size at the cost of longer encoding times.
    - Bug fixes, more tests

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

# Data
## CSVEncoder: Example Output
File Size 800KB -> 61KB encoded -> 28KB encoded & compressed
```json
{
	"encoding_size": 64,
	"value_columns": {
		"ForecastHorizonHour": {
			"function": [
				-456371.9999999486,
				0.0002777777777777467
			],
			"format": ".6f"
		},
		"AsOfDateUTC": {
			"column_value": "2022-01-23T21:34:01.1100000Z"
		},
		"AverageNumericValue": {
			"encoder": {
				"numeric_type": "float",
				"encoding_depth": 4,
				"float_precision": 3,
				"signed": true
			},
			"lookup": {
"Wql0": "00","ZxE8": "01","WLu0": "02","W9Ku": "03","W2VO": "04","Wtua": "05","W1vu": "06","XMrq": "07","XFxe": "08","W0Fe": "09","WI7O": "0A","Wuue": "0B","W2em": "0C","W0KA": "0D","W0Jv": "0E","Wwda": "0F","W0Wq": "0G","WKeK": "0H","WwzS": "0I","WILS": "0J","W1mW": "0K","WwSe": "0L","X4kS": "0M","WSuS": "0N","XCVK": "0O","W7zO": "0P","Wr9a": "0Q","XCjO": "0R","WAjy": "0S","WLIW": "0T","WqCe": "0U","WD3y": "0V","Wupy": "0W","Wtxi": "0X","X2fe": "0Y","WAgq": "0Z","W0KF": "0a","WzEm": "0b","Wzgu": "0c","WLDq": "0d","WC70": "0e","WG10": "0f","Ws9e": "0g","W6wC": "0h","W9MS": "0i","WHca": "0j","W6Ha": "0k","X1Ji": "0l","Wwxu": "0m","Wp-a": "0n","X0_O": "0o","WL_q": "0p","W3X0": "0q","WMki": "0r","WBze": "0s","WNxG": "0t","WNZq": "0u","Wti4": "0v","W3M4": "0w","Wzdm": "0x","X4vO": "0y","W83e": "0z","Wu0O": "0-","X9Ou": "0_","XEgO": "10","WNV8": "11","W0NS": "12","W4Fu": "13","W76i": "14","WNDy": "15","X6Gu": "16","W1d8": "17","WpWu": "18","WOH8": "19","X3ZS": "1A","X71K": "1B","WM64": "1C","WRsq": "1D","X4b4": "1E","W1B0": "1F","WytK": "1G","W0Js": "1H","W_Ja": "1I","W3su": "1J","W8Se": "1K","WONO": "1L","WwG8": "1M","WvG4": "1N","W_v4": "1O","WRB4": "1P","XFw4": "1Q","WMpO": "1R","WNFW": "1S","X94a": "1T","WAtK": "1U","WO34": "1V","WwHi": "1W","WJOe": "1X","XFQq": "1Y","WAJO": "1Z","WwBS": "1a","W9_4": "1b","W0si": "1c","WIhK": "1d","WtdO": "1e","WNYG": "1f","WO7m": "1g","WNS0": "1h","WtHW": "1i","WMCK": "1j","WzXW": "1k","X2Ra": "1l","W2Tq": "1m","WOd0": "1n","WU50": "1o","XCd8": "1p","XK6q": "1q","W9iK": "1r","X7Zi": "1s","WHqe": "1t","WKN8": "1u","WJqm": "1v","WwtC": "1w","XGbq": "1x","XMdm": "1y","W78G": "1z","WDL8": "1-","Ww5C": "1_","WCdq": "20","WLLe": "21","WKRq": "22","W23G": "23","WArm": "24","W1Iq": "25","W-RK": "26","W8um": "27","W0Jf": "28","V_YK": "29","W0S8": "2A","XNfO": "2B","WHRe": "2C","XMJS": "2D","X0lm": "2E","W7Cy": "2F","WIb4": "2G","X5ya": "2H","X5LW": "2I","WEPu": "2J","WNH4": "2K","WBqG": "2L","Wwre": "2M","W-8a": "2N","WtgW": "2O","W8_0": "2P","WLyi": "2Q","W038": "2R","WKty": "2S","WtNm": "2T","W7mu": "2U","ZySG": "2V","XCTm": "2W","W016": "2X","V_Te": "2Y","WyUK": "2Z","WEBq": "2a","WKye": "2b","XCLy": "2c","W43O": "2d","WyfG": "2e","WxJK": "2f","W0uG": "2g","W0JT": "2h","WLbG": "2i","WyD8": "2j","W0mS": "2k","X210": "2l","W2HK": "2m","WyMW": "2n","Wrme": "2o","W5dO": "2p","XIzO": "2q","W-5S": "2r","WBtO": "2s","W_OG": "2t","WCom": "2u","Wxn0": "2v","W4eu": "2w","W3z8": "2x","XFuW": "2y","Wp9S": "2z","WNu8": "2-","W4Ty": "2_","WAfG": "30","WO9K": "31","W49e": "32","WQsm": "33","XJYu": "34","WWR0": "35","WCEq": "36","WyA0": "37","Ws0G": "38","W8wK": "39","WKpG": "3A","W7He": "3B","WU88": "3C","WxzW": "3D","Wr1m": "3E","WH_a": "3F","X0T0": "3G","WCRK": "3H","WH5m": "3I","WIiu": "3J","WDMi": "3K","WNmK": "3L","W7MK": "3M","WGIC": "3N","WIIK": "3O","WvwG": "3P","W-OC": "3Q","XHG0": "3R","W09O": "3S","W60O": "3T","W6oO": "3U","W50K": "3V","W0JO": "3W","W5w8": "3X","X4ZW": "3Y","WLCG": "3Z","XMgu": "3a","W0K5": "3b","Wpo4": "3c","X2Q0": "3d","WGWG": "3e","WJDi": "3f","W95G": "3g","Wssy": "3h","W7PS": "3i","W40G": "3j","X3Gi": "3k","XH54": "3l","V_bS": "3m","Wge8": "3n","WxUG": "3o","X4N0": "3p","WyBa": "3q","X3My": "3r","WBk0": "3s","WEou": "3t","Ww6m": "3u","W5J4": "3v","Wvxq": "3w","W7jm": "3x","WrM4": "3y","W89u": "3z","WvEW": "3-","W7Nu": "3_","W-0m": "40","WvBO": "41","WxYy": "42","WwNy": "43","W5ua": "44","WtrS": "45","W8Yu": "46","WNTa": "47","WtQu": "48","WFI8": "49","W5HW": "4A","Wxq8": "4B","WZEi": "4C","WvR0": "4D","Wtbq": "4E","W0K0": "4F","WLcq": "4G","WwYu": "4H","W0Lu": "4I","ZyCe": "4J","X4Ri": "4K","WN7i": "4L","WAdi": "4M","WziS": "4N","WA_8": "4O","W2SG": "4P","XL0e": "4Q","XBAy": "4R","ZvmO": "4S","XMfK": "4T","WP38": "4U","WYR8": "4V","W6py": "4W","WAuu": "4X","WTTy": "4Y","WtoK": "4Z","X34C": "4a","W5ey": "4b","WBn8": "4c","XLaa": "4d","WM-K": "4e","Wxc4": "4f","WFRW": "4g","W7BO": "4h","XC3C": "4i","W9aW": "4j","WRz4": "4k","Wzoi": "4l","V_uC": "4m","X4LS": "4n","W73a": "4o","X4De": "4p","W2M0": "4q","WsoG": "4r","W0K2": "4s","X3C0": "4t","WFPy": "4u","ZvH8": "4v","WL60": "4w","WhC4": "4x","W5pu": "4y","W3rK": "4z","X9NK": "4-","W1gG": "4_","WxfC": "50","W5zG": "51","W8gi": "52","WGJm": "53","X44G": "54","W_8e": "55","W9Pa": "56","W0JW": "57","WxGC": "58","WPjK": "59","XMMa": "5A","XLfG": "5B","W8R4": "5C","Wz5O": "5D","W9zW": "5E","WDW4": "5F","X9V8": "5G","V_g8": "5H","W44y": "5I","V_-S": "5J","WAZ0": "5K","Wx0a": "5L","WG8q": "5M","WuSW": "5N","W0d4": "5O","Wwum": "5P","W3Fq": "5Q","WAKy": "5R","Wv9q": "5S","WsBC": "5T","Wx5G": "5U","W0JZ": "5V","XL6u": "5W","Ws1q": "5X","W9R8": "5Y","Ws-m": "5Z","W0Im": "5a","W1HG": "5b","WwoW": "5c","WJ90": "5d","Zv1W": "5e","X2e4": "5f","W-DG": "5g","WwR4": "5h","WAy0": "5i","Ww0W": "5j","WQ6K": "5k","WN1S": "5l","XAse": "5m","W8lO": "5n","WyJO": "5o","V_Oy": "5p","WKCC": "5q","X1s4": "5r","W6MG": "5s","W3SK": "5t","WrEG": "5u","WMZm": "5v","WIyW": "5w","W8q4": "5x","WKqq": "5y","WuwC": "5z","W0Jd": "5-","WwUC": "5_","Wuf0": "60","Wtje": "61","WJC8": "62","WD5W": "63","WGlu": "64","XCQe": "65","X02S": "66","WMbK": "67","W9wO": "68","WJ4K": "69","Wyrm": "6A","W6Ki": "6B","XEB8": "6C","WRpi": "6D","Wrl4": "6E","W5Cq": "6F","XGua": "6G","W1pe": "6H","Wvq0": "6I","XMA4": "6J","WA3m": "6K","WJWS": "6L","X00u": "6M","WQz0": "6N","WFWC": "6O","W0pa": "6P","W0Ti": "6Q","WV8C": "6R","X0Ua": "6S","WIJu": "6T","X0Xi": "6U","WCgy": "6V","WOjG": "6W","WUCq": "6X","Wk-G": "6Y","W2YW": "6Z","WnbS": "6a","WGDW": "6b","WPCW": "6c","XLiO": "6d","X2By": "6e","W3HO": "6f","WMFS": "6g","WPxO": "6h","WHvK": "6i","WOCS": "6j","WLWa": "6k","WCHy": "6l","WqVO": "6m","XGSS": "6n","WL4S": "6o","W1-a": "6p","W8iG": "6q","W0Qa": "6r","W3Tu": "6s","WwKq": "6t","X8We": "6u","WNeW": "6v","W-Bi": "6w","WDwe": "6x","XL_8": "6y","W3Ne": "6z","WCA8": "6-","W-qK": "6_","Zw00": "70","W2B4": "71","X4Q8": "72","WJY0": "73","W7lK": "74","Wxxy": "75","WKni": "76","X4m0": "77","Wz0i": "78","W_Mi": "79","WzVy": "7A","W1P4": "7B","XBYO": "7C","W2xW": "7D","WBae": "7E","XMVy": "7F","W9c4": "7G","W9O0": "7H","X2T8": "7I","WOuC": "7J","W9UG": "7K","WzDC": "7L","Wsl8": "7M","WCPm": "7N","WHDa": "7O","WGzy": "7P","WCDG": "7Q","W4uW": "7R","WJne": "7S","Wtey": "7T","WEUa": "7U","W5rS": "7V","Wuji": "7W","WsQq": "7X","W_ZC": "7Y","WtlC": "7Z","WvYq": "7a","WFh8": "7b","W56a": "7c","Wvjm": "7d","X52m": "7e","WHZS": "7f","WxEe": "7g","WFUe": "7h","W8MO": "7i","W8G8": "7j","XLUK": "7k","WCru": "7l","WwXK": "7m","Wq4q": "7n","WB8W": "7o","WNLm": "7p","WQB0": "7q","W2be": "7r","W5X8": "7s","W_ia": "7t","Wrz8": "7u","WIsG": "7v","W6zK": "7w","W0Jo": "7x","X5fq": "7y","X6-C": "7z","X5kW": "7-","W3w0": "7_","X2kK": "80","WKFK": "81","X314": "82","W3EG": "83","WqrG": "84","Wj4O": "85","W4Ye": "86","WC8a": "87","WAn4": "88","WFwm": "89","XJD0": "8A","W21i": "8B","XKVq": "8C","X8H0": "8D","WH4C": "8E","XA34": "8F","WZ2C": "8G","WRHK": "8H","WKvW": "8I","W-Su": "8J","X3wu": "8K","Wv3a": "8L","WpFi": "8M","W8Vm": "8N","W5Va": "8O","W7Yq": "8P","W8Hi": "8Q","XEHO": "8R","W6rW": "8S","W_tW": "8T","Wzn8": "8U","WMg0": "8V","W2sq": "8W","WHnW": "8X","WGT8": "8Y","XNJW": "8Z","XCB0": "8a","WuPO": "8b","Wwc0": "8c","X0kC": "8d","X0Je": "8e","W3-i": "8f","Wu3W": "8g","X418": "8h","WK5y": "8i","W0Jh": "8j","V_NO": "8k","WvzO": "8l","W7iC": "8m","X1T4": "8n","XDTq": "8o","WuKi": "8p","W2hu": "8q","W0o0": "8r","WOIi": "8s","WOE0": "8t","W1Qe": "8u","WpuK": "8v","W0K6": "8w","WL1K": "8x","WJLW": "8y","WOKG": "8z","WszC": "8-","W3eq": "8_","WKm8": "90","W1rC": "91","WuJ8": "92","W-US": "93","WMcu": "94","WGvG": "95","WIeC": "96","WKOi": "97","W2o8": "98","W36S": "99","XEz8": "9A","WH-0": "9B","WMH0": "9C","Wq-e": "9D","WF2W": "9E","W_L8": "9F","X3tm": "9G","WCtS": "9H","WEcO": "9I","Wu1y": "9J","Wy8S": "9K","XBP0": "9L","WGMu": "9M","WITG": "9N","W6xm": "9O","W0JS": "9P","WvaO": "9Q","WNcy": "9R","W4bm": "9S","WIce": "9T","WzMa": "9U","V_S4": "9V","XCHG": "9W","V_Lq": "9X","WKGu": "9Y","W3Ya": "9Z","W5Ke": "9a","Wrxa": "9b","W24q": "9c","W1VK": "9d","WWVi": "9e","XKzW": "9f","W758": "9g","Wp04": "9h","WrgO": "9i","W2Wy": "9j","XCa0": "9k","X7Ru": "9l","W-L4": "9m","W1o4": "9n","WLeO": "9o","Wsxe": "9p","WzGK": "9q","WxSi": "9r","W0Jn": "9s","W6PO": "9t","W0JV": "9u","W8f8": "9v","W0K9": "9w","W0JX": "9x","X7bG": "9y","XMqG": "9z","W2EC": "9-","W2jS": "9_","W13C": "A0","WNg4": "A1","WJTK": "A2","WqjS": "A3","W0Jp": "A4","V_pW": "A5","Wtw8": "A6","W3gO": "A7","WLAi": "A8","W0Jy": "A9","WtBG": "AA","W1sm": "AB","WRa4": "AC","WDv4": "AD","W1SC": "AE","WNKC": "AF","XCKO": "AG","W4M8": "AH","W2Fm": "AI","WMYC": "AJ","W7aO": "AK","W654": "AL","XLGG": "AM","WBA4": "AN","V_yu": "AO","WMve": "AP","W19S": "AQ","WBXW": "AR","Ws3O": "AS","WtYi": "AT","W5xi": "AU","WJ7S": "AV","WLFO": "AW","W-le": "AX","WrQm": "AY","W_AC": "AZ","V_r4": "Aa","X5N4": "Ab","WGhC": "Ac","W7q0": "Ad","WEEy": "Ae","WtFy": "Af","WNr0": "Ag","W928": "Ah","WMRy": "Ai","W3KW": "Aj","W1ky": "Ak","V_ea": "Al","WrKW": "Am","W0Ja": "An","WF0y": "Ao","X05a": "Ap","X3TC": "Aq","WyVu": "Ar","X0h4": "As","WA6u": "At","W7Km": "Au","WpjO": "Av","X65y": "Aw","W0Zy": "Ax","W66e": "Ay","WzcC": "Az","WET0": "A-","XLoe": "A_","WBy4": "B0","WI2i": "B1","WZfG": "B2","X1Mq": "B3","X0dy": "B4","WtPK": "B5","W79q": "B6","WtzG": "B7","X6j0": "B8","W0Ji": "B9","W96q": "BA","WNpS": "BB","Zwku": "BC","W0gC": "BD","WGti": "BE","W0ee": "BF","W4BC": "BG","Wt0K": "BH","X35m": "BI","WItq": "BJ","W9ju": "BK","XKuq": "BL","XMUO": "BM","WLGy": "BN","W4zC": "BO","W0VG": "BP","XJG8": "BQ","WzJS": "BR","X0I4": "BS","WO4e": "BT","Wy5K": "BU","WPQa": "BV","V_hi": "BW","XLHq": "BX","WM9C": "BY","X0GW": "BZ","X3Um": "Ba","W3bi": "Bb","Woku": "Bc","WuaK": "Bd","W3a8": "Be","W2dC": "Bf","W7Vi": "Bg","Wtpu": "Bh","WLqu": "Bi","Wvt8": "Bj","WWoS": "Bk","WCiW": "Bl","WNsa": "Bm","W85C": "Bn","WbSu": "Bo","W_5W": "Bp","ZyxW": "Bq","W720": "Br","WurW": "Bs","WoNS": "Bt","V_kq": "Bu","W1hq": "Bv","W8UC": "Bw","WEXi": "Bx","WLTS": "By","WD_K": "Bz","W6t4": "B-","WJZa": "B_","WrVS": "C0","W0JY": "C1","X0Bq": "C2","W2Qi": "C3","X5qm": "C4","Wq9W": "C5","W33K": "C6","WKsO": "C7","XLO4": "C8","WC_G": "C9","Wvf4": "CA","WqQi": "CB","Wr-i": "CC","WLj4": "CD","X078": "CE","WzPi": "CF","W69m": "CG","WI_e": "CH","WuHa": "CI","X2Jm": "CJ","W0ku": "CK","W3B8": "CL","WyZ0": "CM","WT84": "CN","W4rO": "CO","WNIe": "CP","WDUW": "CQ","W0K4": "CR","WC0m": "CS","W1ei": "CT","WudS": "CU","WvoS": "CV","WsJ0": "CW","W0JQ": "CX","WJci": "CY","WAA0": "CZ","W-gy": "Ca","WT0G": "Cb","W3Qm": "Cc","WvPS": "Cd","W_am": "Ce","WLK4": "Cf","W0CW": "Cg","WBla": "Ch","W0JP": "Ci","WuU4": "Cj","W2rG": "Ck","W-k4": "Cl","WR-e": "Cm","WuQy": "Cn","Wvge": "Co","WOAu": "Cp","W6ji": "Cq","XCNW": "Cr","Wpba": "Cs","XMiS": "Ct","W16K": "Cu","W066": "Cv","WTNi": "Cw","Wv6i": "Cx","X3OW": "Cy","XM2G": "Cz","WIZW": "C-","XCSC": "C_","WHLO": "D0","Wuga": "D1","WomS": "D2","WQ-a": "D3","W46W": "D4","WLhW": "D5","Wzrq": "D6","XB1a": "D7","W0-W": "D8","W3me": "D9","X1fa": "DA","W6i8": "DB","XETu": "DC","WASm": "DD","XAmO": "DE","WqTq": "DF","X590": "DG","WuXC": "DH","WEta": "DI","WMLi": "DJ","WJtu": "DK","WJRm": "DL","Wyaa": "DM","W5-q": "DN","W6Ve": "DO","W0Jb": "DP","WKx4": "DQ","W0HC": "DR","X0LC": "DS","X6eK": "DT","X9KC": "DU","WNjC": "DV","WKhS": "DW","WHGi": "DX","Wubu": "DY","W31m": "DZ","W8c0": "Da","WzO8": "Db","WvXG": "Dc","ZxjO": "Dd","W2-e": "De","W0JM": "Df","WtMC": "Dg","WO1W": "Dh","WIAW": "Di","W0Jw": "Dj","XKO0": "Dk","Wsja": "Dl","WxiK": "Dm","WMNG": "Dn","WM2y": "Do","W11e": "Dp","XMtO": "Dq","W9Yy": "Dr","WRIu": "Ds","X8NG": "Dt","W4PG": "Du","WqIu": "Dv","WyRC": "Dw","WM7e": "Dx","XHf0": "Dy","XMZ4": "Dz","X47O": "D-","WAc8": "D_","WE5a": "E0","WHwu": "E1","Wydi": "E2","XDWy": "E3","WyiO": "E4","XN0m": "E5","WaA4": "E6","WBSq": "E7","XJMO": "E8","X248": "E9","WsTy": "EA","Wy0e": "EB","Wdzq": "EC","W8Ny": "ED","W-wa": "EE","X6hS": "EF","XIlK": "EG","WMym": "EH","W88K": "EI","W70S": "EJ","WsM8": "EK","W4HS": "EL","WAoe": "EM","WBgu": "EN","W06G": "EO","X7Gy": "EP","Wt88": "EQ","WAXS": "ER","WpCa": "ES","WN4a": "ET","WBL0": "EU","WEW8": "EV","Wwmy": "EW","W0Jz": "EX","WD0q": "EY","WyGG": "EZ","WFMq": "Ea","W3pm": "Eb","WQQe": "Ec","W0Jl": "Ed","WMOq": "Ee","W0E4": "Ef","X5tu": "Eg","Wt3S": "Eh","WJya": "Ei","W3Ci": "Ej","Wqz4": "Ek","WsPG": "El","W824": "Em","WwD0": "En","Wzae": "Eo","WEnK": "Ep","WrPC": "Eq","W7ra": "Er","WH2e": "Es","WLY8": "Et","WGe4": "Eu","W8aS": "Ev","W9Vq": "Ew","Wosi": "Ex","WOQW": "Ey","WrdG": "Ez","X6Dm": "E-","WxaW": "E_","X38u": "F0","X0ta": "F1","W2Ce": "F2","X7hW": "F3","WKTO": "F4","W3oC": "F5","WCOC": "F6","WJiy": "F7","Wu54": "F8","Wf7G": "F9","WuYm": "FA","X2AO": "FB","W0KD": "FC","W9D4": "FD","XJoW": "FE","WuCu": "FF","XMO8": "FG","X0cO": "FH","XI-y": "FI","W9de": "FJ","Wqbe": "FK","W0Jj": "FL","V_xK": "FM","W34u": "FN","W7G4": "FO","Wygq": "FP","WJ1C": "FQ","WM_u": "FR","WREC": "FS","W_Xe": "FT","XMn8": "FU","WMAm": "FV","Wt9i": "FW","X2yO": "FX","XBWq": "FY","WYn0": "FZ","W3PC": "Fa","W5aG": "Fb","Zxz0": "Fc","XBTi": "Fd","WLZi": "Fe","X1F0": "Ff","X9-O": "Fg","WLx8": "Fh","W9n0": "Fi","XLPe": "Fj","WwwK": "Fk","W484": "Fl","W1Wu": "Fm","WAMW": "Fn","XEKW": "Fo","WKLa": "Fp","X7j4": "Fq","WJhO": "Fr","XNHy": "Fs","WFDS": "Ft","XNom": "Fu","Wui8": "Fv","WJfq": "Fw","W7U8": "Fx","WvSa": "Fy","WqKS": "Fz","Wv8G": "F-","W__K": "F_","WNAq": "G0","W0Ju": "G1","W_oq": "G2","X28q": "G3","WKZe": "G4","W4mi": "G5","W00y": "G6","Wrbi": "G7","WSNe": "G8","W0JN": "G9","WNnu": "GA","X0ZG": "GB","W5EO": "GC","WKj0": "GD","WJN4": "GE","W4Ni": "GF","W2P8": "GG","V_se": "GH","WO6C": "GI","W0J-": "GJ","W0JU": "GK","W7R0": "GL","X15e": "GM","WRTq": "GN","WABa": "GO","WsNi": "GP","X7yi": "GQ","WK1G": "GR","WDcK": "GS","W8D0": "GT","W7XG": "GU","WEv8": "GV","XLD8": "GW","V_VC": "GX","WMDu": "GY","W1Ca": "GZ","X1qW": "Ga","WJ_i": "Gb","W05U": "Gc","X2ay": "Gd","WpHG": "Ge","WGGe": "Gf","W1YS": "Gg","WvJC": "Gh","X0OK": "Gi","WSSK": "Gj","W4SO": "Gk","Wvui": "Gl","WOLq": "Gm","W6Qy": "Gn","Wsbm": "Go","W39a": "Gp","WCJW": "Gq","WCGO": "Gr","W0Je": "Gs","WJm4": "Gt","WRl0": "Gu","W_du": "Gv","WMsW": "Gw","WF8m": "Gx","WCW0": "Gy","WuBK": "Gz","W01a": "G-","WJvS": "G_","W30C": "H0","WvU8": "H1","W0bW": "H2","WQ9S": "H3","WA5K": "H4","W3l4": "H5","WBiS": "H6","WA2C": "H7","WySm": "H8","V_jG": "H9","WE_O": "HA","XCWu": "HB","WGim": "HC","WKK0": "HD","W0KG": "HE","W9tG": "HF","W7dW": "HG","WOOy": "HH","WLmC": "HI","X18m": "HJ","WKAe": "HK","WLsS": "HL","XAAu": "HM","WK_m": "HN","V_Zu": "HO","W2ma": "HP","XN70": "HQ","WruS": "HR","WxXO": "HS","WzHu": "HT","WSVS": "HU","W0Jx": "HV","Wzk0": "HW","WMu4": "HX","WdT0": "HY","W6Ym": "HZ","WroC": "Ha","WzL0": "Hb","W90a": "Hc","W07q": "Hd","WquO": "He","WYuq": "Hf","Ww9u": "Hg","WDAC": "Hh","WE2S": "Hi","WBfK": "Hj","XBmS": "Hk","WvlK": "Hl","XMcC": "Hm","W2l0": "Hn","WY_4": "Ho","WDGS": "Hp","X7eO": "Hq","W3jW": "Hr","XAKG": "Hs","Zunu": "Ht","W9Si": "Hu","W0K1": "Hv","W0K3": "Hw","Wv-y": "Hx","X1Xm": "Hy","WLNC": "Hz","Wt1u": "H-","WCMe": "H_","WAVu": "I0","WFqW": "I1","WwJG": "I2","XDIu": "I3","WK94": "I4","WR9W": "I5","WuoO": "I6","XECi": "I7","X1kG": "I8","WN_y": "I9","WKY4": "IA","WK2q": "IB","WHAS": "IC","V_vm": "ID","WCL4": "IE","WG48": "IF","X0AG": "IG","W2vy": "IH","X8TW": "II","Wvmu": "IJ","Ww3e": "IK","WKDm": "IL","W3Iy": "IM","WL98": "IN","X3p4": "IO","WMTW": "IP","WG7G": "IQ","WmOu": "IR","Wqvy": "IS","WsdK": "IT","X62q": "IU","W6Nq": "IV","X1au": "IW","WIna": "IX","W208": "IY","WHp4": "IZ","WF44": "Ia","WwMO": "Ib","W26O": "Ic","W4VW": "Id","WAEi": "Ie","W9Hm": "If","V_mO": "Ig","X6CC": "Ih","W4J0": "Ii","W0KB": "Ij","WZ6u": "Ik","W6ES": "Il","W4Qq": "Im","WAO4": "In","WHXu": "Io","W0Jr": "Ip","WAD8": "Iq","W0hm": "Ir","WJIO": "Is","W1Tm": "It","W9BW": "Iu","Wx28": "Iv","WWwG": "Iw","WFs4": "Ix","WCBi": "Iy","WIvO": "Iz","W17u": "I-","WW8G": "I_","W9xy": "J0","WjUy": "J1","Wvby": "J2","W7-y": "J3","W4Ka": "J4","Wby8": "J5","WLRu": "J6","Wtt0": "J7","WPpa": "J8","Wz_C": "J9","WNOu": "JA","WIm0": "JB","WDDK": "JC","WAUK": "JD","WM1O": "JE","X0W8": "JF","X2DW": "JG","X7fy": "JH","XFeu": "JI","WB2G": "JJ","W7ui": "JK","WLV0": "JL","W4Cm": "JM","WEdy": "JN","W6bu": "JO","WI4G": "JP","W1z0": "JQ","W1xS": "JR","X5hO": "JS","W1NW": "JT","WA8S": "JU","W0KK": "JV","WFoy": "JW","XCFi": "JX","W2Iu": "JY","W51u": "JZ","WtX8": "Ja","X4WO": "Jb","WyqC": "Jc","W4ja": "Jd","W1uK": "Je","X2p0": "Jf","W1Fi": "Jg","WKfu": "Jh","WsEK": "Ji","X4wy": "Jj","WJGq": "Jk","X9he": "Jl","W6-u": "Jm","WAza": "Jn","WtU0": "Jo","X7QK": "Jp","Wy_8": "Jq","WE8i": "Jr","XAH8": "Js","X5sK": "Jt","X7Le": "Ju","WNCO": "Jv","WAqC": "Jw","WNNK": "Jx","W99y": "Jy","Wv0S": "Jz","W1jO": "J-","WKcm": "J_","XNnC": "K0","XJaS": "K1","WyEi": "K2","W8Kq": "K3","W5i4": "K4","V_QW": "K5","X144": "K6","W-ai": "K7","WzqG": "K8","WC3u": "K9","WY3i": "KA","WE78": "KB","W0jK": "KC","Wqhu": "KD","WEh4": "KE","XBd4": "KF","W2a4": "KG","WxVq": "KH","WL-G": "KI","WFOO": "KJ","X6vW": "KK","WztO": "KL","WNyq": "KM","X4na": "KN","WFLG": "KO","WS1m": "KP","WJpC": "KQ","Wu9m": "KR","WBoi": "KS","WviC": "KT","W80W": "KU","WLfy": "KV","W8xu": "KW","WOse": "KX","W0YO": "KY","WsgS": "KZ","W5bq": "Ka","Wa3q": "Kb","WU9i": "Kc","WCcG": "Kd","W0J_": "Ke","XHNq": "Kf","WyHq": "Kg","WDBm": "Kh","X4IK": "Ki","WI8y": "Kj","Wzze": "Kk","X0aq": "Kl","WDdu": "Km","ZwVG": "Kn","W0Jt": "Ko","WFzu": "Kp","Wbwa": "Kq","W8PW": "Kr","Wxri": "Ks","WIQ8": "Kt","W6lG": "Ku","XMDC": "Kv","WHIG": "Kw","XCP4": "Kx","WDam": "Ky","Wut4": "Kz","WH7K": "K-","XJBS": "K_","W6SW": "L0","W7JC": "L1","WBEm": "L2","XBKK": "L3","W2uO": "L4","WAHq": "L5","W9JK": "L6","WtSS": "L7","WxR8": "L8","Wu8C": "L9","WHOW": "LA","WRxW": "LB","XAWm": "LC","WBHu": "LD","W0K8": "LE","WB0i": "LF","WMha": "LG","WvHe": "LH","WEGW": "LI","W0JR": "LJ","Wu-u": "LK","WLva": "LL","W_Pq": "LM","WwVm": "LN","XAQW": "LO","ZxTm": "LP","XCei": "LQ","X0wi": "LR","W5Qu": "LS","Wi_i": "LT","W2KS": "LU","WJsK": "LV","WEI4": "LW","Wu6e": "LX","WD2O": "LY","WN68": "LZ","W5Yi": "La","X5C8": "Lb","XKUG": "Lc","WMK8": "Ld","WSgO": "Le","WMmG": "Lf","W7xq": "Lg","WNbO": "Lh","WN9G": "Li","X4C4": "Lj","WB6y": "Lk","WMIa": "Ll","W-Me": "Lm","WtEO": "Ln","WVXC": "Lo","W9fC": "Lp","ZwFe": "Lq","W380": "Lr","WShy": "Ls","WyO4": "Lt","Zw-W": "Lu","WBDC": "Lv","W7by": "Lw","W9ri": "Lx","WIp8": "Ly","WXxu": "Lz","W7EW": "L-","X9QS": "L_","WMWe": "M0","Wwf8": "M1","W6J8": "M2","W00o": "M3","WKka": "M4","XNPm": "M5","WzSq": "M6","X040": "M7","WuES": "M8","WJeG": "M9","Wv20": "MA","W2gK": "MB","W5U0": "MC","W1a0": "MD","W4dK": "ME","WuVe": "MF","XLZ0": "MG","WvCy": "MH","WQSC": "MI","W7ge": "MJ","X1te": "MK","W1E8": "ML","XLEi": "MM","WGs8": "MN","XBIm": "MO","W7oS": "MP","Wtmm": "MQ","WMqy": "MR","WMV4": "MS","W2z4": "MT","W0xO": "MU","X1WC": "MV","WFBu": "MW","W6ue": "MX","WM4W": "MY","W5SS": "MZ","Zyhu": "Ma","WNhe": "Mb","X4qi": "Mc","Wseu": "Md","W9q8": "Me","WsHS": "Mf","W_ry": "Mg","W3hy": "Mh","XNk4": "Mi","WtaG": "Mj","W8BS": "Mk","W3dG": "Ml","WqNa": "Mm","WIWO": "Mn","XFbm": "Mo","WqM0": "Mp","W3VS": "Mq","W5t0": "Mr","WEJe": "Ms","WGZO": "Mt","WDI0": "Mu","WN30": "Mv","W4-m": "Mw","W1KO": "Mx","W0vq": "My","Wqa4": "Mz","W104": "M-","X3AS": "M_","WLOm": "N0","X1OO": "N1","WNvi": "N2","X25i": "N3","Wspq": "N4","W3uS": "N5","WFkG": "N6","WSX0": "N7","WLnm": "N8","WC2K": "N9","X0s0": "NA","WQ04": "NB","WHhG": "NC","WCUS": "ND","W3xa": "NE","WNWi": "NF","W9Ee": "NG","WT3O": "NH","W9GC": "NI","W0P0": "NJ","WMeS": "NK","W8Ea": "NL","WIOa": "NM","WUX8": "NN","X2cW": "NO","Wt-q": "NP","W5Fy": "NQ","W7Sa": "NR","X9vi": "NS","WQIq": "NT","XBZy": "NU","W2pi": "NV","W8jq": "NW","WqxW": "NX","W4EK": "NY","X3b0": "NZ","WHtm": "Na","W29W": "Nb","W9oa": "Nc","W6Cu": "Nd","WPVG": "Ne","W5oK": "Nf","W000": "Ng","V_ny": "Nh","WFau": "Ni","WJJy": "Nj","W4pq": "Nk","W0K7": "Nl","X9Ta": "Nm","WvMK": "Nn","WLke": "No","V_Wm": "Np","Wyy0": "Nq","WDia": "Nr","X1Bu": "Ns","XMae": "Nt","Wvra": "Nu","XLrm": "Nv","W9gm": "Nw","W6f0": "Nx","WrYa": "Ny","W0r8": "Nz","WrX0": "N-","WyKy": "N_","W8JG": "O0","X9u8": "O1","XCE8": "O2","X8V4": "O3","WDqO": "O4","WwEa": "O5","W2Na": "O6","WOFa": "O7","W5MC": "O8","W4l8": "O9","WAPe": "OA","WA0e": "OB","WJ5u": "OC","W0yy": "OD","WHb0": "OE","WsKa": "OF","WuzK": "OG","W1Ly": "OH","WLpK": "OI","WEaq": "OJ","WxKu": "OK","WL2u": "OL","WWYq": "OM","X3vK": "ON","X1_S": "OO","XEoC": "OP","W0Jm": "OQ","WuNq": "OR","W98O": "OS","W1ba": "OT","WrSK": "OU","WsFu": "OV","XJgi": "OW","WKbC": "OX","Wz3q": "OY","XNL4": "OZ","WJ2m": "Oa","XOXe": "Ob","W0Ay": "Oc","X7cq": "Od","XDz4": "Oe","W4i0": "Of","W8XK": "Og","W4xe": "Oh","WIfm": "Oi","Wx3i": "Oj","Wsmi": "Ok","W0Jq": "Ol","XGrS": "Om","WGyO": "On","WvNu": "Oo","XANO": "Op","WIN0": "Oq","Wuxm": "Or","X6pG": "Os","W41q": "Ot","XAYK": "Ou","XBxO": "Ov","W0KC": "Ow","WvVi": "Ox","XAuC": "Oy","WJAa": "Oz","W0KE": "O-","X8eS": "O_","WMnq": "P0","WKIS": "P1","XNcG": "P2","X4iu": "P3","W4w4": "P4","W27y": "P5","XC04": "P6","Whce": "P7","Wyoe": "P8","W53S": "P9","W14m": "PA","W5gW": "PB","WK-C": "PC","WG2a": "PD","WFyK": "PE","XAVC": "PF","W8da": "PG","WB5O": "PH","WNQS": "PI","X6La": "PJ","WSdG": "PK","V_d0": "PL","WwPW": "PM","WGcW": "PN","WtJ4": "PO","WHe8": "PP","ZvWm": "PQ","WN-O": "PR","WxMS": "PS","W04i": "PT","WK7W": "PU","WJb8": "PV","WJUu": "PW","W8re": "PX","WJx0": "PY","W550": "PZ","WqdC": "Pa","WMQO": "Pb","W9uq": "Pc","W7f4": "Pd","WNkm": "Pe","WMj8": "Pf","W_zm": "Pg"
			},
			"format": ".6f"
		}
	},
	"time": {
		"name": "UTC",
		"start": 1643004000.0,
		"encoder": {
			"numeric_type": "int",
			"encoding_depth": 2,
			"float_precision": 0
		},
		"lookup": {
			"uG": "0",
			"00": "1"
		}
	},
	"keys": {
		"columns": [
			"Attribute"
		],
		"lookup": {
			"relative_humidity_50m:p": "0",
			"low_cloud_cover:p": "1",
			"wind_speed_100m:ms": "2",
			"wind_gusts_80m:ms": "3",
			"prob_rr_3h:p": "4",
			"wind_speed_50m:ms": "5",
			"wind_dir_120m:d": "6",
			"visibility:km": "7",
			"wind_dir_10m:d": "8",
			"fresh_snow_6h:cm": "9",
			"high_cloud_cover:p": "A",
			"relative_humidity_2m:p": "B",
			"wind_gusts_50m:ms": "C",
			"wind_speed_120m:ms": "D",
			"effective_cloud_cover:p": "E",
			"t_2m:F": "F",
			"wind_dir_100m:d": "G",
			"direct_rad:W": "H",
			"wet_bulb_t_2m:C": "I",
			"total_cloud_cover:p": "J",
			"dew_point_2m:C": "K",
			"snow_depth:cm": "L",
			"wind_speed_10m:ms": "M",
			"global_rad:W": "N",
			"precip_1h:mm": "O",
			"medium_cloud_cover:p": "P",
			"wind_gusts_10m:ms": "Q",
			"msl_pressure:hPa": "R",
			"wind_dir_80m:d": "S",
			"diffuse_rad:W": "T",
			"wind_dir_20m:d": "U",
			"wind_dir_50m:d": "V",
			"wind_speed_20m:ms": "W",
			"wind_gusts_100m:ms": "X",
			"wind_speed_80m:ms": "Y",
			"wind_gusts_20m:ms": "Z",
			"t_2m:C": "a",
			"air_density_100m:kgm3": "b",
			"t_100m:C": "c",
			"sfc_pressure:hPa": "d",
			"relative_humidity_100m:p": "e"
		}
	},
	"columns": [
		"UTC",
		"Attribute",
		"AverageNumericValue",
		"AsOfDateUTC",
		"ForecastHorizonHour"
	],
	"data": "1b4s1I5H1GDs182K16AC1UDV1V4U1SEc1Q6P1ZNz1C2g13Dp12Nz1MNJ1D6P1WBP15BD1Y2k17FO1JBF1XCu1aNh1FGL1TNg1HNg1EBF19Ng1NNg1ANg11BF1PNg1KAl1c2k1ONg14091eB_1BPI10DW1dFc1LNg1R2V0U5k16PK18J81JD81I9V178S1VD31GGj1S1D12MU1ZMy1CM-13I-1M6Q1DMy1WH2152k1Y1c1QMy1FEJ1XGZ1cKC1KK51TNg1HNg1ED819Ng1NNg1ANg11D81PNg1bHw1R2V1LNg1dFc103A1a291e7S14091ONg1BJA079O1I5p1GCw18Ne164Y1U6h1VFS1SN71XAQ1Z1c1COD1Y6P122g1M2A1D1c1WAx15KC1J5a1Q1c13PA1F0h1cIr1aNp1bCR1K9X1T991HNV19Ng1N3X1ANg115a1E5a1R2V1PNg1dFc105y1B7p1LNg14091ONg1e1v0XM-1I4m1GCb189R16NH1U6j1VNB1S6D1Q2k173x1C6P13MU122k1M4I1D2k1W2A15H21YKC1Z2k1JEO1PNg1aPT1KNh1T1Z1H671EEO19Ng1NIw1ANg11EO1FLg1b4s1ONg14091eCY1BEe10F41dFc1LNg1c6P1R2V0VCp1UJL16Ls17NG1GLe1I5a1S3318OX1X2g132k1ZBF1CBD12BD1MOc1DBD1W0915NJ1JNg1QBF1F271YAx1cMy1b4F1KEO1TC91H851ENg19Ng1NIK1ANg11Ng1aH21R2V1ONg14091eGE1B8x10LV1d4J1LNg1PNg0VJx1UBY165917In1GBV1IBF1S1n18No1X2k136Q1Z121C6r12JV1MOc1D121WEf15DR1JNg1QJV1Y5a1FNc1cM-1aCu1bGJ1K4I1TKB1HEZ19Ng1NOp1ANg11Ng1ENg1R2V1PNg1d4J103f1BPV1LNg14091ONg1e690SLd17301I1c1G9418Cf16AP1UBy1VLL1QNJ1JNg1CH2135O124I1M091D121W5a154I1Y4I1Z6Q1FIn1X5O1cPA1K2A1TOJ1H0o1ENg19Ng1NMo1ANg11Ng1PNg1bEX1R2V1ONg14091eCY1BOq103f1dFc1LNg1a8u0VA21U3f16Ei17LF1GLV1IOD1SF7185d1XBF135O1ZKY1C5O126r1MJV1D6r1W12156r1JNg1QKY1F0Z1Y6r1cML1b0E1K2A1TEV1HFk1ENg19Ng1N0_1ANg11Ng1aOT1R4J1ONg14091eIs1BPP10JB1dFc1LNg1PNg0V3O1UJP163J17AN1GOi1ID81SMn183F1XBD13BF1ZAx1CBF126r1MJV1D2A1WNJ152A1J091QKY1Y2A1F0S1c251a171bKo1K6Q1TCQ1H4x19Ng1ND11ANg11091E091R4J1PNg1dDd109T1B7f1LNg14091ONg1eAV0S6i174M1IOD1GJP18Kw16Kj1ULA1VPP1XCK1JNg1Z5O1CBD13KC12BP1M5a1DBP1W12152A1QH21F5K1Y6Q1c251bKo1KKY1T5R1H3Z1ENg19Ng1NLo1ANg11Ng1aFm1R4J1ONg14091eA21BKt10AV1dDd1LNg1PNg0S951VIx1U3t1IKY1G0j1XPA16Na1QMU12Ir1CDp13A017GO1MBP1DIr1WH215Ir1YIr1ZD81JNg18A-1FNI1a6P1bDj1KNJ1TIH1H8q1ENg1N2p1ANg11Ng19Ng1R4J1PNg1LNg1dDd10901cAQ1eHD14091ONg1BD50S5317Og1I5a1GIC18Hp16OE1UNr1VHA1XML1JNg1ZM-1CPA13AQ12MU1M2A1DMU1WAx15CK1QOD1Y1c1F521cPA1bHV1KCg1TNg1HNg1ENg19Ng1NNg1ANg11Ng1a6Q1R4J1ONg14091eJ_1B5v100d1dDd1LNg1PNg0V9I1UHh16LA17Ad1GOn1I3S1S0f18Bl1X7B135b1ZA01CPA12PA1M2A1DA01WAx158r1JNg1QA01YOD1FK31cDp1aDR1bA91KEO1TNg1HNg19Ng1NNg1ANg11Ng1ENg1R4J1PNg1dFc10Et1BLZ1LNg14091ONg1e3A0S49178m1IG-1G6b18N916PN1UGy1VAD1QI-1JNg1CAQ13OH12AQ1M6Q1DI-1WH215Nz1YDp1ZI-1FBn1XIt1cM-1bEX1KNg1TNg1HNg1ENg19Ng1NNg1ANg11Ng1a3S1LNg1R2V1ONg14091eDQ1BJx10CD1dFc1PNg0S4u1VHi1U6V187Q1G531IID1XIt16Ac1QI-1M6Q1CAQ13Mx12AQ17HZ1DI-1WH215Nz1YDp1ZI-1JHd1aNg1ANg1K4m1TNg1HNg1EHd19Ng1NNg1FAd11Hd1bGJ1PNg1ONg14091e2S1B4710No1dFc1LNg1cM-1R2V0SPD1VOJ1U631X7B1GEs1IIg162C1QPA18Kd1CCu132512PA1M6Q1DPA1W5O15Nz1YD817Nk1ZPA1J6r19Ng1aGH1F8P1KBu1TNg1HNg1E6r1NNg1ANg116r1PNg1bGJ1ONg1R2V1LNg1d4J10OI1cM-1eDQ14091BLh072d1SEs1IPL1GDi180V169T1UKm1VKO1XMx13Jg1ZDp1CCu12Dp1M0G1DM-1WBD15Nz1JBF1QM-1FFO1YOD1cD81aBW1bGJ1K3m1TNg1HNg19Ng1NNg1ANg11BF1EBF1R2V1PNg1dFc102Q1BPe1LNg14091ONg1e6o0X5b1I291GOa185F166L1UKB1VKp1SIZ1QOD1YMy1CA013GZ17Bb12D81MBP1DOD1W5O158r1ZD81JNz19Ng1aPL1bGJ1K291TNg1HNg1ENz1NNg1ANg11Nz1PNg1F141ONg14091eN01BN2106g1dFc1LNg1cOD1R2V0VPE1UBz16Fr17Ii1G3f1I9V1SE1181-1XGZ13AQ1ZMy1CDp12MU1MBP1DMy1WH2152k1JI-1QMy1F9O1Y1c1cOD1bKe1K2Y1TNg1HNg1EI-19Ng1NNg1ANg11I-1aNp1R2V1ONg14091eNo1BBT105v1dFc1LNg1PNg0VMW1ULY16Oz17F51GIX1I9X1SD018IE1XPA13A01Z6P1CD8126P1MBP1D8r1WH215CK1JNR1Q6P1Y8r1FKu1cMy1aK51bKe1K8k1TNg1HNg19Ng1NNg1ANg11NR1ENR1R2V1PNg1dFc10MR1BBT1LNg14091ONg1eMY0SMN17BD1I8k1G0J18Hj16Mn1UF61V9I1XM-1J1V1ZCK1C1c13OD12CK1M6r1DKC1W0G15BF1QCK1YKC1F3U1c1c1b4F1K5p1TNg1HNg1E1V19Ng1NNg1ANg111V1a9V1R2V1ONg14091eDn1BGI10Mv1d4J1LNg1PNg0VBE1UGV168i173S1GI41IK51S7v18Ae1XM-13MU1ZCK1CNz12CK1M121DCK1W6Q155O1JEy1QCK1FB-1YIr1cNz1bHv1K9V1TNg1HNg1EEy19Ng1NNg1ANg11Ey1a2Y1R2V1ONg14091ePf1B3110AF1dFc1LNg1PNg0VPW1ULA161R172R1GEH1IGX1SFe18HC1XDp13MU1Z2k1C8r128r1MJV1D2k1WNJ15Ax1JEy1Q2k1YIr1FBr1cNz1aHO1bHv1KNp1TNg1HNg19Ng1NNg1ANg11Ey1EEy1R2V1PNg1dFc10CP1BGI1LNg14091ONg1e0r0SFV172R1IGX1G6W18Kh161n1U7U1V6T1XKC1JEy1ZBP1CKY13BF120G1MCg1D0G1WDR15121QBP1FBr1Y2A1c8r1bHv1KNp1TNg1HNg1EEy19Ng1NNg1ANg11Ey1aHO1R2V1ONg14091eAP1BKM10Jx1dFc1LNg1PNg0S7G1V441UF21IGX1GK91X1216JC1Q5a12Hd1CJV135a17G-1MOc1D3S1WCg15Cg1Y3S1ZJV1JEy18OD1F9g1a3m1bHw1KGX1TNg1HNg1EEy1NNg1ANg11Ey19Ng1R2V1PNg1LNg1dFc100u1cKC1eCP14091ONg1B9R0S7D17G-1INp1G8W18CL169S1ULr1VDZ1XNJ1JEy1Z121C6r136r12091MCg1D091WEf15091QJV1Y091F1z1cBD1bCR1KNp1TNg1HNg1EEy19Ng1NNg1ANg11Ey1aAl1R2V1ONg14091e111B1f10A11dFc1LNg1PNg0V3X1UM2160k17G-1G3v1I3m1SLa18Gn1X2A136Q1Z6r1C6Q125a1MEf1DDR1WDR155a1JEy1Q121Y5a1F2F1cBD1a5H1bCR1K3m1T9_1HPT19Ng1N981ANg11Ey1EEy1R2V1PNg1d4J10BB1BAg1LNg14091ONg1eLh0S9g17G-1IH91GKu18NL163B1UBn1VAK1Q4I1JEy1C6r13NJ12Ef1MCg1DEf1W0915091Y091ZNJ1F3i1X121cH21b8w1KBu1T5F1H8r1EEy19Ng1NLW1ANg11Ey1aNh1LNg1RMa1ONg14091eAg1BI910PR1d4J1PNg0SPd1VBn1UOg189v1G3_1IGH1X5a16Fx1Q5a1MOc1C4I13JV123S17G-1D3S1WCg15Cg1YOc1Z4I1JEy1aFM1ANg1KGH1TGY1H6H1EEy19Ng1NI91FMJ11Ey1b9w1PNg1ONg14091eN21B0t10KM1d4J1LNg1c6r1RMa0S8m1VAd1ULg1XJV1GLw1I2R16Fx1Q5a18J31C4I134I12Oc1MOc1DOc1WCg15Cg1YCg17G-1ZJV1JEy19Ng1aEO1FKU1K2R1TCN1H6z1EEy1N9e1ANg11Ey1PNg1b0a1ONg1RMa1LNg1d4J10BT1c3S1eGI14091BI907G-1S4o1ICg1G9O188P163U1UFx1V3B1X1213NJ1ZNJ1C6r12Ef1MCg1DEf1W0915DR1JEy1Q4I1FK31Y091cPT1a5a1bHE1KCg1TLo1H6s19Ng1NHo1ANg11Ey1EEy1RMa1PNg1d4J10BT1B3L1LNg14091ONg1e8t0X4I1I091GBn188N16J31U1K1VK31SMk1Q5a17Ef1C12134I12Cg1MOc1DCg1WCg15Ef1YCg1Z4I1JEy19Ng1aJV1FKr1K091TGN1HBf1EEy1N1o1ANg11Ey1PNg1b0a1ONg1R2V1LNg1d4J10311cEO1e1914091BBm0YOc17NJ1I5a1GHF18J016Me1UJ01V681SPc1QDR1Z5a1CJV123S1M3S1D3S1WOc15Oc1JEy1X5a1FBw135a1c3S1a121bO-1K5a1TPU1H171EEy1NNo1ANg11Ey19Ng1R2V1ONg14091e8z1BPR108t1dFc1PNg1LNg0VND1UGr167l1I4I1G7l1SBl18Iy1X091YHd1Z091CDR130912Hd1MEO1DHd1WHd15Hd17H21QEf1JEy1BBT1a6r1bFC1K121TDD1HBD1EEy1F461N7o1ANg11Ey19Ng1R2V1ONg14091eGm10191dFc1LNg1cCg1PNg0SD-1VLb1U161IJV1X4I1GCy163k1Q5a18DT1C12134I12Cg1MOc1DCg1WCg15Ef1YCg176r1ZJV1JEy1F8N1aNJ1K4I1TJ-1HPT1EEy19Ng1N9n1ANg11Ey1PNg1bO-1ONg14091eGm1B1V10O71dFc1LNg1cOc1R2V0V7A1U9U164l17Ef1G8U1I5a1S0c18BR1X2A132A1Z6r1C2A12DR1MEf1DDR1W09155a1JEy1Q121F1K1Y5a1c3S1bO-1KJV1TNg1HNg1EEy19Ng1NNg1ANg11Ey1a121R2V1ONg14091eGm1B1V10O71dFc1LNg1PNg0VE21ULt1678172R1GJq1IDR1S6A185o1XKY13KY1ZBP1CKY12121MDR1D121WJV15121JEy1Q6r1Y121F5C1c3S1a4I1bO-1KDR1TNg1HNg19Ng1NNg1ANg11Ey1EEy1R2V1PNg1dFc10O71BDh1LNg14091ONg1eGm0SAs172R1I091G8d18JF162E1U6U1VFH1XKY1JEy1Z0G1CAx13Ax12121MDR1D121W4I15NJ1Q2A1FKr1YNJ1cHd1b0a1KDR1TNg1HNg1EEy19Ng1NNg1ANg11Ey1aJV1R2V1ONg14091eGm1BI9108t1dFc1LNg1PNg0S4K1V1E1UP31I091G4n1XAx164n1Q6Q12NJ1CH213H2172R1M5a1DNJ1W4I15NJ1YNJ1Z0G1JEy18771FED1aJV1b0a1K091TNg1HNg1EEy1NNg1ANg11Ey19Ng1R2V1PNg1LNg1dFc108t1cHd1eGm14091ONg1BPR0SHq172R1IEf1G9l18Dt16Jp1U8D1VGQ1X5O1JEy1ZKY1CH2135O126r1M5a1D6r1W12156r1QBP1Y6r1F7i1cEO1b0a1KEf1TNg1HNg1EEy19Ng1NNg1ANg11Ey1a5a1R2V1ONg14091e8z1B0t106j1dFc1LNg1PNg0VBZ1U6S16BZ172R1G1O1IEf1S6618GB1XBF13BD1ZAx1CBF122A1MJV1D2A1WNJ152A1JEy1Q0G1Y6Q1FK31cHd1a5a1b0a1KEf1TNg1HNg19Ng1NNg1ANg11Ey1EEy1R2V1PNg1dFc101g1BDh1LNg14091ONg1e6j0SA617PT1IEf1GBh18M816Cj1UGz1V9J1XKC1JEy1Z5O1CIr13Ir12BP1M121D6Q1W2A15BP1QKY1YBP1FO01cOc1bO-1K091TNg1HNg1EEy19Ng1NNg1ANg11Ey1aDR1R2V1LNg1dFc101V1PNg1eI914091ONg1BGI0X6P17PT1IEf1GD216Ge1U2z1V9h1SEx1QH2120G1CCK132k1JEy1MNJ1DBP1W6Q15KY1YKY1ZBD1FO018ES1cCg1aDR1K091TNg1HNg1EEy19Ng1NNg1ANg11Ey1bFC1R2V1PNg1dFc10KM1LNg1eAg14091ONg1B6j0IEf1XOD1GKD18Fz16Am1UMm1V6m1SFK1Q2k12H21C2g13MU1M6r1DAx1WBP15H21YH217Cu1Z6P1JEy19Ng1aDR1FK31K091TNg1HNg1EEy1NNg1ANg11Ey1PNg1bOw1ONg1R2V1LNg1dFc102-1c091e3L14091B1g07P51SAS1IEf1GOV18Am163h1UAY1V6E1XCu13PA1ZOD1CDp12BF1M2A1DBF1WKY155O1JEy1QMU1FK31YBF1c5a1bIj1K091TNg1HNg1EEy19Ng1NNg1ANg11Ey1a5a1R2V1ONg14091eMb1BBT10BB1dFc1LNg1PNg0SLn1VN41UGP1I0918Ji1GJa1XML16F81QA012KC1CAQ13GZ1M6Q1DCK1WAx15BD1YKC17Gp1ZCu1JEy19Ng1a5a1K091TNg1HNg1EEy1F7i1NNg1ANg11Ey1PNg1b0D1ONg14091e6v1BDh103L1dFc1LNg1c4I1R4J0V8b1UJa1I0918Ln1GGl1SLH160L1X5b126P1Z1F1CML13Jg1M6Q1DNz1WAx15KC17Ml1QI-1JEy1Y8r1F5C1bLE1K091TNg1HNg1EEy19Ng1NNg1ANg11Ey1a4I1R4J1ONg14091eAF1BBB10471dFc1LNg1c6r1PNg0VCV1UDY165o175I1G2v1IDR1S0I18FF1XMx12My1ZML1C5b13Mx1M6Q1DMU1WH2152k1JEy1QGZ1Y1c1a121c2A1FBw1bLE1K091TNg1HNg19Ng1NNg1ANg11Ey1EEy1R4J1PNg1dFc10Jv1BLh1LNg14091ONg1e5l0S2n17861I5a1G9q185S168U1UJ21V0I1XIt1YMy1Z7B1CAE13AE12D81MBP1DDp1W5O158r1QJT1JEy1F461cBP1bNl1K091TNg1HNg1EEy19Ng1NNg1ANg11Ey1aNJ1R4J1ONg14091ePf1BJx10AP1dFc1LNg1PNg0VFy1ULX163q17Oh1GDm1IJV1S5c182O1XIt13It1Z8u1CAE12Cu1M0G1DI-1WBF151c1JEy1Q7B1F9v1YM-1c0G1b8w1KDR1TNg1HNg1EEy19Ng1NNg1ANg11Ey1a6Q1R4J1ONg14091eDJ1BLZ10671dFc1LNg1PNg0VKR1U4r161w173v1GPM1I4I1SOx18EK1XMD139d1Z8u1CIt12GZ1MKY1DML1WIr15MU1JEy1Q7B1YCu1F5n1cKY1a0G1b8w1K5a1T711HEf19Ng1NGG1ANg11Ey1EEy1R4J1PNg1dFc106g1BGw1LNg14091ONg1eKI0SCn17PB1INJ1GNn180Q16Hl1UEz1VBH1XBv1JEy1ZAE1CIt13Gg12Mx1MAx1DOH1WCK15M-1Q8u1FPX1YGZ1cAx1b3b1KJV1TH61HCu1EEy19Ng1N2u1ANg11Ey1aAx1R4J1ONg14091e4G1B6710LL1dFc1LNg1PNg0S0F1V3w1U3-1IBP1G5U1XMD16L81QOH12ML1C9d13Gg174y1M5O1DML1W2k15M-1YI-1Z7B1JEy18LK1FIu1a2k1bCR1K121T3A1H911EEy1NNK1A5a11Ey19Ng1R4J1PNg1LNg1dFc10CD1cBD1eCD14091ONg1BHI0SOY17511I5O1G0b18Ar161k1UDM1VJc1XOT1JEy1ZIt1CGg13MD12Cu1MBD1DI-1W6P15D81Q7B1YPA1FEw1cCK1b4s1K6r1TNT1HF21EEy19Ng1NHU1AH211Ey1aOD1R4J1ONg14091eN81B2b106k1dFc1LNg1PNg0V7Y1ULM16F_17AL1GG21ICK1S7t18791X1713171ZGg1COT12M-1MKC1DDp1W1c15D81JEy1QIt1YM-1FLx1cNz1aI-1b4F1K6Q1T4k1HAI19Ng1N6X1A2g11Ey1EEy1R4J1PNg1dFc10Cf1BHK1LNg14091ONg1e020SF117AK1I2k1GK618C216Ff1UBS1VKl1QJT1JEy1C9d13Fm12OD1MBF1DD81W8r15MU1YOD1Z8u1F5E1XFm1cMU1bGJ1K6Q1T6c1HJQ1EEy19Ng1NI51AJM11Ey1aGZ1LNg1R4J1ONg14091e0T1B1v105y1dDd1PNg0SFB1VI81U0l18Ns1G1l1I6P1X8u16NO1QJg1MH21CJT137B12My17Ah1DMU1WKC151c1YMy1Z251JEy1a5b1ABg1KBP1TPW1HAE1EEy19Ng1NDQ1FH411Ey1bA91PNg1ONg14091eM41BPW10HD1dDd1LNg1cDp1R4J0SNZ1V4a1UGd1X251G8K1INz16541QAQ183d1CJg1325122g1M0G1DMy1WBF158r1Y1c17I01ZGZ1JEy19Ng1aOH1FIq1KBP1T4X1H8r1EEy1NEN1AEM11Ey1PNg1bDj1ONg1R4J1LNg1dDd101v1cAQ1eI414091B5d07JU1S781I6P1GHT1837167A1UKg1V2e1XAE138u1ZMx1C7B12PA1M5O1DCu1W2k15MU1JHH1Q5b1FH41YDp1cAQ1aJg1b0E1KBP1T6p1H3S19Ng1NP51AFx11HH1EHH1RFc1PNg1dDd10KQ1BPW1LNg14091ONg1eEi0X4_1I2k1G8b188-16Fv1UEQ1V1e1SF81QIt17Nc1CFm13MD12251MKC1DMx1W1c15Cu1YML1Z9d1J1L19Ng1a1F1FJ01K6Q1TNg1HNg1EGm1NNg1A3211Gm1PNg1bG11ONg14091eGt1BDK10KQ1dLP1LNg1RFc1c1F0VMp1UAv1IKC18181GEq1S9D175Y169i1X06136H1Z4_1CJ-1M8r1DFm1WD815Jg1J8z1Y8u1QCT1FNc129d1c1F1aCu1bG11K6Q1TNg1HNg1E8z1NNg1ANz118z19Ng1RFc1ONg14091eB_1B81107S1dLP1PNg1LNg0V2o1U0Q16Eh1IBD1G4r1SGP18Ek1XIc1YMD1Z6p1C8B1323124_1M1c1DJ-1WPA15JT17OS1QJQ1JGR1BC71aM-1bG11K2A1TNg1HNg1F7G19Ng1NNg1A6q11OE1ELy1RDd1ONg14091e9Y10F41dLP1LNg1cI-1PNg0XGG1SAT1V8-1IH216FF1GB71Q2m1UEK1ZLU180g13GG12911MMU1DJe1W1F15Fm1YJ-175x1CO61JIB1a2g1K2A1b0E1TNg1HNg1E4g19Ng1AMt11241PNg1RDd1NNg14091ePC1BBy10IN1F561d011LNg1ONg1cPA0V0X1UDg16F-178N1G5z1IKY1SDH18AA1XHn1YAB1Z0C1C8q139_1MDp1D231W5b15CT1JEy1Q7r1FFD126p1cDp1a8r1b0E1K6r1TNg1HNg1ELI1NNg1AEy11D419Ng1RDd1ONg14091eCD1B1C10Bi1d011PNg1LNg0V0v1UEQ16Bs1IAx1GDY1SM8188-1XH01YJQ1Z9_1C8W13MT12231MPA1DNb1WOH15J-17Og1Q8q1JO71BHL1a6P1b0E1K2A1TNg1HNg1FIf19Ng1NNg1A1g11J01E3I1RLP1ONg14091eCD10N81d011LNg1cDp1PNg0SNP17Ev1VL71IH216Bd18Ok1G8p1U9p1X6z13Aj1C8312Nb1MAQ1D9-1W8u156H1J8t1Y8B1QMT1F7H1ZC61cDp1bG11K2A1TNg1HNg1EGb19Ng1NNg1AAg11JW1a1c1RLP1ONg14091eNo1B4G10CD1dLu1LNg1PNg0aMy1cDp1LNg1eHI109o1BHz1FHu1dLu1J8z18Go1I5O1G8g16921UOk1VAf1S7Z1XH5140917Da1ONg1R011PNg1ZCc1CBb13Mh129-1MML1DJY1WFm15061YIc1QIM1K2A1TNg1HNg1E4e19Ng1NNg1A1f119o1bKo0YNb1VKR1U0v1I8r18AT1GOr1SCU165S1X1J13Eb1Z9Z1CHr122m1MJg1D4q1WGg15JQ175C1QCc1J8s1ONg1aA01FBK1bA41KBD1TNg1HNg1EFe1NNg1AAg11IX19Ng1RLu14091c1F1eMY1BD5102Q1dBC1LNg1PCg0VMA1UBd1ID818Cn1GCV1SH116Hx1X8f1YF21ZA71C4z13NE12JY1M251DGG1WOT156p177j1Q9Z1J8z1ONg1aML1bEd1K1c1TNg1HNg1E5q19Ng1NNg1FOB11891A1g1RBC14091eEe1B0p109C1dKn1LNg1cMx1PNJ0SI21VBj1U4D1XFl1G8c1IAQ165c1QA718LH1C2x135I124q1MMx1D4P1WCT158B1YAI17Bn1ZF51JEy1FL51aJT1KA01TNg1HNg1EBJ19Ng1NNg1AEy110V1PAx1bB91ONg14091ePf1BLd10671dLq1LNg1cAE1RBC0VKs1U3o16E217M21GH81I5b1S2j18PS1X3213D41Z4z1C3j12O61MOH1D4P1W4_15231JNF1QHr1F5K1Y2m1cGg1b281KAQ1TNg1HNg1EJL19Ng1NNg1APY11MN1aFm1RKn1ONg14091eAJ1BJE10Dn1d701LNg1POg0VK81U7A169317Id1G9m1I7B1S2N18CF1XBG13Fl1Z1J1C2d12GG1MJT1D1m1WBv15Ic1JKM1QH51YJY1F241cCT1aBv1b5-1K5b1TNg1HNg19Ng1NNg1A4g110H1E0u1RKn1P8Y1d7010FV1BNo1LNg14091ONg1eDn0SPg179_1IGg1GIG189F16BZ1ULM1V7t1XNY1JEy1Z7_1C5I13BG12GG1M7B1D041WJ-15P51QF51FLk1YLU1cAk1bAn1KJT1TNg1HNg1EEy19Ng1NNg1A5i11Ey1a911RLq1ONg14091eGY1BJ610KI1d701LNg1PEy0SGB1VBZ1UPg1IOT1G2E1X2d16F11QMl12LU1C7_133j17N51MOH1DGG1W4_15231Y9-1ZH51JEy188T1FAN1aAB1bAn1KIt1TNg1HNg1EEy1NNg1AHh11Ey19Ng1RLq1PFp1LNg1d7010GY1c9n1ePb14EL1OGc1BOI0SNs17JZ1I4_1GN1183G16MV1UGB1VF11XN51JEy1ZBb1CH5134z12AI1M251DLU1WOT15JQ1Q6s1YNb1FL21c911b5V1KGg1TD81HG-1EEy19Ng1NM-1AKJ11Ey1a061RLq1OGc14HG1eNK1BBY10MS1d701LNg1PGf0VHy1UNs16JG17Nd1GE91IJ-1S5r18GM1XHr13A71ZCc1CBb12Nb1MJg1D9-1WFm15Je1JEy1QIM1Y9c1FLD1cAB1aJR1bC11KCT1TKu1H2A19Ng1NB61A0j11Ey1EEy1RKn1PIy1d70100r1BM01LNg14OA1OGc1eGw0X9Z1IAB1GM_186e16Aq1UCJ1V5f1SFX1QGp179a1CCc13Mq12IY1M1F1DP51W8u150K1YJR1Z6f1JEy1FAR1a9c1K0K1T491HOH1EEy19Ng1NEu1A3s11Ey1PMu1b9x1ONg14HG1eMR1BEe10LG1d701LNg1cJQ1RKn0VON1UNZ16Mc17Im1G721I6p1S4p18Ba1X0w13Aj1Z991C5Q12AB1MCu1DIY1WOH15CT1JEy1QH01FKS1Y6H1c231b9u1KJe1TLL1H861EEy19Ng1NMI1AMr11Ey1a9-1RKn1ONg14EL1e1R1B9C10NK1d701LNg1P2J0V2I1U7e16PJ179Z1GEg1IIc1S7y18Jj1XCL13Gp1ZMT1CFN12J-1MM-1DJe1WJg15Gg1JEy1Q8W1Y4_1FK91cNb1a4q1bGK1KIY1TBm1HH419Ng1NLz1ANg11Ey1EEy1RKn1P6O1dLq10671BFV1LNg14091ONg1eP00SHM17MZ1IIY1GJs18O116PF1UNS1V8F1X8W1JPC1ZMB1CHP13Ck12CT1MM-1D0K1WML159d1QKG1FB01Y171c9c1b571KAB1TMY1HE01EPC19Ng1NE61ANg118X1aJY1RBC1ONg14091eDn1BD510BY1dLq1LNg1P4c0S2y1V1Q1U081IJe1G2y1X9j162y1Q2m12MD1C1m139j173_1MD81DCT1WGZ15AE1YGg1Z4q1J7h18081F2L1a9-1bC11KJ-1TMn1H891E7h1N4V1ANg11Lk19Ng1RBC1PEm1LNg1dKn10CD1cIY1eKI14091ONg1B3Z0SAM17If1I9n1GAM18BX16AM1UAM1VAM1X2m1J0P1Z9c1CF213AI12Fm1MOD1DGg1W1F157B1Q6p1Y9d1FH61cJQ1bAn1KMD1TEN1H0e1E0P19Ng1NGA1ANg112_1aNb1RLu1ONg14091eFe1BM4100T1dKn1LNg1PIi0V5W1U9f167k175n1GFj1IFm1SBX18BL1X2m139-1Z8B1CNb12AE1MNz1D9d1WM-155b1J5Y1QJR1Y7B1FPH1c9n1a6H1bGs1KJT1T1m1H8W19Ng1N9a1ANg11GL1E5Y1R011P8W1dBC10CD1BJL1LNg14091ONg1eBi0SBX17Mk1IJg1GMG18Dk165B1U8C1VBL1XAI1JLv1Z6p1CIc13F2127B1MIr1DAE1W1c15I-1Q061Y251FJD1c171bB91KAQ1TNg1HNg1ELv19Ng1NNg1ANg11OA1aIt1RLP1LNg1dLu10FV1PAE1e1C14091ONg1BLd0XF217Pd1IM-1G6d16Nv1UFE1V8C1SGW1QAB12OH1C8B13P51J3K1MKY1D7B1WIr15D81YGZ1Z061FLx18K11cAE1aI-1KOD1TNg1HNg1E3K19Ng1NNg1ANg113K1b9s1RLP1PNg1d0110NK1LNg1eDn14091ONg1BG007Pd1XP51I2k1G6y166J1U341VLc1SC81Q6H12251C6p139c1MAx1DOH1WCK15D81Y1F1JOS1ZJe1F5618BQ1cJT1KKC1TNg1HNg1EOS19Ng1NNg1ANg11OS1PNg1bA41ONg1RDd1LNg1d0110Ee1a2g1BCP1eKI140907Pd1I0G1G2D18FI16BM1UE81VLc1S4d1X8B1Q9n1Z911CJR12Jg1M5O1D251W2k15M-1JOh1YAQ13IY1FKW1c251a5O1bIp1KBP1TNg1HNg19Ng1NNg1ANg11Oh1EOh1RFc1PNg1dLP10FV1B1h1LNg14091ONg1eFe0XJQ1IDR1G3a18EG169z1UK_1VLc1SA_1Q0K17Pd1CJe13JR12GZ1MBF1DJg1W6P15M-1YI-1Z9n1JKC1EKC1a121K091TNg1HNg1FBw19Ng1NNg1ANg11KC1PNg1bKo1ONg14091eA81B0u102Q1dDd1LNg1cJg1RFc0VDy1UJI16MM17HG1G4Q1IHd1SOW189A1X4_134_1ZOT1C1712Cu1MBF1DAQ1W2k15OD1J8u1QMD1FNL1YA01cML1bG11KEO1TNg1HNg1EPA19Ng1NNg1AKC11CK1aEf1R4J1ONg14091e8x1BLh10HL1dDd1LNg1PNg0V8R1UFd16BQ17Lw1G2q1I5J1S3l18LC1X8u138u1ZJT1C7B12D81M5O1DDp1WCK15My1JP51QOH1YOD1aPT1cGZ1F0P1b0E1K5J1TNg1HNg1EAE1NNg1A7B118r19Ng1R4J1PNg1dFc10N81BLh1LNg14091ONg1eC70S6C1IAa1G6n1Y2g16Om1UJu1VDE1XGZ17AK1Z1F1CGZ13GZ122g1MH21DMy1WKC15Nz1QAQ1JCk18E-1F3x1bDj1KAa1TNg1HNg1E9119Ng1NNg1AIc116P1aAO1R2V1ONg14091eGD1BLh10KV1dFc1LNg1c1F1PNg0VGQ1UAb160R17441GJX1IGH1SOu18Jb1X5b12D81ZAQ1C1F13ML1MKY1DD81WIr151c1JIl1QI-1F3x1YMU1cI-1bHV1KAa1TNg1HNg1EN519Ng1NNg1A3V119d1aAO1R2V1ONg14091e3A1B6v10No1dFc1LNg1P2R0VLb1UF0161T17JM1GO_1IGH1SEP187I1X7B13251ZI-1CGZ12PA1M0G1DPA1WBF151c1JHu1QCu1YD81F8m1cCu1aFM1bA91KAa1TNg1HNg19Ng1NNg1ALg11711EMr1R2V1PEO1dFc10OI1BA11LNg14091ONg1e8I0S3Y179j1IGH1GC418CE16Ih1U2E1V0Y1X9d1JGy1ZAQ1CGZ13OH121F1M6Q1D1F1W5O151c1QAQ1F8m1YA01cPA1bEX1KAa1TNg1HNg1E7419Ng1NNg1A24118W1aFM1R2V1ONg14091ePC1BDV10021d4J1LNg1PHd0SOO1VGi1UAX1IAa1GBI1XMD16Cy1QGZ12ML1CJg138u17KG1M6Q1DML1W5O152g1YPA1ZGZ1JJr185g1FMJ1aFM1bEX1KAa1TNg1HNg1EKr1NNg1A9H117r19Ng1R2V1PEO1LNg1d4J10Do1cA01e3Z14091ONg1BPe0SCe17Bf1IAa1GJF18N_162E1UP81V6w1XCT1JJW1Z5b1C2513It125b1MBP1D5b1W5O15My1QJg1YI-1FPd1cA01bEX1KA51TNg1HNg1E3g19Ng1NNg1ADI114q1aID1R2V1ONg14091eN01BGA10GY1d4J1LNg1P2R0V371U0m162617MB1G6w1IA51SDb187m1XBv13Fm1ZOH1C7B12Mx1MBP1DMx1WBF15MU1JIo1QMx1Y1F1FHG1cDp1a4m1bGJ1KA51TNg1HNg19Ng1NNg1A95119c1EMe1R2V1PNg1d4J10Dn1BBB1LNg14091ONg1e2i0S3717981I5J1G7L188b16Eo1UOr1V4H1XBv1YGZ1Z9d1CGg13MD12Mx1MAx1DOH1WKC15D81QIt1JP11FLg1cA01bEX1K5J1TNg1HNg1E6l19Ng1NNg1A1X11Ii1aPT1RMa1LNg1d4J100r1PNg1e1C14091ONg1BGA0X9n177D1I3S1GK216FP1U2T1VMH1S5L1Q1712251CBv13Ak1J671MBF1DOH1W6P15A01YML1Z4_1F7j184r1cPA1a091K3S1T6s1H711EBx19Ng1N4b1ALL11DO1bEX1RMa1PNg1d2V10Mv1LNg1e6714091ONg1BDV0IJV1XJQ1G7g18N-162v1U0g1V8g1S8l1Q9n12251CAB13JR1MKC1DOH1W2g15Cu1YJg17C61Z6H1JEy19Ng1a6r1FEv1KJV1TAc1H1Z1EMt1ND31AEy116q1PNg1bEX1ONg1RBq1LNg1d2V107p1cI-1eET14091BA107FN1SJz1I6Q1GBj185X166t1UEA1V7Z1XIY136p1ZAB1CJQ12OH1MNz1D7B1WM-15ML1JEy1Q9n1FPX1YMx1cDp1bKe1K6r1TLB1H8E1E8119Ng1NLT1AEy11AD1aH21RBq1ONg14091e1S1BJx107p1d2V1LNg1PP90SLX1VB51UKZ1IH2187X1GDY1X9c16LK1QAB128u1C8B13231MMU1DAE1WAQ15OH1Y7B17Lr1ZJQ1JEy19Ng1aCK1KKY1TFZ1HOz1EGw1FOS1N9b1AHH11OC1PH41bHv1ONg14091ePI1BET107p1d2V1LNg1cMU1RBq0VH-1UN41IKC187M1G481S1i16611XP512It1Z8B1CP513P51MA01D9d1W5b15It17Gp1QJQ1JEy1Y9d1F561bHw1KBD1TKq1H641EHH19Ng1NKZ1AHH11191a2g1RMa1ONg14091e9R1B1R10Jx1d2V1LNg1c6P1PGx0VOR1UGz165z17131GFv1I6P1SFA18LX1X23127B1ZJQ1C8B13231MD81D8u1WGZ157B1JO71QJe1Y8u1aA01cMy1F1r1b4F1KIr1T4C1HCh19Ng1N6Y1AEt11MY1EA11RMa1PH41d4J10HX1BJE1LNg14091ONg1eCP0S5j17O81IMy1G1_18KT16O51UHl1VBj1X8B1YOH1ZJe1C6p13IY12Mx1MMU1DOH1WI-15251Q9n1J0u1F1b1cDp1bGJ1KCK1T8H1H2U1E1j19Ng1N8G1A1d11DK1aML1R2V1ONg14091eEH1B0T10Pb1d4J1LNg1PP90V421UHS16Dm17L01G501IM-1S4f18KH1X8B13IY1ZAB1C6p12Jg1M1c1D5b1WDp15ML1JDo1Q0K1FL51YJg1cI-1bHV1K8r1TIa1HGk1ELV19Ng1N6L1AI111NC1aJT1R2V1ONg14091eNK1BOX10KI1dFc1LNg1PNg0V8l1UCV165h172_1G1W1INz1SHg187d1XIc13231ZJe1CIY12Mx1M8r1DMx1WD8151F1J6L1Q9n1Y5b1FLx1cPA1aI-1bA91KIr1TMT1HMy19Ng1N1J1A7N112J1E7P1R2V1PPT1dFc101C1BBy1LNg14091ONg1eEe0SFv171m1IIr1GJz18Mj161N1U611VFF1XNb1JIF1ZJe1C8B13Ic12JT1MCK1D7B1WMy15AQ1Q6H1F561Y251cM-1bEX1KH21TNg1HNg1EKm19Ng1NNg1A2P11Lk1a2g1R2V1ONg14091eBY1BPb106g1dFc1LNg1PHd0SLn1VMf1U3y1I0G1G451XF216FF1QAB128u1C2313Nb17BP1MBD1DIt1WNz15I-1YMx1ZJR1J3s183E1FKW1aBF1bGJ1KBP1TNg1HNg1ELx1NNg1AKa11Ad19Ng1R2V1PCg1LNg1dFc10Dn1cOD1e0214091ONg1BPI0SEl17Jg1I6Q1GH-18C5162T1UDF1VAY1X2m1JIX1Z6p1CIc13F212It1MBD1D9d1WNz15I-1QJe1YOH1FPX1cM-1bEX1K2A1TNg1HNg1E5M19Ng1NNg1AKS11Hp1aAx1R4J1ONg14091eAi1B4710P01dFc1LNg1P0G0VFK1UCs16IT17IY1GMf1INJ1SG7188M1XLU132m1ZIY1CNb129d1MBD1DGg1W1c15AQ1J4e1QJQ1YJT1FNW1cA01a0G1bHV1KNJ1TNg1HNg19Ng1NNg1A3F113J1EDQ1R4J1PNz1dFc101S1BNF1LNg14091ONg1e5l0XGG1I4I1GNy18Bt16HR1UBc1V3c1S841Q2317HP1CF213LU12Gg1MBD1DOT1W1c151F1Y7B1Z9c1JEy1FPG1a2A1KJV1TNg1HNg1E8s19Ng1NNg1A8t11311PI-1bDj1ONg14091e9R1B1f10Mb1dDd1LNg1cCu1R4J0VOU1UA3165Z17Ot1GKZ1IH21S5T18DF1XKG13041Z9-1CO6124_1M8r1DJ-1WM-15Mx1JEy1Q711FBA1YGg1cAQ1bG11KAx1TNg1HNg1E1919Ng1NNg1A1911GI1aKC1R4J1ONg14091eLh1BAF100u1dDd1LNg1P2k0V7M1U5T160X174A1G2O1I1c1SPO18381X8q13Bf1Z4q1C9j129n1MMy1D911WAQ15It1JEy1QJY1Y4_1F7G1cML1aM-1bKo1K6P1TNg1HNg19Ng1NNg1AGm111V1EO71RFc1P121dLP101h1BLZ1LNg14091ONg1e0u0SM817HZ1ICu1GDH18FW16I61UPO1VMQ1X981JEy1Z9j1C0C13Hn12Je1MA01DJQ1W2515171Q4P1FH41Y6H1c251bIp1KDp1TNg1HNg1E8t19Ng1NNg1AEy11Dh1a5b1RFc1ONg14091e1f1BHX107p1dLP1LNg1PNg0SOo1VKz1UOR1IDp1GKT1XDZ163w1Q0C12061CL413De17MX1MA01D6p1W2515CT1Y6H1ZHn1J9o18M81FJ01a1F1bOl1KD81TNg1HNg1E7v1NNg1A3N11PD19Ng1RDd1P2R1LNg1d0110G01c5b1e2K14091ONg1BEH0SLN17L-1IOD1G2M18LH16Oj1UH11VHx1X6f1JKy1ZDe1CLr138312JQ1MA01DIY1W2515CT1QL41Y911FNc1cML1bIp1KMy1TNg1HNg1E1U19Ng1NNg1A3z110z1aCu1RLP1ONg14091eFR1B5l105l1d011LNg1PHd0VOj1U7m169K17AK1G751I2g1S4f18Ib1X9Z13Mq1Z831CFa126p1MA01D231W2515CT1J5a1QLr1YAB1FLp1c1F1aDp1bIp1KNz1TNg1HNg19Ng1NNg1AG-11EO1EDR1RLP1POc1dLu10Gw1BLZ1LNg14091ONg1e0r0XBb1IMy1G5818Hl169r1U3P1VPM1SFk1QGp178P1CCc130q12231MCu1DP51WOH15Ak1YJQ1Z6f1JBb1FNw1aDp1K1c1TNg1HNg1EP519Ng1NNg1ADZ11KY1PHd1bOl1ONg14091eP01B4L10AP1dLu1LNg1cGZ1R010V6I1UNn165c17Bg1G8c1IMy1S1W18411XMl13Be1ZIM1C6s12Nb1MAQ1D9-1W8u156H1J4W1QEj1F1r1Y8B1cML1b7x1K1c1TNg1HNg1ENE19Ng1NNg1A3T11M-1aA01R011ONg14091eGw1B4L10EH1dBC1LNg1P2R0VLH1UBs16En17Fx1G5j1IMU1S7d18D11XA713Ml1Z0w1C0q12AI1MGZ1DLU1WIt15Je1J681Q831YIc1FBK1c5b1aPA1b9s1K2g1TNg1HNg19Ng1NNg1AHc11It1EK41RLu1PNg1dBC10FR1BLi1LNg14091ONg1eAP0S1a173x1IPA1G5_18MH16M11UNn1VIJ1X4z1JAo1Z0q1CMh13F512JY1MJg1DGG1WGg15JQ1QFa1FH71Y711cJT1bEd1KM-1TNg1HNg1EDD19Ng1NNg1ACS113X1aJg1RLu1ONg14091eMR1BP010MR1dKn1LNg1PNg0S0F1VO51U6I1IGZ1GFk1X3j16Oj1QBe124q1C1J132x170P1MMx1D4P1WCT158B1YAI1ZMh1JCH18Co1FFn1a8u1bFL1KI-1T991H5Q1EKE1N5s1A9E115R19Ng1RLu1PNg1LNg1dKn108V1cIt1eLf14091ONg1BAi0SIv17GT1IOH1G2f183u163o1UO51VM11XBG1JLL1Z1J1COt13Fl12C31M7B1D9j1WJ-15P51QHr1YLU1F0Z1cMD1b8j1KML1TO41HJJ1E0J19Ng1N7J1AB111Ep1aOT1RLu1ONg14091eLG1BMY10MS1dKn1LNg1PNg0V7g1U5P163D17Fx1G4B1IOT1SE_18EW1XD4132d1ZF51C2x12GG1M7B1D1m1WJ-15P51JET1QA71YJY1FLk1c0K1a911b5-1K9d1TDo1HIn19Ng1N351AGE113F1EIA1RBC1PNg1dKn10Lf1BBY1LNg14091ONg1e5l0XOt1I911GN_18L816H81UHS1VKs1S9K1QMl17Ku1C7_138f12O61M8u1D4P1WAk15P51YJY1ZH51J0t1FAR1a9c1KAk1TH31H9t1E5v19Ng1NOM1AJh113Z1PNg1b5V1ONg14091eJx1BGY10FR1dLq1LNg1c061RBC0VDw1U3716Nq173T1G1G1I9c1SE418BU1XNE137_1ZA71C4z124q1M8u1DGG1WAk15P51JEy1Q9Z1F0s1Y2m1c9c1b9u1K6p1T8H1H8O1EEy19Ng1NBk1A2Q11Ey1aLU1RKn1ONg14091eDV1BLl101S1dLq1LNg1PNg0VJc1UCM16Hb17Il1G9q1IIc1S5D182Z1X3j132x1ZHr1CN512O61MAE1DC31W0K15Nb1JEy1QBb1YJY1FCS1cP51a4q1bGK1KIY1TO71HD919Ng1NKP1A3O11Ey1EEy1RKn1PNg1d7010151BLl1LNg14091ONg1e6v0SM617Gn1IP51G0x181G16HW1UNq1V7L1X2d1JEy1ZD91CNE133j12GG1MAE1D4P1W0K15Nb1Q8_1FK91YLU1c711b2h1K8B1T1t1HJe1EEy19Ng1NF71AJN11Ey1aO61RKn1ONg14091eLh1BLl10G01d701LNg1PNg0SD61VEo1UHb1I711G401X32162r1QMh12C31C3j13D417Nx1MIt1D041W9n15711Y4q1ZEb1JEy180b1F871aGG1b9P1K9c1T031H6Q1EEy1NNc1AJn11Ey19Ng1RKn1PNg1LNg1d70104L1cF21eNF14091ONg1BLl0S5g178S1IF21G3Q180x168J1U4N1VKk1X131JEy1Z1J1C5I13JM124P1MIt1D9j1W9n15F21QHr1YO61FIy1cAI1bLJ1KIc1TMD1HPT1EEy19Ng1NCT1AAu11Ey1aC31RKn1ONg14091e1h1BLd10ET1d701LNg1PNg0V9m1U2r166_174o1GCl1I9-1SK718J91XAH13Ii1ZNE1CBG121m1MIt1D6Z1W6H159-1JEy1QD91YGG1F361cJY1a4P1bCX1KP51TNg1HNg19Ng1NNg1AA711Ey1EEy1RLq1PNg1d7010Mv1BLd1LNg14091ONg1eJA0XIm1IAI1GBp18Lm16AZ1U8J1VCa1SEE1QEb17FO1CEL13GF12041M9d1DKG1W6H159-1YC31Z3j1JEy1F6l1a041KNb1TNg1HNg1EEy19Ng1NNg1ANg11Ey1PNg1bCi1ONg14091eAF1BLd10FR1d701LNg1c4q1RLq0V551UEE16Gv173i1GFT1IAI1S2t186_1XIi13NY1ZN51CFl121m1MIt1D6Z1W9n15F21JEy1QD91FGq1YGG1cO61b3W1KNb1TNg1HNg1EEy19Ng1NNg1A6z11Ey1a041RLq1ONg14091e4L1BFV10MR1d701LNg1P8r0VGv1U2t16Ap17AK1G6M1IAI1SMg181I1X3213D41Z4z1C3j124P1MAE1D9j1W0K15711JEy1QHr1YO61FIE1cGG1a9j1bG91KNb1TNg1HNg19Ng1NNg1AKu11Ey1EEy1RLq1PMD1d4S108V1BDo1LNg14091ONg1eEH0SDS173x1IAI1GJF18G216Kl1U1O1VCE1X5I1JEy1ZF51C2x132d12C31M8u1D041WAk15Nb1QA71FH_1Y4q1cC31bG91KP51TNg1HNg1EEy19Ng1NNg1AAt11Ey1a9j1RLq1ONg14091eLf1BLL10MS1d4S1LNg1PO60SNA1VB41UGi1IAI1G0o1XOt16GM1QMl12GG1C7_138f17JK1M7B1D1m1WJ-15P51YJY1ZH51JEy188e1FF61a6Z1bG91KP51TNg1HNg1EEy1NNg1ACQ11Ey19Ng1RLq1PGp1LNg1d4S10Ld1c4P1e5v14091ONg1BHI0SB317Em1IAI1GMV18NA16IW1ULR1VHJ1X8f1JEy1ZMh1C1J13NE12O61M7B1D4P1WBv15Ic1QBe1Y2m1F7N1c4P1bDf1KIc1TNg1HNg1EEy19Ng1NNg1AMN11Ey1a6Z1RLq1ONg14091eDn1B9o10Dx1d4S1LNg1PNE0VDA1U8n16N317GT1G2l1IAI1SMK18N11XNE13N51Z8_1CF512LU1MJT1DC31W4_159c1JEy1Q0q1YAI1F3H1c1m1aKG1bDf1KIc1TNg1HNg19Ng1NNg1AIL11Ey1EEy1RLq1PJd1d4S102Q1BJL1LNg14091ONg1eFV0XF51I9-1G8018G316Jf1UJG1V3d1SGd1QFa17AK1CA713H5122m1MMx1D4q1WCT15IY1YF21ZMq1JGm1FH_1a6Z1KIc1TNg1HNg1E8t19Ng1NNg1AOi11I91PMw1bDf1OM3142g1eGY1B9o10JE1d4S1LNg1c4P1RLq0V4t1U82161A177w1GBa1IF21S3r18FX1X8_13Ml1Z6z1C9Z129-1M251DJY1WOT15JQ1J8t1Q5Q1FGq1YNb1cC31bG91K9c1TNg1HNg1EI919Ng1NNg1AK-119R1a041RLq1OM314It1e9C1BHI101C1d4S1LNg1P4A0V8h1U9G163p176B1GKi1IF21SLj18IO1X0q136s1Z5Q1CFa12Nb1M5b1D9-1WGg15061JBT1QLr1Y9c1F361cO61a1m1bG91K9c1TNg1HNg19Ng1NNg1ANi11Jv1EGA1R701PLa1d4S10FV1BLL1LNg14231OM31eLd0S7e17K41I711GDG180M16Lb1UKN1V0y1X6z1JN21ZLr1C6f130w12Ic1MML1D711WFm15AB1QH01FIy1Y8B1c4q1b3W1K231TNg1HNg1E1f19Ng1NNg1AHi111R1aC31R701OM3148B1eDn1BDo109C1d4S1LNg1P7V0S2H1VJt1U7-1INb1GIU1X8316Aw1QL412231CLr13Ej17PZ1MGZ1DIc1WIt156H1Y6p1ZH01JMb18JS1F0e1aGG1b3W1K231TNg1HNg1ECP1NNg1AGy11Ee19Ng1R701PAy1LNg1d4S10DJ1cLU1ePb148B1OM31BFV0SKK17Gk1IP51G7z18EF161B1UB81VOs1X991J1h1Z8W1CH013FN126p1MAQ1D231W8u150K1QHP1Y061FK91cJY1bCi1K8B1TNg1HNg1E5l19Ng1NNg1AJn110p1aO61R701OM314IY1eIP1BLd10Pb1d4S1LNg1PIV0VOd1U9y16Fq17NQ1GF31I231SJH181s1XIH13L41Z8q1CNV12061MAQ1DJQ1W7B15J-1J1f1Q7r1Y911FK91cAI1a4q1bCX1KJR1TNg1HNg19Ng1NNg1AJJ11Ee1EJv1R701P9a1d4S10Bi1BKV1LNg148B1OG61eFh0X9_1IIY1GII186u16II1U6u1VO31SII1Q4P17AL1C0C138q126H1MI-1DAB1WJT154_1Y9n1Z9j1JMb1FN91a4q1K6H1T6p1H1F1EJA19Ng1NGp1APH111R1P131bLJ1OG6149c1eN01B8x10BN1d4S1LNg1c9-1R700VL_1UNm16DU17MX1GDU1IJR1S4-185G1X9j13041Z4q1C1m12Ak1MCu1D9n1WOH15171JBm1Q2m1FN91YJ-1c711b9P1KJ-1T7E1HMX1E9R19Ng1N9N1AAN11Jv1a4q1RLq1OG614P51eC71B9710GD1d4S1LNg1PEj0VLO1UPF16Js173x1GJs1IAB1SHs18LC1XLU13LU1Z711C2m12CT1MPA1DBv1W2515MD1JDh1QIc1YCT1FN91cNb1a4q1b2h1KOT1TA81HJn19Ng1NI_1ALv119R1EBm1RLq1PP51d4S10HK1B7S1LNg14Nb1OG61eFp0S9L17Og1I6H1GL318NU16MO1U7C1VFd1X711J6j1ZIY1CP5137112MD1MA01DOT1W5b15Fm1QJR1FCS1YMD1cIc1bGK1KIt1TGu1H361E1g19Ng1NEC1ALD11I91a4q1RLq1OG614711e1v1B6210M91d4S1LNg1PPA0SHB1V9k1U1p1IAk1G0O1X2316C_1Q9n129d1CIY138B17031MDp1DFm1WJg15It1Y9d1ZJe1JEy18LQ1FCS1a4q1b9u1KJT1T3C1H4O1EEy1NF91AEU11Ey19Ng1RLq1PNg1LNg1d7010OC1c231eNj14F21OG61B960S2W177K1ICT1G2W182W16C_1U2W1V2W1XJQ1J4e1Z9n1C0613JQ12OH1MMU1DJT1WCu15251QBv1YOH1FKS1c6p1b571K5b1TCm1HBn1E1j19Ng1NKb1A20113A1aF21RLq1ONg14MD1e3f1BIX10691d4S1LNg1P5I0V2c1U9W16C_177G1G2W1IGg1S6518JX1XAB13911ZBv1C9n12ML1M6P1DJg1WD815AQ1JDJ1Q171YML1F7E1c061a9c1bC11KGZ1T2i1HME19Ng1N7q1A6x117O1EPC1RLq1PEI1d4S10691B5w1LNg14MU1ONg1eAV0XJ-1IAE1GC_18Ov16C_1UP61V8a1SAG1QIt17BK1CCT13Bv12Cu1MIr1DCu1WNz15M-1YPA1ZFm1JEe1FEU1aJQ1KCu1T0s1H4_1EGD19Ng1NKm1AFt11GS1P7Q1b5V1ONg14091eCH1B5d10Oa1d4S1LNg1c911RLq0VOv1UKF162W17Lx1G651IOH1SO218FY1XFm13It1ZMx1C8u12OD1MAx1DD81WIr151c1JGw1Q5b1FLk1YMU1c0K1bAn1KM-1TP51H5a1EAW19Ng1NC31A3e11OB1a911RLq1ONg14091eIz1BNj10FQ1d4S1LNg1P3N0V7C1UD7162W175E1GKx1IML1S4i185m1X5b13Jg1ZI-1CGZ12Nz1M2A1DNz1WKY15Ir1J9R1QPA1Y8r1F4X1c4_1aJ-1bDP1KMU1TNg1HNg19Ng1NNg1AIZ119t1EM01R701PFp1d4S10FQ1BPW1LNg14091ONg1eLy0SHk17H41II-1GCr18Jl162W1UFg1VOy1XDp1JEy1Z2g1COD13M-12KC1MJV1DKC1WNJ15KY1Q1c1F0Z1YBF1cOT1b5-1KNz1TNg1HNg1EEy19Ng1NNg1A6911NV1aOT1R701ONg14091e3J1BFr10CH1d4S1LNg1PEy0SE31VHB1UFY1IAQ1GI71XOD16Fo1Q8r12BD1C2g13My17Ev1M5a1DIr1WNJ150G1Y5O1Z6P1JEy184R1FD_1aGg1b5-1K2g1TNg1HNg1EEy1NNg1AG_119t19Ng1R701PEy1LNg1dPQ10DL1cGg1eOC14G51OCv1B810S1x17Br1IAQ1G3R18Fo16Kf1U101VJI1X1c1JEy1Z2k1C8r13Nz12BF1M5a1DBF1W1215BP1QCK1YH21FER1c9d1b5-1KOD1TNg1HNg1EEy19Ng1NNg1AGD11OB1a9d1R4S1OCv141K1ePW1B5y10G_1dPQ1LNg1PEy0V4T1U3a167F177s1GHm1I1F1S1y18Ct1X6P132k1ZIr1CKC12H21M5a1D5O1W12156Q1JEy1QBD1YAx1FDD1cAE1aIt1b5-1KM-1TNg1HNg19Ng1NNg1AEt11GS1EEy1R4S1PEy1d4v101u1BJ61LNg14E71OCv1eDK0X8r1I1F1G9t187Q164y1U7E1VFJ1S8m1Q5O178f1CBF13CK12Ax1MDR1DAx1W4I152A1Y0G1Z5O1JEy1FFn1a8u1KA01TNg1HNg1EEy19Ng1NNg1ADJ117O1PEy1bGs1OCv14E71eP11BDo105y1d4v1LNg1c7B1RPQ0V5M1U9B166-174P1G631IGZ1SMs18C-1XCK13Ir1ZAx1C5O120G1MDR1DKY1WJV156r1JEy1QKY1FL51YBP1cOH1bGs1KI-1TNg1HNg1EEy19Ng1NNg1AG0113A1aJT1RPQ1OCv14E71eGD1BLG10Cf1d5e1LNg1PEy0VNj1U0H16IQ17My1GK-1IML1S3F186o1XIr13BD1Z0G1CH212BP1M091DBP1WJV156r1JEy1Q0G1Y6Q1FIq1c251aOH1bGs1K1F1TNg1HNg19Ng1NNg1APR11Ey1EEy1R4v1PEy1dHt10OI1B7p1LNg14E71OCv1e4w0S2s17D81II-1GAR18EY165i1U7l1VH_1XD81JEy1Z1c1C2g13MU12CK1M6r1DCK1WBP15BF1QNz1F6K1YIr1c1F1b8j1KCu1TNg1HNg1EEy19Ng1NNg1A9R11Ey1aJg1R4v1OB914B11e4G1B7p10BY1d5e1LNg1PEy0SEv1V6q1U5x1IA01G8N1XAE16Mk1QML12D81COH138u17A01MAx1DM-1WIr151c1YMU1Z5b1JEy18PX1F681a1F1bFL1KM-1TNg1HNg1EEy1NNg1A1S11Ey19Ng1RPQ1PEy1LNg1d5e10MS1cPA1e1C140T1OB91BJx0SKu17I-1IOD1GKu18DB16JO1UDB1VCq1X6p1JEy1Z0K1CJe13JR12GZ1MKC1DJg1W1c15PA1QBv1Y1F1FFi1cOD1bEd1KMU1TNg1HNg1EEy19Ng1NNg1AGw11Ey1aPA1RPQ1OB914HX1e941BJx10MR1d5e1LNg1PEy0V7s1UMC16Ka17GZ1G4b1I2g1SKa18MZ1XO6134q1ZNb1C2m12AE1M1c1D9d1WA015251JEy1Q231Y7B1F7G1c1c1aM-1b9s1K1c1TNg1HNg19Ng1NNg1AMS11Ey1EEy1RPQ1PEy1d5e10Jv1BJA1LNg14HX1OB91eLZ0XHn1I8r1G7R18ME16P41U2w1VO91SCO1Q4P175b1C0C139_12Bv1MM-1DAk1WML15Fm1YCT1Z6Z1JEy1RPQ1aMy1K2k1TNg1HNg1EEy19Ng1NNg1ADx11Ey1PEy1bOl1OB914HX1eLh1BJA101f1d5e1LNg1cCK1FHu0VBG1U5I16Du17OH1GAH1IKC1SEL182d1XGp13Lr1ZMT1CFN12JR1MAQ1DIY1W8u15Ak1JEy1Q8W1FL61YJe1c5O1bKo1KIr1TNg1HNg1EEy19Ng1NNg1ANo11Ey1aNz1RPQ1OB914HX1eGI1BJA102-1d5e1LNg1PEy0VN51UF516D4176H1G2d1I8r1S8f18H51XGp13Lr1Z7D1CFN126p1MGZ1D8B1WIt159n1J8z1QCk1YJR1F4j1cCK1aD81bIp1KIr1TNg1HNg19Ng1NNg1A0A11CD1ECp1R4S1PHN1d4v105l1BIP1LNg14DW1O2X1eCP0SHr172m1INz1GF5186s16Eb1UMq1VBb1XLr1JBB1Z7D1CC6139912IY1MJg1D231WGg15AB1QCk1FMe1Y6p1c2g1bOl1KIr1T4q1H9c1E7p19Ng1NIm1A7U11CH1aI-1R701O2X14KO1eMS1B2i101j1dPQ1LNg1POE0S5t1V0w1U831IMy1GMq1XLr169Z1QNV12231CC6139917Hn1M251DIc1WOT15061Y8B1Z7D1JAJ18Ej1FH41a5b1bA41KIr1THh1HH61EN81NKX1A1U115319Ng1RLq1P2a1LNg1d4S10N01cM-1eCD14LU1O2X1BM40SCL17Ej1ID81G5Q18MT166f1UDe1VFN1X991JHK1ZIH1CC613FN12Ic1MOH1DP51WCT15JQ1QNV1Y9c1FFn1cI-1b9s1KKC1T4e1HM01EJk19Ng1NJ11AFO11GS1a8u1RKn1O2X14711eDQ1BPY10J_1d701LNg1P880V8W1UHP16H017A71GH01IA01S7D18Hn1X9913FN1ZIH1CDZ12P51M7B1D711WJ-158B1J9M1QNV1YP51F4M1c5b1aMD1bOQ1KKC1T0N1H6R19Ng1NEB1AMl114X1E7b1RBC1P3M1dLq101v1B5d1LNg14JQ1O2X1eHK0XFN1II-1GHP189j16HP1U6Z1VBf1S9_1Q9817Fl1CDZ13FN12711MAE1DF21W0K159c1Y711ZIH1JJw1F1U1aJ-1KKC1TKc1HB21EJw19Ng1NGa1ANg11Mk1PNE1bEd1O2X14CT1e1X1BNM10691dKn1LNg1c7B1RLu0V9-1UP516GG17Of1G4q1IPA1SJY18Ic1XDe13De1ZNV1C7D12Ic1MOH1DP51WCT15JQ1JNw1Q8q1F0Z1Y9c1cJT1b9s1KKC1T6N1HHf1E5Y19Ng1NKL1A2k118S1aOT1R011ONg14A01eKQ1BCH10731dBC1LNg1P6f0VAk1UCT16JQ17NQ1G061IM-1SAB18171XIH13L41Z8q1CCk12IY1MJg1D231WFm15911JEv1Q7r1YJQ1FDD1cMx1aIt1b7x1KKC1TIB1HG819Ng1NIR1AGg11MC1EEm1R011PBf1dLu10GR1BFw1LNg14H21ONg1eIL0SOH174y1IOD1GAE18Dp16Fm1UPA1VGZ1XNV1JGU1Z7r1C9_139812JR1MI-1D6p1W7B15J-1Q041FIe1YAB1c251bA41KKC1TEM1HAc1ENx19Ng1NGN1AJY11Fl1aOH1RLP1ONg14091e0H1BHD10IA1dLu1LNg1P6p0S8r1VH21U121IMy1GMU1X9_16Dp1QO612AB1CBf138q17IV1MDp1D061W5b15OT1Y0K1Z1m1JDO185a1FH71aML1bIp1KKC1TIY1H991EGC1N7c1AFN11HP19Ng1RDd1PMx1LNg1d01108x1c5b1eOL14091ONg1B8x0S3S179O1I1c1G12188Z16BP1UM51VMi1X0C1JLa1ZO61C9j137r129n1MMy1D911WAQ15It1Q2m1Y4_1FMe1cJg1b1H1KKC1TNg1HNg1EF519Ng1NNg1A4z117B1aI-1RFc1ONg14091eBy1BNo10Fe1dLP1LNg1PBD0V071U5A16Fu17Bg1G2B1I6P1SOZ18Kv1X6Z13041Z2m1CGG12J-1M6P1D0K1WDp15OH1J2w1QAI1YMD1F7G1cML1aM-1bKo1KKC1TNg1HNg19Ng1NNg1AME112R1E4q1RFc1PNg1dDd101C1BMS1LNg14091ONg1eLL0XLU1IBD1GHd18FG16DR1UDz1VHQ1S2B1Q9c17Au1CF2132m12MD1M2k1D171WOD15Jg1YAE1ZIc1JJd1F0i1a1c1KH21TNg1HNg1E8W19Ng1NNg1A4z112R1PM-1b0E1ONg14091eD51B8V100p1dDd1LNg1c1F1R4J0VM51UFU16KC174h1GAx1IKY1S3S18Nt1X9c13231ZJR1C6p128u1MCK1DIt1WMy151F1JCO1QJe1F3g1YMx1cAQ1bDj1K6Q1TNg1HNg1ECc19Ng1NNg1AFN11G-1aKC1R4J1ONg14091eJ61BMR10021dDd1LNg1P6p0VK01UE516Jg17EJ1GI-1I6r1S5O18FU1XAB13911ZAk1C9n125b1MIr1DMx1W1c15PA1J3V1QJ-1YML1F5x1cCu1aAx1bHV1K121TNg1HNg19Ng1NNg1AJY11G-1E3j1R2V1PDe1dFc10N81BFR1LNg14091ONg1e0d0SGZ17B-1IDR1G9n18E516JR1U8Z1VJV1XCT1JNQ1ZMD1C17131712AQ1MBF1D1F1W8r15D81QGg1FEv1YCu1cPA1bA91K091TNg1HNg1EME19Ng1NNg1AGg11G-1a6r1R2V1ONg14091eHN1BG010D51dFc1LNg1P2x0SJR1V1c1U2B1I3S1GMB1XAE16NV1QJT12M-1C8u13AE17DB1M5O1DDp1WCK15My1YD81Z7B1JFb18Fs1FO01aDR1bGJ1KHd1TNg1HNg1ENQ1NNg1A2k11Ng19Ng1RMa1PBO1LNg1d4J10Fe1cA01e9014091ONg1B7p0SL417HZ1IG-1GF518P216NE1UOc1VFm1XJg1JAU1ZML1CJg13Jg121c1MAx1DMy1WIr156P1QGZ1Y1c1FEm1cM-1bKe1KNg1TNg1HNg1EAU19Ng1NNg1ANg11Ng1aHd1RMa1ONg14091eIA1BNF10By1d4J1LNg1PAU0V3S1UDq162m175s1GIc1I5J1SMx18BM1XI-13I-1ZCu1CI-12Nz1MKY1D1c1WBF158r1J4y1QPA1YNz1FLg1cD81aPT1bKe1KAO1TNg1HNg19Ng1NNg1ANg113S1E4y1RMa1PK41d4J10Fe1B0u1LNg14091ONg1e0H0XPA1IFM1GNt181q16Dq1UDk1VGW1SCz1QD817CG1CA013PA126P1M0G1DNz1W5O15CK1Y8r1ZDp1JPB1FEr1aG-1KID1TNg1HNg1EPB19Ng1NNg1ANg115a1PMZ1b4F1ONg14091eGD1B9R109o1d2V1LNg1cD81RMa0VOe1U8o161Y17DN1GOP1I4m1SDC18I31XDp13Dp1ZOD1CM-128r1M6Q1D8r1WH215KC1JLa1QMU1F741Y2k1cOD1b4F1KGH1TNg1HNg1ELa19Ng1NNg1ANg112A1aAO1RMa1ONg14091e3A1BA110CD1d2V1LNg1P6F0VM71U2r167217Nf1GCy1IAa1SE918CF1XM-13D81Z2g1CMU122k1M2A1D2k1WKY15Ir1JLS1Q1c1YCK1FPd1cMU1aID1bHv1KA51TNg1HNg19Ng1NNg1ANg11H21ELS1RMa1PBO1d2V10N81BDV1LNg14091ONg1e2S0SOK17Ka1IIg1GNq18Ez164l1U7X1VKz1XD81J3v1Z8r1C1c13MU12KC1M6r1DKC1W0G15BF1Q2k1F8P1YIr1cMU1bHv1KIg1TNg1HNg1E3v19Ng1NNg1ANg11CK1aGH1RMa1ONg14091ePC1B3L10HL1d2V1LNg1PJd0SDH1V0g1U3c1IH91G3u1XMU16M11QIr12Ir1CNz13My17LS1MNJ1DIr1WBP155O1YBD1ZIr1J6F189h1FNR1aA51bHv1KH91TNg1HNg1E6F1NNg1ANg112g19Ng1RBq1P2_1LNg1d2V10Fh1cMy1eOL14091ONg1BAg0SI617Nd1IAO1G3P18NX161M1UC01VFW1XPA1JAH1ZOD1CM-13A0126P1MBP1D6P1WH215CK1QMy1Y8r1FKU1cD81b4F1K4m1TNg1HNg1EAH19Ng1NNg1ANg11CK1aHd1RBq1ONg14091eDQ1BMR102i1d2V1LNg1PH50VBh1UKZ165j17Jm1GIJ1ICg1SLK18Mf1XOH13Mx1ZGZ1C5b12MU1MH21DMU1WKC151c1JMq1QAQ1YMy1FDa1cA01a2A1bKe1K2R1TJR1HDu19Ng1N6B1ANg11H21EMq1RBq1PDe1d2V10A81B021LNg14091ONg1e3A0YDp1I6r1GCA18Af166I1UJa1V921SCx1XGg17MP1ZAE1CFm13Gg12Dp1MIr1DDp1W6P15D81QJT1J0C1RBq1a2k1bEX1KEf1TOA1H6v1E0C19Ng1NKA1ANg112A1FJy1ONg14091eDW1BPC103A1d2V1LNg1cI-1PAI0VD11UL916KT17Ev1G7a1IBD1SMH18B71XJ-13J-1Z171CBv12AQ1M2k1DAQ1WMU15Cu1J0K1QMD1FBK1YAQ1cGZ1bA91KNJ1T3F1HP71E0K19Ng1NAz1ANg115a1aPA1RMa1ONg14091eG41BPU10221d2V1LNg1P9d0VOr1U60169Q170i1GH11IMy1S1N18DH1X0613061Z6H1CJe12Jg1M1c1D5b1WDp15ML1J2g1QAk1YJg1F1Z1c5b1a7B1bHV1KAx1T5v1HIb19Ng1N6G1ANg113S1E2g1RMa1P2k1d2V108i1B8y1LNg14091ONg1e220SGh17CZ1IAQ1GCd18OG16Ox1UJz1V5S1XIc1JNg1Z6p1C9c139c12JT1MOD1D7B1WAQ15OH1Q061F1U1YJT1cOH1b0E1KCK1T1f1H0o1ENg19Ng1NOb1ANg11Ng1aBv1RMa1ONg14091eFp1B2G10Gt1d2V1LNg1PNg0SGh1V8L1U0W1IA01GH11X9c16J21QAB128u1C23139c17Lx1MMU1DIt1WI-15OH1Y8u1ZJQ1JNg187W1FD_1aGg1b0E1KKC1T6o1H2N1ENg1N8A1ANg11Ng19Ng1RMa1PNg1LNg1d2V10PY1cOH1eP114091ONg1BAV0SGh17Dr1IOD1GDc185N16KT1UBd1VOr1X9c1JNg1Z061C8B1323129d1MMy1DFm1WCu15OH1Q911YAE1F5R1cOH1b0E1KBD1TN61H6a1ENg19Ng1N0l1ANg11Ng1a7B1RMa1ONg14091e9Y1BF7108i1d4J1LNg1PNg0VI61U8p16CV17NG1GJ21I1c1SLH18KR1X9c13231ZJR1C6p12Gg1M2g1DOT1WPA15OH1JNg1QJe1Y9d1FH41cOH1aJg1bG11K5O1TEv1H0N19Ng1NBo1ANg11Ng1ENg1RMa1PNg1d4J109Y1BHD1LNg14091ONg1eIL0XIc1I8r1GCA18J716Bj1U8g1V601S3-1Q6p17KW1C23139c12171MNz1DCT1WA015OH1YFm1ZIY1JNg1FMe1aCu1KH21T4_1H2p1ENg19Ng1N3B1ANg11Ng1PNg1bG11ONg14091e5q1BDQ10221d4J1LNg1cOH1RMa0VMF1UMQ163w17PG1GKT1IIr1SMH18AT1X7113711Z9c1CNb124_1M6P1DJ-1WDp15OH1JNg1Q231FDr1YGg1cOH1bG11KKY1TNg1HNg1ENg19Ng1NNg1ANg11Ng1aOD1R2V1ONg14091eHK1B2i10J_1d4J1LNg1PNg0V8p1UJo165j17K31G7d1IH21S5S18AA1X2m132m1Z711C9-12Ak1M8r1D9n1WM-15OH1JNg1QP51YOT1FIf1cOH1a6P1bKo1KBP1TNg1HNg19Ng1NNg1ANg11Ng1ENg1R2V1PNg1dFc10761B9C1LNg14091ONg1ePU0SCx178m1I0G1GHl18N4161_1UEQ1VL91XF21JNg1ZIc1CNb13F212Bv1M2k1DJ-1WOD15251Q9c1FBA1YGg1c251bG11K2A1TNg1HNg1ENg19Ng1NNg1ANg11Ng1aKC1R2V1ONg14091eIA1BM010IN1dFc1LNg1PNg0SMA1VA61U4r1I2A1GCV1XNb16Hg1QIY12171CIc13P5179g1MCK1D4_1WMU15Jg1Y9d1Z8B1JNg18El1F391a5O1b0E1K121TNg1HNg1ENg1NNg1ANg11Ng19Ng1R2V1PNg1LNg1dFc106k1cJg1eDQ14091ONg1BLf0SOG17L01I121G6I187u16En1UEl1V2O1X9c1JNg1Z6p1C8B132312MD1MKC1D171W2g15GZ1QJR1YAE1F5n1cGZ1bDj1KJV1TNg1HNg1ENg19Ng1NNg1ANg11Ng1a0G1R2V1ONg14091e211B5l10LL1dFc1LNg1PNg0V481UCC16I2177V1GNu1I5a1S0B18C01XIY136p1Z061CJQ12Fm1MIr1DMD1W1c151F1JNg1QJe1Y7B1FEv1c1F1a6r1bHV1K091TNg1HNg19Ng1NNg1ANg11Ng1ENg1R2V1PNg1dFc10Ll1BCP1LNg14091ONg1eHI0YOH1IEf1GGl189D16431UN-1VFW1SI61XJR176F1Z911CJe13JR12It1MBD1DFm1WNz15I-1Q6H1JNg1R2V1aJV1bHV1KCg1TNg1HNg1ENg19Ng1NNg1ANg11Ng1FED1ONg14091eFV1B1f10LG1dFc1LNg1cI-1PNg0V3h1U3E165_179S1G3P1I3S1SFv18CB1XAB13AB1Z9n1C91128u1M5O1DAE1W8r15PA1JNg1QAk1FGT1Y251cPA1bA91KHd1TNg1HNg1ENg19Ng1NNg1ANg11Ng1aEf1R2V1ONg14091e671BAg10ET1dFc1LNg1PNg0VGo1UHe165j174z1GFy1ICg1S9218Dv1X91136H1ZAk1C9n128u1MBF1DAE1W6P15PA1J5I1QJ-1Y251F8Q1cA01aDR1bA91KCg1TNg1HNg19Ng1NNg1ANg115I1E5I1R2V1PNg1dFc101S1BN21LNg14091ONg1e1R0SA617991I091GLK180U167a1U001VOF1X6H1JEI1ZJ-1C0K139n127B1MBF1DAE1W6P15Cu1QBv1FED1Y251cA01bA91K091TNg1HNg1EEI19Ng1NNg1ANg11EI1aJV1R2V1ONg14091eMv1BI910PI1dFc1LNg1PNg0SJa1VAS1UMz1IJV1GMF1X9n168L1Q4_127B1CAk130K174q1MBD1D8u1WNz15Cu1Y251ZBv1J7Q187n1FBw1a121bA91KJV1TNg1HNg1E7Q1NNg1ANg117Q19Ng1R4J1PNg1LNg1dFc109R1cDp1e2K14091ONg1BGI0SEQ17171I121G0-180n16DY1UCB1VHa1X0K1J3N1Z4_1CBv13J-127B1MBD1D8u1WNz15Cu1QCT1Y251F461cM-1bA91KNJ1TNg1HNg1E3N19Ng1NNg1ANg113N1a6r1R4J1ONg14091e111B6j10GA1dFc1LNg1PNg0VC01UDv16LX171c1GJa1I6r1SDl188v1X0K13Bv1ZCT1C4_12JT1MIr1D8u1W1c15I-1JFp1QOT1Y251F9v1cD81a6Q1bEX1K2A1TNg1HNg19Ng1NNg1ANg11Fp1EFp1R4J1PNg1dDd100t1B8s1LNg14091ONg1eDV0Y251I6Q1GH-183c161e1UC51V5u1SOF1X0K17Hd1ZOT1CCT134_12JT1MIr1D7B1W1c15I-1QMD1JEy1R4J1a0G1bEX1KBP1TNg1HNg1EEy19Ng1NNg1ANg11Ey1FNW1ONg14091e0t1B1L10GI1dDd1LNg1cOD1PNg0V2o1UIS167Z17Mx1GLn1IAx1SMd18Pa1XBv13171ZFm1CMD12Mx1MKC1DOH1W2g15I-1JHH1Q9d1FKW1YJg1cMU1bEX1KAx1TNg1HNg1EHH19Ng1NNg1ANg11HH1aBF1R4J1ONg14091eN21BPR10KM1dDd1LNg1PNg0VCW1UEz1605179j1G481IBD1S5Z18Eq1XCT13171ZIt1CMD125b1MCK1D251WMy15I-1JHH1Q7B1YML1FIu1cMU1a2k1bEX1KBF1TBe1H2A19Ng1N3j1ANg11HH1EHH1R4J1PNg1dDd10Ag1B9R1LNg14091ONg1eN20SPO17Hr1I2k1G7T180g169J1UCW1VN41YGZ1J1L1ZIt1CGg13OT12ML1M2k1DML1WMy15Cu1Q7B1F561X171cMU1bGJ1KKC1TEa1H061E1L19Ng1NDX1ANg111L1a2g1R4J1ONg14091eN21B1510Mb1dDd1LNg1PNg0S7T1VPO1U8-1I1c183h1G051XOT16FF1Q7B121F1CGg13MD1M2k1D1F1WMU15Cu1YAQ17P41ZIt1JGm1FFJ1aM-1K8r1T1P1H0w1EGm19Ng1NNN1ANg11Gm1PNg1bGJ1ONg14091e2-1BHX100u1dDd1LNg1cMy1R4J0S0-1V4Z1U4E1IMU18Ja1GL91YI-16OR1XGg13MD1ZIt1CGg12I-1M8r1DI-1WOD15Cu17Ay1Q7B1J8z1R4J1aI-1FHF1bGJ1K1c1TIk1HJ41E8z1NHY1ANg118z19Ng1ONg14091cMy1e2-1BM0101h1dDd1LNg1PNg0UFF16FA17L11GCn1IDp1VCI18Gz1SOR1WOD1Q7B1ZIt1CGg13Gg12A01M6P1DA01J8z1XFm1FH41R4J1cMy15Cu1bGJ1KMU1TJ51HOf1E8z19Ng1N3n1a5b1ANg1PNg1ONg14091e2-1BFV10AF1dDd1LNg118z1YCu"
}
```
## CSV Example Input
```csv
UTC,Attribute,AverageNumericValue,AsOfDateUTC,ForecastHorizonHour
2022-01-24T06:00:00Z,air_density_100m:kgm3,1.282000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,dew_point_2m:C,-1.500000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,diffuse_rad:W,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,direct_rad:W,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,effective_cloud_cover:p,2.600000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,fresh_snow_6h:cm,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,global_rad:W,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,high_cloud_cover:p,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,low_cloud_cover:p,2.600000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,medium_cloud_cover:p,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,msl_pressure:hPa,1034.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,precip_1h:mm,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,prob_rr_3h:p,1.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,relative_humidity_100m:p,80.100000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,relative_humidity_2m:p,95.900000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,relative_humidity_50m:p,84.700000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,sfc_pressure:hPa,1032.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,snow_depth:cm,0.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,t_100m:C,3.100000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,t_2m:C,-0.900000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,t_2m:F,30.400000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,total_cloud_cover:p,2.600000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,visibility:km,29.700000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wet_bulb_t_2m:C,-1.400000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_dir_100m:d,111.800000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_dir_10m:d,95.300000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_dir_120m:d,112.900000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_dir_20m:d,97.100000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_dir_50m:d,102.600000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_dir_80m:d,108.200000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_gusts_100m:ms,4.500000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_gusts_10m:ms,3.300000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_gusts_20m:ms,3.400000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_gusts_50m:ms,3.600000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_gusts_80m:ms,4.200000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_speed_100m:ms,3.400000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_speed_10m:ms,1.600000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_speed_120m:ms,3.300000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_speed_20m:ms,2.000000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_speed_50m:ms,2.700000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T06:00:00Z,wind_speed_80m:ms,3.100000,2022-01-23T21:34:01.1100000Z,18.000000
2022-01-24T07:00:00Z,air_density_100m:kgm3,1.283000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,dew_point_2m:C,-2.400000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,diffuse_rad:W,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,direct_rad:W,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,effective_cloud_cover:p,4.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,fresh_snow_6h:cm,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,global_rad:W,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,high_cloud_cover:p,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,low_cloud_cover:p,4.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,medium_cloud_cover:p,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,msl_pressure:hPa,1034.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,precip_1h:mm,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,prob_rr_3h:p,1.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,relative_humidity_100m:p,81.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,relative_humidity_2m:p,95.800000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,relative_humidity_50m:p,85.200000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,sfc_pressure:hPa,1032.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,snow_depth:cm,0.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,t_100m:C,2.900000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,t_2m:C,-1.900000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,t_2m:F,28.700000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,total_cloud_cover:p,4.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,visibility:km,28.000000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wet_bulb_t_2m:C,-2.300000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_dir_100m:d,116.500000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_dir_10m:d,105.700000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_dir_120m:d,117.200000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_dir_20m:d,106.900000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_dir_50m:d,110.500000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_dir_80m:d,114.100000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_gusts_100m:ms,4.900000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_gusts_10m:ms,3.700000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_gusts_20m:ms,3.700000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_gusts_50m:ms,4.100000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_gusts_80m:ms,4.600000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_speed_100m:ms,3.800000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_speed_10m:ms,1.900000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_speed_120m:ms,3.700000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_speed_20m:ms,2.400000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_speed_50m:ms,3.100000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T07:00:00Z,wind_speed_80m:ms,3.500000,2022-01-23T21:34:01.1100000Z,19.000000
2022-01-24T08:00:00Z,air_density_100m:kgm3,1.284000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,dew_point_2m:C,-2.700000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,diffuse_rad:W,12.700000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,direct_rad:W,11.500000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,effective_cloud_cover:p,1.200000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,fresh_snow_6h:cm,0.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,global_rad:W,24.200000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,high_cloud_cover:p,0.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,low_cloud_cover:p,1.200000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,medium_cloud_cover:p,0.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,msl_pressure:hPa,1034.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,precip_1h:mm,0.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,prob_rr_3h:p,1.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,relative_humidity_100m:p,81.200000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,relative_humidity_2m:p,95.600000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,relative_humidity_50m:p,85.300000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,sfc_pressure:hPa,1032.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,snow_depth:cm,0.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,t_100m:C,2.800000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,t_2m:C,-2.000000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,t_2m:F,28.300000,2022-01-23T21:34:01.1100000Z,20.000000
2022-01-24T08:00:00Z,total_cloud_cover:p,1.200000,2022-01-23T21:34:01.1100000Z,20.000000
.....
```
## JSONEncoder: Example Output
File Size 288KB -> 26KB encoded -> 8KB encoded and compressed
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
## JSON Example Input
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
