import array
import time
import io
import fcntl

HDC2000_ADDRESS = 0x40  # 1000000
# Register
# 2 bytes
HDC2000_TEMPERATURE_REGISTER = 0x00
HDC2000_TEMPERATURE_OFFSET_REGISTER = 0x08

HDC2000_HUMIDITY_REGISTER = 0x02
HDC2000_HUMIDITY_OFFSET_REGISTER = 0x09

HDC2000_RESET_REGISTER = 0x0E
HDC2000_CONFIG_REGISTER = 0x0F
HDC2000_MANUFACTURERID_REGISTER = 0xFC
HDC2000_DEVICEID_REGISTER = 0xFE

# Configuration Register Bits
HDC2000_RESET_RESET_BIT = 0x80
HDC2000_RESET_HEATER_ENABLE = 0x8
HDC2000_CONFIG_GO = 0x1

# Offsets for temp and humidity
TEMP_OFFSET_VALUE = 0xE0
HUM_OFFSET_VALUE = 0x40

I2C_SLAVE = 0x0703

HDC2000_fw = 0
HDC2000_fr = 0


class Pi_HDC2080:
    def readManufacturerID(self):
        s = [HDC2000_MANUFACTURERID_REGISTER]
        s2 = bytearray(s)
        HDC2000_fw.write(s2)
        time.sleep(0.0625)
        data = HDC2000_fr.read(2)  # read 2 byte config data
        buf = array.array('B', data)
        return buf[0] * 256 + buf[1]


    def readDeviceID(self):
        s = [HDC2000_DEVICEID_REGISTER]
        s2 = bytearray(s)
        HDC2000_fw.write(s2)
        time.sleep(0.0625)
        data = HDC2000_fr.read(2)  # read 2 byte config data
        buf = array.array('B', data)
        return buf[0] * 256 + buf[1]

    def __init__(self, twi=1, addr=HDC2000_ADDRESS):
        global HDC2000_fr, HDC2000_fw

        HDC2000_fr = io.open("/dev/i2c-" + str(twi), "rb", buffering=0)
        HDC2000_fw = io.open("/dev/i2c-" + str(twi), "wb", buffering=0)

        a1 = fcntl.ioctl(HDC2000_fr, I2C_SLAVE, HDC2000_ADDRESS)
        a2 = fcntl.ioctl(HDC2000_fw, I2C_SLAVE, HDC2000_ADDRESS)
        if (a1 < 0 or a2 < 0):
            exit()  # abort
        time.sleep(0.1)
        config = HDC2000_RESET_RESET_BIT
        s = [HDC2000_RESET_REGISTER, config]
        s2 = bytearray(s)
        HDC2000_fw.write(s2)
        time.sleep(0.1)
        # Program the Temp offset
        offset = TEMP_OFFSET_VALUE
        s = [HDC2000_TEMPERATURE_OFFSET_REGISTER, offset]
        s2 = bytearray(s)
        HDC2000_fw.write(s2)
        time.sleep(0.1)
        # Program the Humidity offset
        offset = HUM_OFFSET_VALUE
        s = [HDC2000_HUMIDITY_OFFSET_REGISTER, offset]
        s2 = bytearray(s)
        HDC2000_fw.write(s2)
        time.sleep(0.1)
        print('Manufacturer ID: {}'.format(self.readManufacturerID()))
        if (self.readManufacturerID() != 0x4954):
            print("ERROR CRITICAL MANUFACTURE ID NOT MATCH")
            exit()
        if (self.readDeviceID() != 0xD007):
            print("ERROR CRITICAL DEVICE ID NOT MATCH")
            exit()

    def setTemperatureOffset(self):
        s = [HDC2000_CONFIG_REGISTER, HDC2000_CONFIG_GO]
        HDC2000_fw.write(bytearray(s))  # GO
        s = [HDC2000_TEMPERATURE_OFFSET_REGISTER]  # temp offset
        HDC2000_fw.write(bytearray(s))
        time.sleep(0.1)  # wait for measure to be done
        data = HDC2000_fr.read(2)
        buf = array.array('B', data)

        # Convert the data
        temp = (buf[0]) + (buf[1]*256)
        print('Binary Read: {}, Decimal Read: {}'.format(buf, temp))
        cTemp = (temp / 65536.0) * 165.0 - 40
        return cTemp

    # public functions
    def readTemperature(self):
        s = [HDC2000_CONFIG_REGISTER, HDC2000_CONFIG_GO]
        HDC2000_fw.write(bytearray(s))  # GO
        s = [HDC2000_TEMPERATURE_REGISTER]  # temp
        HDC2000_fw.write(bytearray(s))
        time.sleep(0.1)  # wait for measure to be done
        data = HDC2000_fr.read(2)
        buf = array.array('B', data)

        # Convert the data
        temp = (buf[0]) + (buf[1]*256)
        #print('Binary Read: {}, Decimal Read: {}'.format(buf, temp))
        cTemp = (temp / 65536.0) * 165.0 - 40
        return cTemp

    def readHumidity(self):
        s = [HDC2000_CONFIG_REGISTER, HDC2000_CONFIG_GO]
        HDC2000_fw.write(bytearray(s))  # GO
        s = [HDC2000_HUMIDITY_REGISTER]  # humidity
        HDC2000_fw.write(bytearray(s))
        time.sleep(0.1)
        data = HDC2000_fr.read(2)  # read 2 byte humidity data
        buf = array.array('B', data)
        humidity = (buf[0]) + (buf[1] * 256)
        humidity = (humidity / 65536.0) * 100.0
        return humidity

    def readConfigRegister(self):
        s = [HDC2000_CONFIG_REGISTER]  # temp
        s2 = bytearray(s)
        HDC2000_fw.write(s2)
        data = HDC2000_fr.read(1)  # read 2 byte config data
        buf = array.array('B', data)
        print(data)
        print(buf)
        return buf[0]

    def turnHeaterOn(self):
        return

    def turnHeaterOff(self):
        return

    def setHumidityResolution(self, resolution):
        return

    def setTemperatureResolution(self, resolution):
        return


if __name__ == "__main__":
    hdc2000 = Pi_HDC2080()

    while True:
        print('Temperature: {}C'.format(round(hdc2000.readTemperature(), 2)))
        print('Humidity: {}%'.format(round(hdc2000.readHumidity(), 2)))
        time.sleep(1)
