"""Test iTAC API functionality."""

from itac import ITAC


itac = ITAC()
itac.login()

# Fetch SIM related data.
sim_data = itac.getAttributesFromSerialNumber("P22002862823", ["IMEI", "IMSI", "EID"])

itac.logout()

print(sim_data)
