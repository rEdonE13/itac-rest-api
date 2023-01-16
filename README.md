# iTAC REST API
RESTful API for iTAC

## iTAC Session
This API functions on a Session Context based, meaning that only after a successful authentication the API can be used.

## Config File

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
    attributes      = ["ATTRIBUTE_1", "ATTRIBUTE_2"]
)

itac.logout()

print(attribute_values)

```