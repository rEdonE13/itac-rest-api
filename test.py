"""Test iTAC API functionality."""

from itac import ITAC
from itacconfig import CAPACITY
from itacconfig import USER_ID


itac = ITAC()
itac.login(USER_ID)

# Fetch SIM related data.
sim_data = itac.getAttributesFromSerialNumber(CAPACITY, "P22002862823", ["IMEI", "IMSI", "EID"])

itac.logout()

print(sim_data)
