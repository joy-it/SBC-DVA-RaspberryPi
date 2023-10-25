# Import all required libraries
import SBC_DVA_lib
import time
import sys

if __name__ == '__main__':
    try:
        # Initialize the INA236
        SBC_DVA_lib.reset_ina236(0x40)
        SBC_DVA_lib.init_ina236(0, 7, 4, 4, 0, 0)
        SBC_DVA_lib.calibrate_ina236()
        SBC_DVA_lib.mask_enable(1)
        SBC_DVA_lib.write_alert_limit()
        SBC_DVA_lib.read_alert_limit()
        time.sleep(5)
        SBC_DVA_lib.manufacturer_ID()
        SBC_DVA_lib.device_ID()
        print("start")
        while True:
            # Main loop
            # Read Current, Power, Shunt Voltage and Bus Voltage from the corresponding registers
            current = SBC_DVA_lib.read_current()
            power = SBC_DVA_lib.read_power()
            shunt_voltage = SBC_DVA_lib.read_shunt_voltage()
            bus_voltage = SBC_DVA_lib.read_bus_voltage()
            # Output the read values from the registers
            print(f"Current [A]: {current}, Power [W]: {power}, Shunt [V]: {shunt_voltage}, Bus [V]: {bus_voltage}")
            time.sleep(1)

    except KeyboardInterrupt:
        sys.exit()
