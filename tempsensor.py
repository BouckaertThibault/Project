import time

sensor_file = '/sys/bus/w1/devices/28-8000001f5c2a/w1_slave'


def read_temp_raw():
    f = open(sensor_file, 'r')
    lines = f.readlines()
    f.close()
    return lines


def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        zin = ("Het is : " + str(temp_c) + "\N{DEGREE SIGN}C")
        return zin


while True:
    print(read_temp())
    time.sleep(1)


