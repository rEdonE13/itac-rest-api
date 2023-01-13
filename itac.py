"""iTAC Class"""

import json
import requests

from itacconfig import API_URL
from itacconfig import HEADERS
from itacconfig import station
from itacconfig import user


class ITAC:
    """
    A class to represent itac.

    Attributes:
        attr1       (str): Path
        api_url     (str): RESTful API URL

    Methods:
        create_connection():
            Establish a connection
        login(user):
            Logins the given user and gets a valid session.
        logout():
            Logs out the user in the session context.
    """
    def __init__(self) -> None:
        self.api_url = API_URL
        self.headers = HEADERS
        self.session_context = None


    def login(self) -> None:
        """Authenticate as a machine with user data."""
        url = self.api_url + "regLogin"
        payload = {
            "sessionValidationStruct": {
                "stationNumber": station["capacity"],
                "stationPassword": station["pwd"],
                "user": user["id"],
                "password": user["pwd"],
                "client": "01",
                "registrationType": "S",
                "systemIdentifier": station["capacity"]
            }
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        self.session_context = res.json()["result"]["sessionContext"]


    def logout(self) -> None:
        """Desactivate the current session."""
        url = self.api_url + "regLogout"
        payload = {
            "sessionContext":       self.session_context
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()


    def trGetSerialNumberInfo(self, serial_number: str, result_keys: list[str]) -> list[str]:
        """Get information about the passed serial number."""        
        url = self.api_url + "trGetSerialNumberInfo"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        "35061400",
            "serialNumber":         serial_number,
            "serialNumberPos":      "-1",
            "serialNumberResultKeys":  result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["serialNumberResultValues"]


    def getAttributesFromSerialNumber(self,
            serial_number: str,
            attributes) -> list[str] :
        """Get attribute values from the passed serial number."""
        url = self.api_url + "attribGetAttributeValues"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station["capacity"],
            "objectType":           0,
            "objectNumber":         serial_number,
            "objectDetail":         "-1",
            "attributeCodeArray":   attributes,
            "allMergeLevel":        0,
            "attributeResultKeys":  ["ATTRIBUTE_CODE", "ATTRIBUTE_VALUE", "ERROR_CODE"]
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["attributeResultValues"]


    def trGetStationSetting(self, station_number: str, station_setting_result_keys: list[str]) -> list[str]:
        """Queries the actual product version and the corresponding
        work order at a station."""
        url = self.api_url + "trGetStationSetting"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "stationSettingResultKeys": station_setting_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["stationSettingResultValues"]


    def trGetTopFailures(self, station_number: str,
                               top_failures_filter: list[str], 
                               top_failures_result_keys: list[str]
                        ) -> list[str]:
        """This function outputs the booked failures, sorted by frequency, for a freely selectable
        period under review. In doing so, it is possible to select whether failures should be
        ascertained relating to the part, order or station. In addition, it is possible to limit the
        maximum number of failures to be considered (MAX_ROWS); this makes, for example,
        a "TopTen" or even "TopThree" failure type analysis possible."""
        url = self.api_url + "trGetTopFailures"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "trGetTopFailuresFilter":   top_failures_filter,
            "topFailuresResultKeys":    top_failures_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["topFailuresResultValues"]
