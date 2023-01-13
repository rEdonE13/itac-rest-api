"""iTAC Class"""

import json
import requests

from itacconfig import API_URL
from itacconfig import HEADERS


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


    def login(self, user: str) -> None:
        url = self.api_url + "regLogin"
        payload = {
            "sessionValidationStruct": {
                "stationNumber": "35061400",
                "stationPassword": "Password",
                "user": user,
                "password": "password",
                "client": "01",
                "registrationType": "S",
                "systemIdentifier": "35061400"
            }
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        self.session_context = res.json()["result"]["sessionContext"]


    def logout(self) -> None:
        url = self.api_url + "regLogout"
        payload = {
            "sessionContext":       self.session_context
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()


    def trGetSerialNumberInfo(self, serial_number: str, result_keys: list[str]) -> list[str]:
        url = self.api_url + "trGetSerialNumberInfo"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        "35061400",
            "serialNumber":         serial_number,
            "serialNumberPos":      "-1",
            "serialNumberResultKeys":  result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        return res.json()["result"]["serialNumberResultValues"]


    def getAttributesFromSerialNumber(self, 
            station_number: str,
            serial_number: str,
            attributes) -> list[str] :
        url = self.api_url + "attribGetAttributeValues"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "objectType":           0,
            "objectNumber":         serial_number,
            "objectDetail":         "-1",
            "attributeCodeArray":   attributes,
            "allMergeLevel":        0,
            "attributeResultKeys":  ["ATTRIBUTE_CODE", "ATTRIBUTE_VALUE", "ERROR_CODE"]
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        return res.json()["result"]["attributeResultValues"]


    def trGetStationSetting(self, station_number: str, station_setting_result_keys: list[str]) -> list[str]:
        url = self.api_url + "trGetStationSetting"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "stationSettingResultKeys": station_setting_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        return res.json()["result"]["stationSettingResultValues"]


    def trGetTopFailures(self, station_number: str,
                               top_failures_filter: list[str], 
                               top_failures_result_keys: list[str]
                        ) -> list[str]:
        url = self.api_url + "trGetTopFailures"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "trGetTopFailuresFilter":   top_failures_filter,
            "topFailuresResultKeys":    top_failures_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        return res.json()["result"]["topFailuresResultValues"]
