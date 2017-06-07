import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

waterpomp = 21

GPIO.setup(waterpomp, GPIO.OUT)

# while True:
#     try:
GPIO.output(waterpomp, True)
time.sleep(17)


while True:
    GPIO.output(waterpomp, False)



    # except(KeyboardInterrupt):
    #     print("Programma afsluiten")
    #     GPIO.output(waterpomp, False)