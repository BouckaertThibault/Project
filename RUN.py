from LCD_class import LCD
from hcsr04sensor import sensor
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
scherm = LCD(25, 27, 5, 6, 13, 19)
waterpomp = 21
GPIO.setup(waterpomp, GPIO.OUT)
tempsensor = '/sys/bus/w1/devices/28-8000001f5c2a/w1_slave'
trig_waterbak = 18
echo_waterbak = 23
trig_reservoir = 24
echo_reservoir = 17

#####volume variabelen voor reservoir#####
meting_vol = 4.3            #afstand sensor met een vol reservoir
meting_leeg = 16.3          #afstand sensor met een leeg reservoir
volume_vol = 3.0            #max volume reservoir
volume_leeg = 0.0           #min volume reservoir



def lees_waterbak():
    value = sensor.Measurement(trig_waterbak, echo_waterbak)
    raw_measurement = value.raw_distance()
    metric_distance = value.distance_metric(raw_measurement)
    return metric_distance


def lees_reservoir():
    value = sensor.Measurement(trig_reservoir, echo_reservoir)
    raw_measurement = value.raw_distance()
    metric_distance = value.distance_metric(raw_measurement)
    return metric_distance


def lees_temperatuur():
    f = open(tempsensor, 'r')
    line1 = f.readlines()
    f.close()

    line2 = line1
    while line2[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        line2 = line1
    equals_pos = line2[1].find('t=')
    if equals_pos != -1:
        temp_string = line2[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000.0
        round(temp_c, 1)
        return temp_c


def lcd():
    LCD.WriteText(scherm, "Reservoir: " + str(meting_naar_liter()) + "L" + "Temp: " + str(round(lees_temperatuur(), 1)) + chr(223) + "C")


def waterpomp_aan():
    GPIO.output(waterpomp, GPIO.HIGH)


def waterpomp_uit():
    GPIO.output(waterpomp, GPIO.LOW)

def meting_naar_liter():
    a = (volume_vol - volume_leeg) / (meting_vol - meting_leeg)
    b = volume_leeg - a * meting_leeg
    liter = a * lees_reservoir() + b
    return liter


try:
    print(str(lees_reservoir()) + " cm " + str(round(meting_naar_liter(), 2)) + " L")
    lcd()

except(KeyboardInterrupt):
    LCD.uitzetten(scherm)


