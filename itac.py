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

    ***Check IMSApi documentation for Key Values.

    Attributes:
        api_url         (str):  RESTful API URL
        headers         (dict): Http headers
        session_context (str):  iTAC session context structure

    Methods:
        login():
            Logins the given user in the config file and gets a valid session.
        logout():
            Logs out the user in the current session context.
        trGetSerialNumberInfo(serial_number, result_keys):
            serial_number   (str):      Serial number
            result_keys     list(str):  Serial number key values to be featch.
        getAttributesFromSerialNumber(serial_number, attributes):
            serial_number   (str):      Serial number
            attributes      list(str):  List of attributes to be featch.
        trGetStationSetting(station_setting_result_keys):
            serial_number   (str):      Serial number
        def trGetTopFailures(top_failures_filter, top_failures_result_keys):
            trGetTopFailuresFilter  list(str):  Filter key values.
            topFailuresResultKeys   list(str):  Result key values.
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
                "stationNumber":    station["id"],
                "stationPassword":  station["pwd"],
                "user":             user["id"],
                "password":         user["pwd"],
                "client":           "01",
                "registrationType": "S",
                "systemIdentifier": station["id"]
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
            "stationNumber":        station["id"],
            "serialNumber":         serial_number,
            "serialNumberPos":      "-1",
            "serialNumberResultKeys": result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["serialNumberResultValues"]


    def trActivateWorkOrder(self,
            station_number: str,
            work_order: str,
            serial_number: str,
            serial_number_pos: str = "-1",
            process_layer: int = 0,
            flag: int = 1
    ) -> list[str]:
        """
        This function activates or deactivates the passed work order on the station or line.
        
        Parameters
            station_number (str): Station number of the work station in the iTAC system
            work_order (str): Number of a production order
            serial_number (str): Serial number of the panel
            serial_number_pos (str): Position of the single panel in the unit-array
            process_layer (int): Orientation of the PCB during the work step [0; 1; 2; 3]
            flag (int): Mode "Work order activation" [1; 11; 21; 2; 12; 22; 3; 13; 23; 4; 14; 24]
        """
        url = self.api_url + "trActivateWorkOrder"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "workOrderNumber":      work_order,
            "serialNumber":         serial_number,
            "serialNumberPos":      serial_number_pos,
            "processLayer":         process_layer,
            "flag":                 flag
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]


    def getAttributesFromSerialNumber(self,
            serial_number: str,
            attributes) -> list[str] :
        """Get attribute values from the passed serial number."""
        url = self.api_url + "attribGetAttributeValues"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station["id"],
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


    def trGetNextSerialNumber(self,
            station_number: str,
            work_order: str,
            part_number: str,
            number_of_records: int) -> list[str] :
        """
        This function returns the serial numbers provided by the iTAC system for a part 
        that is to be produced.

        Parameters
            station_number (str): Station number of the work station in the iTAC system
            work_order (str): Number of a production order; if necessary, with the ID alternative that is to be used for the ID generator
            part_number (str): Part number in the iTAC system
            number_of_records (int): Default value for the number of entries in the array
        """
        url = self.api_url + "trGetNextSerialNumber"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "workOrderNumber":      work_order,
            "partNumber":           part_number,
            "numberOfRecords":      number_of_records
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["serialNumberArray"]


    def trAssignSerialNumberForProductOrWorkOrder(self,
            station_number: str,
            work_order: str,
            part_number: str,
            bom_version: str,
            serial_number_ref: str,
            serial_number_ref_pos: str,
            process_layer: int,
            serial_numbers_data: list,
            activate_work_order: int
        ) -> list[str] :
        """Get next serial number from ID Generator."""
        url = self.api_url + "trAssignSerialNumberForProductOrWorkOrder"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "workOrderNumber":      work_order,
            "partNumber":           part_number,
            "bomVersion":           bom_version,
            "serialNumberRef":      serial_number_ref,
            "serialNumberRefPos":   serial_number_ref_pos,
            "processLayer":         process_layer,
            "serialNumberArray":    serial_numbers_data,
            "activateWorkOrder":    activate_work_order
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]


    def trGetStationSetting(self, 
            station_number: str,
            station_setting_result_keys: list[str]) -> list[str]:
        """Queries the actual product version and the corresponding
        work order at a station."""
        url = self.api_url + "trGetStationSetting"
        payload = {
            "sessionContext":           self.session_context,
            "stationNumber":            station_number,
            "stationSettingResultKeys": station_setting_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["stationSettingResultValues"]


    def trGetTopFailures(self, top_failures_filter: list[str],
                               top_failures_result_keys: list[str]
                        ) -> list[str]:
        """This function outputs the booked failures, sorted by frequency, for a freely selectable
        period under review. In doing so, it is possible to select whether failures should be
        ascertained relating to the part, order or station. In addition, it is possible to limit the
        maximum number of failures to be considered (MAX_ROWS); this makes, for example,
        a "TopTen" or even "TopThree" failure type analysis possible."""
        url = self.api_url + "trGetTopFailures"
        payload = {
            "sessionContext":           self.session_context,
            "stationNumber":            station["id"],
            "trGetTopFailuresFilter":   top_failures_filter,
            "topFailuresResultKeys":    top_failures_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]["topFailuresResultValues"]


    def trUploadState(self,
        station_number: str,
        process_layer: int,
        serial_number: str,
        serial_number_pos: str,
        serial_number_state: int,
        duplicate_serial_number: int = 0,
        book_date: str = "-1",
        cycle_time: float = 0,
        serial_number_upload_keys: list = [],
        serial_number_upload_values: list = [],
    ) -> list:
        """
        This function books, in a work-step-conformant manner, the process state of one or more
        individual products (single panel) or of a complete multiple panel. In doing so, a time
        stamp is set for the component lot capture. This function is the universal function for
        the booking of a product.
 
        Parameters
            station_number (str): Station number of the work station in the iTAC system
            process_layer (int): Orientation of the PCB during the work step [0; 1; 2]
 
        """
        url = self.api_url + "trUploadState"
        payload = {
            "sessionContext":           self.session_context,
            "stationNumber":            station_number,
            "processLayer":             process_layer,
            "serialNumberRef":          serial_number,
            "serialNumberRefPos":       serial_number_pos,
            "serialNumberState":        serial_number_state,
            "duplicateSerialNumber":    duplicate_serial_number,
            "bookDate":                 book_date,
            "cycleTime":                cycle_time,
            "serialNumberUploadKeys":   serial_number_upload_keys,
            "serialNumberUploadValues": serial_number_upload_values,
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]


    def trRemoveSerialNumberFromOrder(self,
            station_number: str,
            remove_serial_number_keys
        ) -> list[str]:
        """function descr"""
        url = self.api_url + "trRemoveSerialNumberFromOrder"
        payload = {
            "sessionContext":           self.session_context,
            "stationNumber":            station_number,
            "removeSerialNumberKeys":   remove_serial_number_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS, timeout=5)
        res.raise_for_status()
        return res.json()["result"]
