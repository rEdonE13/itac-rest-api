# iTAC REST API
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![MIT license](https://img.shields.io/badge/License-MIT-blue.svg)](https://lbesson.mit-license.org/)
[![Ask Me Anything !](https://img.shields.io/badge/Ask%20me-anything-1abc9c.svg)](https://GitHub.com/rEdonE13)
[![Twitter](https://badgen.net/badge/icon/twitter?icon=twitter&label)](https://twitter.com/rEdonE_13)

RESTful API for iTAC.

# Table of Contents
* [Requirements](#requirements)
* [How to Use](#how-to-use)
    * [Configuration File](#config-file)
        * [API URL](#api-url-parameter)
        * [HEADERS](#headers-parameter)
        * [Station Parameters](#station-parameters)
        * [User Parameters](#user-parameters)
        * [Example](#example)

# Requirements

* [Python](https://www.python.org/) 3.8.x or above
* Python Libraries: `requests`

The `requirements.txt` file list all Python libraries needed for the application to work, and they will be installed by using:

```bash
pip install -r requirements.txt
```

# How to Use
## Config File
The `itacconfig.py` must contains the following parameters in order to establish a connection with your iTAC System.

### API URL Parameter
Set the REST iTAC API address.
```python
API_URL = ""
```

### Headers Parameter
Content type header as json is a must.
```python
HEADERS = {"Content-Type": "application/json"}
```

### Station Parameters
Every computer has its own ID or Capacity as well as its own Password defined in iTAC. This values are necessary to login a station and allow a biderectional communication with iTAC.
```python
station = {
    "capacity": "",
    "pwd":      ""
}
```

### User Parameters
Every employee or user registed in the iTAC system have an ID and a Password, which are necessary to authenticate the user in a [Station](#station-parameters).
```python
user = {
    "id": "",
    "pwd":      ""
}
```

## Example
### Query an attribute
```python
"""iTAC API - Fetch attribute values."""

from itac import ITAC


itac = ITAC()
itac.login()

# Fetch attribute value.
attribute_values = itac.getAttributesFromSerialNumber(
    serial_number   = "123456789", 
    attributes      = ["ATTR_1", "ATTR_2"]
)

itac.logout()

print(attribute_values)
```

### Output
```
['ATTR_1', '00000000079791453', '0', 'ATTR_2', '57152114070', '0']
```