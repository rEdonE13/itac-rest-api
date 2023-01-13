import json
import requests
from itac import ITAC


class Attribute(ITAC):
    # TODO (alugo): Add documentation
    
    
    def trGetSerialNumberInfo(self, 
                                serial_number: str, 
                                result_keys: list[str]
                            ) -> list[str]:
        # TODO (alugo): Add information for this function
        url = self.api_url + "trGetSerialNumberInfo"
        payload = {
            "sessionContext":       self.session_context,
            "stationNumber":        "35061400",
            "serialNumber":         serial_number,
            "serialNumberPos":      "-1",
            "serialNumberResultKeys":  result_keys
        }
    
        res = requests.post(url=url, data=json.dumps(payload), headers=self.headers)
        res.raise_for_status()
        return res.json()["result"]["serialNumberResultValues"]