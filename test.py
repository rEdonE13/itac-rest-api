"""Test iTAC API functionality."""

from itac import ITAC


itac = ITAC()
itac.login()

# Fetch SIM related data.
serial_number = ""
attributes = [""]

sim_data = itac.getAttributesFromSerialNumber(serial_number, attributes)

itac.logout()

print(sim_data)
