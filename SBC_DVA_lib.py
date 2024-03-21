# Import of Librarys
import time, math
from smbus2 import SMBus

# Address variables ina236A
GND_A = 0x40    # 1000000b
VS_A = 0x41     # 1000001b
SDA_A = 0x42    # 1000010b
SCL_A = 0x43    # 1000011b

# Address variables ina236B
GND_B = 0x48    # 1001000b
VS_B = 0x49     # 1001001b
SDA_B = 0x4A    # 1001010b
SCL_B = 0x4B    # 1001011b

_ADDRESS_A = [
    GND_A,    # 1000000b
    VS_A,     # 1000001b
    SDA_A,    # 1000010b
    SCL_A     # 1000011b
]

_ADDRESS_B = [
    GND_B,    # 1001000b
    VS_B,     # 1001001b
    SDA_B,    # 1001010b
    SCL_B     # 1001011b
]

# Register variables
Config_Reg =          0x00
Shunt_Volt_Reg =      0x01
Bus_Volt_Reg =        0x02
Power_Reg =           0x03
Current_Reg =         0x04
Calibration_Reg =     0x05
Mask_Enable_Reg =     0x06
Alert_Limit_Reg =     0x07
Manufacturer_ID_Reg = 0x3E
Device_ID_Reg =       0x3F

# Reset
RST = 0x8000

# Range of the ADC
ADCRANGE_1 = 0x0000    # �81.92mV (default)
ADCRANGE_2 = 0x1000    # �20.48mV

_ADCRANGE = [
    ADCRANGE_1,    # �81.92mV (default)
    ADCRANGE_2     # �20.48mV
]

# List of voltage values corresponding to the list of _ADCRANGE
_LSB = [
    0.0000025,     # Shunt Voltage, �81.92mV | 2.5uV
    0.000000625,   # Shunt Voltage, �20.48mV | 625nV
    0.0016         # Bus Voltage | 1.6mV
]

# ADC values to be averaged
AVG_1 = 0x0000    # 1 (default)
AVG_2 = 0x0200    # 4
AVG_3 = 0x0400    # 16
AVG_4 = 0x0600    # 64
AVG_5 = 0x0800    # 128
AVG_6 = 0x0A00    # 256
AVG_7 = 0x0C00    # 512
AVG_8 = 0x0E00    # 1024

_AVG = [
    AVG_1,    # 1 (default)
    AVG_2,    # 4
    AVG_3,    # 16
    AVG_4,    # 64
    AVG_5,    # 128
    AVG_6,    # 256
    AVG_7,    # 512
    AVG_8     # 1024
]

# Conversion time for the VBUS measurement
VBUSCT_1 = 0x0000    # 140us
VBUSCT_2 = 0x0040    # 204us
VBUSCT_3 = 0x0080    # 332us
VBUSCT_4 = 0x00C0    # 588us
VBUSCT_5 = 0x0100    # 1100us (default)
VBUSCT_6 = 0x0140    # 2116us
VBUSCT_7 = 0x0180    # 4156us
VBUSCT_8 = 0x01C0    # 8244us

_VBUSCT = [
    VBUSCT_1,    # 140us
    VBUSCT_2,    # 204us
    VBUSCT_3,    # 332us
    VBUSCT_4,    # 588us
    VBUSCT_5,    # 1100us (default)
    VBUSCT_6,    # 2116us
    VBUSCT_7,    # 4156us
    VBUSCT_8     # 8244us
]

# Conversion time for the SHUNT measurement
VSHCT_1 = 0x0000    # 140us
VSHCT_2 = 0x0008    # 204us
VSHCT_3 = 0x0010    # 332us
VSHCT_4 = 0x0018    # 588us
VSHCT_5 = 0x0020    # 1100us (default)
VSHCT_6 = 0x0028    # 2116us
VSHCT_7 = 0x0030    # 4156us
VSHCT_8 = 0x0038    # 8244us

_VSHCT = [
    VSHCT_1,    # 140us
    VSHCT_2,    # 204us
    VSHCT_3,    # 332us
    VSHCT_4,    # 588us
    VSHCT_5,    # 1100us (default)
    VSHCT_6,    # 2116us
    VSHCT_7,    # 4156us
    VSHCT_8     # 8244us
]

# Operating Mode
MODE_1 = 0x0000    # Shutdown
MODE_2 = 0x0001    # Shunt Voltage triggered, single shot
MODE_3 = 0x0002    # Bus Voltage triggered, single shot
MODE_4 = 0x0003    # Shunt voltage and Bus voltage triggered, single shot
MODE_5 = 0x0004    # Shutdown
MODE_6 = 0x0005    # Continuous Shunt voltage
MODE_7 = 0x0006    # Continuous Bus voltage
MODE_8 = 0x0007    # Continuous Shunt and Bus voltage (default)

_MODE = [
    MODE_1,    # Shutdown
    MODE_2,    # Shunt Voltage triggered, single shot
    MODE_3,    # Bus Voltage triggered, single shot
    MODE_4,    # Shunt voltage and Bus voltage triggered, single shot
    MODE_5,    # Shutdown
    MODE_6,    # Continuous Shunt voltage
    MODE_7,    # Continuous Bus voltage
    MODE_8     # Continuous Shunt and Bus voltage (default)
]

_MASK_ENABLE = [
    0x8000,    # SOL (Shunt Over-limit)
    0x4000,    # SUL (Shunt Under-limit)
    0x2000,    # BOL (Bus Over-limit)
    0x1000,    # BUL (Bus Under-limit)
    0x0800,    # POL (Power Over-limit)
    0x0400,    # CNVR (Conversion Ready)
    0x0020,    # MemError
    0x0010,    # AFF (Alert Function Flag)
    0x0008,    # CVRF (Conversion Ready Flag)
    0x0004     # OVF (Math Over-flow)
]

bus = SMBus(1)

# All global variables used in the library
Current_lsb = 0
Lsb = _LSB[0]
Address = _ADDRESS_A[0]
Mode = _MODE[7]
Vshct = _VSHCT[4]
Vbusct = _VBUSCT[4]
Avg = _AVG[0]
Adcrange = _ADCRANGE[0]
temp = bytearray(2)

# Write the required 16-bit value into the register
def _write_register(reg, val):
    global Address
    temp[0] = val >> 8
    temp[1] = val & 0xff
    bus.write_i2c_block_data(Address, reg, temp)

# Read the 16-bit register value that will be returned
def _read_register(reg):
    global Address
    data = bus.read_i2c_block_data(Address, reg, 2)
    return ((data[0] << 8) | data[1])

# Initialize the INA236 with the user-specified parameters
def init_ina236(address, mode, vshct, vbusct, avg, adcrange):
    global Mode, Vshct, Vbusct, Avg, Adcrange, Address, Lsb
    
    Mode = _MODE[mode]
    Vshct = _VSHCT[vshct]
    Vbusct = _VBUSCT[vbusct]
    Avg = _AVG[avg]
    Adcrange = _ADCRANGE[adcrange]

    Address = _ADDRESS_A[address]
    if (Adcrange == ADCRANGE_1):
        Lsb = _LSB[0]
    else:
        Lsb = _LSB[1]

    config = 0x0000
    config |= Mode
    config |= Vshct
    config |= Vbusct
    config |= Avg
    config |= Adcrange
    _write_register(Config_Reg, config)

# Reset the INA236 registers
def reset_ina236(address):
    Address = address
    _write_register(Config_Reg, RST)

# Calibrate the INA236 for the correct Shunt measurement
def calibrate_ina236():
    global Adcrange, Current_lsb
    
    current_lsb_min = 10 / (math.pow(2, 15))
    Current_lsb = current_lsb_min + 0.0018
    SHUNT_CAL = 0.00512 / (Current_lsb * 0.008)
    SHUNT_CAL = math.trunc(SHUNT_CAL)
    if (Adcrange == ADCRANGE_2):
        SHUNT_CAL = SHUNT_CAL / 4
    _write_register(Calibration_Reg, SHUNT_CAL)

# Read the current across the Shunt resistor
def read_current():
    global Current_lsb
    CURRENT = _read_register(Current_Reg)
    return round((Current_lsb * CURRENT), 4)

# Read the power across the Shunt resistor
def read_power():
    global Current_lsb
    POWER = _read_register(Power_Reg)
    return round(math.fabs((32 * Current_lsb * POWER)), 4)

# Read the voltage across the Shunt resistor
def read_shunt_voltage():
    value_raw = _read_register(Shunt_Volt_Reg)
    value_comp = ~value_raw
    value = value_comp + 1
    return round(math.fabs(value * Lsb), 4)

# Read the bus voltage
def read_bus_voltage():
    value = _read_register(Bus_Volt_Reg)
    return round((value * _LSB[2]), 4)

# Set the alert register
def mask_enable(val=1):
    out = _MASK_ENABLE[val]
    _write_register(Mask_Enable_Reg, out)

# Write a value into the alert register as reference
def write_alert_limit(val=0x294):
    _write_register(Alert_Limit_Reg, val)

# Read the value from the alert register
def read_alert_limit():
    raw = _read_register(Alert_Limit_Reg)
    print("Mask/Alert register value: " + str(raw))

# Read the Manufacturer ID
def manufacturer_ID():
    if (_read_register(Manufacturer_ID_Reg) == 21577):
        print("Manufacturer ID: TI")
    else:
        print("Manufacturer ID: nan")

# Read the Device ID
def device_ID():
    print("Device ID: " + str(_read_register(Device_ID_Reg)))
