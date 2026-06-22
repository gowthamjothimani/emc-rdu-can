import can
from qhb_address import QHB_ADDRESS_MAP


class CAN_QHB:

    def __init__(self):
        self.addr = QHB_ADDRESS_MAP()
        self.bus = None

    #  INIT DEVICE 
    def init_device(self):
        try:
            self.bus = can.interface.Bus(
                channel="can1",
                bustype="socketcan"
            )
            print("[CAN] CAN1 initialized successfully")
        except Exception as e:
            print(f"[ERROR] CAN1 initialization failed: {e}")
            self.bus = None

    #  LISTEN 
    def start_device(self):
        if not self.bus:
            print("[ERROR] CAN bus not initialized")
            return

        print("[CAN] Listening on CAN1 ...")

        while True:
            msg = self.bus.recv(timeout=1.0)
            if msg is None:
                continue

            # PACK DATA 1
            if msg.arbitration_id == self.addr.PACK_DATA_1:
                self.decode_pack_data_1(msg.data)

            # PACK DATA 2
            elif msg.arbitration_id == self.addr.PACK_DATA_2:
                self.decode_pack_data_2(msg.data)

            # MAXIMUM ALLOWED PACK VALUES   
            elif msg.arbitration_id == self.addr.MAXIMUM_ALLOWED_VALUES:
                self.decode_pack_data_3(msg.data)
            
            elif msg.arbitration_id >= self.addr.INDIVIDUAL_DATA_BASE:
                self.decode_individual_battery(msg.data)
            

    #  DECODE 
    def decode_pack_data_1(self, data):
        if len(data) < 8:
            return

        soc = data[self.addr.PD1_SOC]
        voltage_raw = (data[self.addr.PD1_VOLTAGE_MSB] << 8) | data[self.addr.PD1_VOLTAGE_LSB]
        voltage = voltage_raw / 1024
        active_bat = data[self.addr.PD1_ACTIVE_BAT]
        passive_bat = data[self.addr.PD1_PASSIVE_BAT]

        print("\n=== PACK DATA 1 (0x18F) ===")
        print(f"SoC        : {soc}{self.addr.UNIT_PERCENT}")
        print(f"Voltage    : {voltage:.2f}{self.addr.UNIT_VOLT}")
        print(f"Active Bat : {active_bat}")
        print(f"Passive Bat: {passive_bat}")

    #  DECODE 0x28F 
    def decode_pack_data_2(self, data):
        try:
            if len(data) < 8:
                return
            # Pack state
            pack_state = data[self.addr.PD2_PACK_STATE]
            state_text = self.addr.BATTERY_STATE.get(pack_state, "Unknown")

            curr_raw = (
                (data[self.addr.PD2_CURRENT_MSB] << 8) |
                data[self.addr.PD2_CURRENT_LSB]
            )

            if curr_raw & 0x8000:
                curr_raw = curr_raw - 0x10000

            raw_max_temp = data[self.addr.PD2_MAX_TEMP]
            raw_min_temp = data[self.addr.PD2_MIN_TEMP]
            max_temp = (raw_max_temp - self.addr.TEMP_OFFSET) + 7
            min_temp = (raw_min_temp - self.addr.TEMP_OFFSET) + 7
            smart_charger = data[self.addr.PD2_SMART_CHARGER]
            charger_status = "Connected" if smart_charger == 1 else "Not Connected"

            print("\n=== PACK DATA 2 (0x28F) ===")
            print(f"State      : {pack_state} ({state_text})")
            print(f"Current    : {curr_raw / 10.0:.1f}{self.addr.UNIT_CURRENT}")
            print(f"Max Temp   : {max_temp}{self.addr.UNIT_TEMP}")
            print(f"Min Temp   : {min_temp}{self.addr.UNIT_TEMP}")
            print(f"Charger Status: {charger_status}")
   
        except Exception as e:
            print(f"[ERROR] PD2 decode failure: {e}")


    def decode_pack_data_3(self, data):
        try:
            if len(data) < 8:
                return

            max_charge_voltage = ((data[1] << 8) | data[0]) / 10.0
            max_charge_current = ((data[3] << 8) | data[2]) / 10.0
            max_discharge_current = ((data[5] << 8) | data[4]) / 10.0
            max_discharge_voltage = ((data[7] << 8) | data[6]) / 10.0

            print("\n=== PACK LIMITS (0x351) ===")
            print(f"Max Charge Voltage   : {max_charge_voltage:.1f}{self.addr.UNIT_VOLT}")
            print(f"Max Charge Current   : {max_charge_current:.1f}{self.addr.UNIT_CURRENT}")
            print(f"Max Discharge Current: {max_discharge_current:.1f}{self.addr.UNIT_CURRENT}")
            print(f"Max Discharge Volt   : {max_discharge_voltage:.1f}{self.addr.UNIT_VOLT}")

        except Exception as e:
            print(f"[ERROR] 0x351 decode failure: {e}")
    
    def decode_individual_battery(self, data):
        try:
            if len(data) < 8:
                return
            permission = data[self.addr.IND_PERMISSION]
            heating_mode = data[self.addr.IND_HEATING_MODE]
            virtual_id = data[self.addr.IND_VIRTUAL_ID_PACK]
            virtual_cell = data[self.addr.IND_VIRTUAL_ID_CELL]
            soc = data[self.addr.IND_SOC]
            state = data[self.addr.IND_STATE_OF_BATTERY]
            raw_current = data[self.addr.IND_CURRENT]

            if raw_current & 0x80:
                raw_current = raw_current - 0x100

            current = raw_current / 10.0
            temp = data[self.addr.IND_TEMP] - self.addr.TEMP_OFFSET
            state_text = self.addr.BATTERY_STATE.get(state, "Unknown")

            print("\n=== INDIVIDUAL BATTERY (0x48F) ===")
            print(f"Permission   : {permission}")
            print(f"Heating Mode : {heating_mode}")
            print(f"Virtual Pack : {virtual_id}")
            print(f"Virtual Cell : {virtual_cell}")
            print(f"SoC          : {soc}{self.addr.UNIT_PERCENT}")
            print(f"State        : {state} ({state_text})")
            print(f"Current      : {current:.1f}{self.addr.UNIT_CURRENT}")
            print(f"Temperature  : {temp}{self.addr.UNIT_TEMP}")
            print("-------------------------------")

        except Exception as e:
            print(f"[ERROR] 0x48F decode failure: {e}")


#  MAIN 
if __name__ == "__main__":
    node = CAN_QHB()
    node.init_device()
    node.start_device()