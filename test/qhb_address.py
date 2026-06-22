class QHB_ADDRESS_MAP:

    def __init__(self):
        self.PACK_DATA_1 = 0x18F
        self.PACK_DATA_2 = 0x28F
        self.MAXIMUM_ALLOWED_VALUES = 0x351
        self.VICTRON_BASED_SERVICE = 0x356

        self.NODE_ID = 15
        self.INDIVIDUAL_DATA_BASE = 0x480

        self.UNIT_PERCENT = "%"
        self.UNIT_VOLT = "V"
        self.UNIT_CURRENT = "A"
        self.UNIT_TEMP = "°C"

        self.BATTERY_STATE = {
            10: "Standby",
            20: "Ready",
            30: "Disengaged",
            40: "Discharging",
            50: "Charging"
        }

        self.TEMP_OFFSET = 55

        # Pack Data 1
        self.PD1_SOC = 0
        self.PD1_VOLTAGE_LSB = 1
        self.PD1_VOLTAGE_MSB = 2
        self.PD1_ACTIVE_BAT = 6
        self.PD1_PASSIVE_BAT = 7

        # Pack Data 2
        self.PD2_PACK_STATE = 0
        self.PD2_CURRENT_LSB = 1
        self.PD2_CURRENT_MSB = 2
        self.PD2_SMART_CHARGER = 5
        self.PD2_MAX_TEMP = 6
        self.PD2_MIN_TEMP = 7


        self.IND_PERMISSION = 0
        self.IND_HEATING_MODE = 1
        self.IND_VIRTUAL_ID_PACK = 2
        self.IND_VIRTUAL_ID_CELL = 3
        self.IND_SOC = 4
        self.IND_STATE_OF_BATTERY = 5
        self.IND_CURRENT = 6
        self.IND_TEMP = 7

        # Limits
        self.MAX_CHARGE_VOLT_LSB = 0
        self.MAX_CHARGE_VOLT_MSB = 1

        self.MAX_CHARGE_CURR_LSB = 2
        self.MAX_CHARGE_CURR_MSB = 3

        self.MAX_DISCHARGE_CURR_LSB = 4
        self.MAX_DISCHARGE_CURR_MSB = 5

        self.MAX_DISCHARGE_VOLT_LSB = 6
        self.MAX_DISCHARGE_VOLT_MSB = 7

        # Battery live data
        self.BAT_SOC = 4
        self.BAT_CURRENT = 5
        self.BAT_TEMP = 6
        self.BAT_STATE = 7