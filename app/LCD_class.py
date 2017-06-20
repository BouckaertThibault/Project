# importeren nodige librarys
import RPi.GPIO as GPIO
import time

class LCD():

    def __init__(self, par_RS, par_E, par_D4, par_D5, par_D6, par_D7):
        GPIO.setmode(GPIO.BCM)
        self.RS = par_RS
        self.E = par_E
        self.D4 = par_D4
        self.D5 = par_D5
        self.D6 = par_D6
        self.D7 = par_D7
        GPIO.setwarnings(False)
        GPIO.setup(self.RS, GPIO.OUT)
        GPIO.setup(self.E, GPIO.OUT)
        GPIO.setup(self.D4, GPIO.OUT)
        GPIO.setup(self.D5, GPIO.OUT)
        GPIO.setup(self.D6, GPIO.OUT)
        GPIO.setup(self.D7, GPIO.OUT)

# functies
    def ehoog_instructie(self):
        GPIO.output(self.RS, GPIO.LOW)
        GPIO.output(self.E, GPIO.HIGH)

    def elaag_instructie(self):
        GPIO.output(self.RS, GPIO.LOW)
        GPIO.output(self.E, GPIO.LOW)

    def ehoog_data(self):
        GPIO.output(self.RS, GPIO.HIGH)
        GPIO.output(self.E, GPIO.HIGH)

    def elaag_data(self):
        GPIO.output(self.RS, GPIO.HIGH)
        GPIO.output(self.E, GPIO.LOW)

    def set_GPIO_data_bits_4bits(self, data):
        filter = 0x8
        list = []
        for i in range(0, 4):
            bit = data & filter
            filter = filter >> 1
            if (bit == 0):
                list.append(bit)
            else:
                list.append(1)

        GPIO.output(self.D7, list[0])
        GPIO.output(self.D6, list[1])
        GPIO.output(self.D5, list[2])
        GPIO.output(self.D4, list[3])

    def function_set_4bits(self):
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x28 >> 4)
        self.elaag_instructie()
        time.sleep(0.05)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x28)
        self.elaag_instructie()
        time.sleep(0.05)

    def function_on_4bits(self):
        self.ehoog_instructie()
        on_number = 0x0f
        self.set_GPIO_data_bits_4bits(on_number >> 4)
        self.elaag_instructie()
        time.sleep(0.05)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(on_number)
        self.elaag_instructie()
        time.sleep(0.05)

    def ClearDisplay(self):
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x01 >> 4)
        self.elaag_instructie()
        time.sleep(0.05)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x01)
        self.elaag_instructie()
        time.sleep(0.05)

    def WriteText(self, zin):
        if (len(zin) > 32):
            self.ClearDisplay()
            location = 0
            zin = "te veel characters"
            zin_lijst = list(zin)
            for item in zin_lijst:
                if (location == 16):
                    self.function_cursor_4bits(0xc0)
                self.data_write_char_4bits(item)
                location += 1
        else:
            self.ClearDisplay()
            location = 0
            zin_lijst = list(zin)
            for item in zin_lijst:
                if (location == 16):
                    self.function_cursor_4bits(0xc0)
                self.data_write_char_4bits(item)
                location += 1

    def function_init_4bits(self):
        self.soft_reset_4bit()
        self.function_set_4bits()
        self.function_on_4bits()
        self.ClearDisplay()

    def function_cursor_4bits(self, data):
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(data >> 4)
        self.elaag_instructie()
        time.sleep(0.05)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(data)
        self.elaag_instructie()
        time.sleep(0.05)

    def data_write_char_4bits(self, character):
        self.ehoog_data()
        self.set_GPIO_data_bits_4bits(ord(character) >> 4)
        self.elaag_data()
        time.sleep(0.05)
        self.ehoog_data()
        self.set_GPIO_data_bits_4bits(ord(character))
        self.elaag_data()
        time.sleep(0.05)

    def soft_reset_4bit(self):
        time.sleep(0.2)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x03)
        self.elaag_instructie()
        time.sleep(0.5)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x03)
        self.elaag_instructie()
        time.sleep(0.1)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x03)
        self.elaag_instructie()
        time.sleep(0.1)
        self.ehoog_instructie()
        self.set_GPIO_data_bits_4bits(0x02)
        self.elaag_instructie()


    def uitzetten(self):
        GPIO.output(self.RS, GPIO.LOW)
        GPIO.output(self.E, GPIO.LOW)
        GPIO.output(self.D4, GPIO.LOW)
        GPIO.output(self.D5, GPIO.LOW)
        GPIO.output(self.D6, GPIO.LOW)
        GPIO.output(self.D7, GPIO.LOW)
        GPIO.cleanup()


    # def get_ip(self):
    #     addrs = netifaces.ifaddresses('eth0')
    #     ip = str(addrs[netifaces.AF_INET][0].get('addr'))
    #     ip_list = list(ip)
    #     return ip_list


