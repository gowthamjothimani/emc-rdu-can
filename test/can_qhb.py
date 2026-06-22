import can
import time
from qhb_address import QHB_ADDRESS_MAP


class CAN_QHB:

    def __init__(self):
        self.addr = QHB_ADDRESS_MAP()
        self.bus = None

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

    def start_listen(self):
        if not self.bus:
            print("[ERROR] CAN bus not initialized")
            return

        print("[CAN] Listening on CAN1 ...")

        while True:
            msg = self.bus.recv(timeout=1.0)

            if msg is None:
                continue
            if msg.arbitration_id == self.addr.PACK_DATA_1:
                self.decode_pack_data_1(msg.data)

    # PACK DATA 1 
    def decode_pack_data_1(self, data):
        try:
            # Safety check
            if len(data) < 8:
                return
            soc = data[self.addr.PD1_SOC]

            voltage_raw = (data[self.addr.PD1_VOLTAGE_MSB] << 8) | data[self.addr.PD1_VOLTAGE_LSB]
            voltage = voltage_raw / 1024

            active_bat = data[self.addr.PD1_ACTIVE_BAT]
            passive_bat = data[self.addr.PD1_PASSIVE_BAT]

            # Print output
            print("\nPACK DATA 1 (0x18F)")
            print(f"SOC        : {soc}{self.addr.UNIT_PERCENT}")
            print(f"Voltage    : {voltage:.2f}{self.addr.UNIT_VOLT}")
            print(f"Active Bat : {active_bat}")
            print(f"Passive Bat: {passive_bat}")
            print("-------------------------------") 

        except Exception as e:
            print(f"[ERROR] Decode failure: {e}")


#  MAIN 
if __name__ == "__main__":
    node = CAN_QHB()
    node.init_device()
    node.start_listen()