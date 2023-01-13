import json
import requests
from itac import ITAC

from itacconfig import HEADERS


class Attribute(ITAC):
    # TODO (alugo): Add documentation
    def getAttributesFromSerialNumber(self, station_number: str, serial_number, attributes):
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


    # TODO (alugo): Add function for attribGetAllAttributeValue

    # TODO (alugo): Add function for attribGetAttributeCode
    def attribGetAttributeCode(self,
                                station_number: str,
                                attribute_code_filter: list,
                                code_result_keys: list[str],
                                condition_result_keys: list[str]
                            ) -> None:
        url = self.api_url + "attribGetAttributeValues"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "attributeCodeFilter":  attribute_code_filter,
            "codeResultKeys":       code_result_keys,
            "conditionResultKeys":  condition_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        return res.json()["result"]["conditionResultValues"]

    # TODO (alugo): Add function for attribGetAttributeValues
    def attribGetAttributeValues(self,  station_number: str, 
                                        serial_number: str, 
                                        attribute_code_array: list[str],
                                        attribute_result_keys: list[str] = ["ATTRIBUTE_CODE", "ATTRIBUTE_VALUE", "ERROR_CODE"]
                                ) -> list[str]:
        
        """
        Gets the values of an attribute.
        
        Attribute:
            station_number:         (str): Capacity or statio number id.
            serial_number:          (str): Part serial number (PYYXXXXXXXXXX).
            attribute_code_array:   (list[str]): List of attribute codes to read values from.
        """
        url = self.api_url + "attribGetAttributeValues"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        station_number,
            "objectType":           0,
            "objectNumber":         serial_number,
            "objectDetail":         "-1",
            "attributeCodeArray":   attribute_code_array,
            "allMergeLevel":        0,
            "attributeResultKeys":  attribute_result_keys
        }

        res = requests.post(url=url, data=json.dumps(payload), headers=HEADERS)
        res.raise_for_status()
        return res.json()["result"]["attributeResultValues"]