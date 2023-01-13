# iTAC REST API
RESTful API for iTAC

## iTAC Session
This API functions on a Session Context based, meaning that only after a successful authentication the API can be used.

## Config File

## Station Parameters
Every computer has its own ID or Capacity as well as its own Password defined in iTAC. This values are necessary to login a station and allow a biderectional communication with iTAC.
```python
station = {
    "capacity": "",
    "pwd":      ""
}
```

## User Parameters
Every employee or user registed in the iTAC system have an ID and a Password, which are necessary to authenticate the user in a [Station](#station-parameters).
```python
user = {
    "id": "",
    "pwd":      ""
}
```