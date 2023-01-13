"""Test iTAC API functionality."""

from itac import ITAC
from itacconfig import CAPACITY
from itacconfig import USER_ID

station_settings = []

top_failures_filter = {"key": "PRODUCT_NUMBER", "value": "2609-100-488-51"}
top_failures_result_keys = ["FAILURE_CAUSE_DESC", "FAILURE_COUNT", "REPAIRED"]

itac = ITAC()
itac.login(USER_ID)
# station_settings = itac.trGetStationSetting(CAPACITY, ["WORKORDER_NUMBER", "PART_NUMBER"])
# top_failures = itac.trGetTopFailures(CAPACITY, top_failures_filter, top_failures_result_keys)

# Fetch SIM related data.
sim_data = itac.getAttributesFromSerialNumber(CAPACITY, "P22002862823", ["IMEI", "IMSI", "EID"])

itac.logout()

# print(station_settings)
# print(top_failures)
print(sim_data)
