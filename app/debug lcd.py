import RPi.GPIO as GPIO
import time

#pinnen benoemen(verander dit als je anders hebt geschakeled)
# !!!! niet pin 4 !!!
rs = 25
rw = 26
e = 27
d4 = 5
d5 = 6
d6 = 13
d7 = 19


GPIO.setmode(GPIO.BCM)
GPIO.setup(rs, GPIO.OUT)
GPIO.setup(rw, GPIO.OUT)
GPIO.setup(e, GPIO.OUT)
GPIO.setup(d4, GPIO.OUT)
GPIO.setup(d5, GPIO.OUT)
GPIO.setup(d6, GPIO.OUT)
GPIO.setup(d7, GPIO.OUT)
print ("programming is running!!!")


##################FUNCTIES##################
def ehoog_instructie(): 	#hoge puls om instructie te  sturen
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(e, GPIO.HIGH)
    GPIO.output(rw, GPIO.LOW)
def elaag_instructie(): 	#lage puls om instructie te sturen
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(e, GPIO.LOW)
    GPIO.output(rw, GPIO.LOW)
def ehoog_data(): 	#hoge puls voor data te versturen(letters)
    GPIO.output(rs, GPIO.HIGH)
    GPIO.output(e, GPIO.HIGH)
    GPIO.output(rw, GPIO.LOW)
def elaag_data(): 	#lage puls voor data te versturen
    GPIO.output(rs, GPIO.HIGH)
    GPIO.output(e, GPIO.LOW)
    GPIO.output(rw, GPIO.LOW)

def set_GPIO_data_bits(data):	# een byte omvormen naar 8 pinnen
    filter = 0x8	# filter met code 1000 0000 of 128   -> naar 0000 1000
    list = []
    for i in range(0, 4): # 4 keer per bit kijken of deze een 0 of 1 is en deze dan opslaan in de list
        bit = data & filter	#en mask (1bit selecteren)
        filter = filter >> 1	#bitshift je gaat de filter aan passen van 1000 0000 naar 01000 0000 tot 0000 0001
        if (bit == 0):
            list.append(bit)
        else:
            list.append(1)
    #list 1 per 1 uitlezen en deze waarde op de pinenen zetten
    GPIO.output(d7, list[0])
    GPIO.output(d6, list[1])
    GPIO.output(d5, list[2])
    GPIO.output(d4, list[3])

def function_set():
    #deze info is voor alle instructies en data dat je verstuurt
    # je gaat eerst een puls hoog zetten voor data of instructie dan ga je een instructie versturen dan geef je een lage puls en deze gaat de waarde laten registreren op het lcd-sherm
    ehoog_instructie()
    set_GPIO_data_bits(0x28>>4) # code voor de set == 0011 1000 zie tabel waarom deze bits -> naar 0010 1000
    elaag_instructie()
    time.sleep(0.05)
    ehoog_instructie()
    set_GPIO_data_bits(0x28)  # code voor de set == 0011 1000 zie tabel waarom deze bits -> naar 0010 1000
    elaag_instructie()
    time.sleep(0.05)


def function_on():
    ehoog_instructie()
    on_number = 0x0f #code voor aanzeten van de lcd en een pinkende cursor te hebben(0000 1111)
    set_GPIO_data_bits(on_number>>4)
    elaag_instructie()
    time.sleep(0.05)
    ehoog_instructie()
    set_GPIO_data_bits(on_number)
    elaag_instructie()
    time.sleep(0.05)

def function_clear():
    ehoog_instructie()
    set_GPIO_data_bits(0x01>>4)	#code om het alles leeg te maken(0000 0001) [dit gaat ook de curor op de start positie platsen]
    elaag_instructie()
    time.sleep(0.05)
    ehoog_instructie()
    set_GPIO_data_bits(0x01) 	# code om het alles leeg te maken(0000 0001) [dit gaat ook de curor op de start positie platsen]
    elaag_instructie()
    time.sleep(0.05)



def function_init():	# gaat de 3 functies aanroepen
    soft_reset_4bit()
    function_set()
    function_on()
    function_clear()

def function_cursor(data): #cursor verplaatsen
    ehoog_instructie()
    set_GPIO_data_bits(data>>4)
    elaag_instructie()
    time.sleep(0.05)
    ehoog_instructie()
    set_GPIO_data_bits(data)
    elaag_instructie()
    time.sleep(0.05)

def data_write_char(character):
    ehoog_data()
    set_GPIO_data_bits(ord(character)>>4)	#je gaat character per character moeten werken en dan met ord deze omzetten naar ascci code waardoor je de oude functie kunt gebruiken
    elaag_data()
    time.sleep(0.05)
    ehoog_data()
    set_GPIO_data_bits(ord(character))  # je gaat character per character moeten werken en dan met ord deze omzetten naar ascci code waardoor je de oude functie kunt gebruiken
    elaag_data()
    time.sleep(0.05)

def soft_reset_4bit():
    time.sleep(0.2)
    ehoog_instructie()
    set_GPIO_data_bits(0x03)
    elaag_instructie()
    time.sleep(0.5)
    ehoog_instructie()
    set_GPIO_data_bits(0x03)
    elaag_instructie()
    time.sleep(0.1)
    ehoog_instructie()
    set_GPIO_data_bits(0x03)
    elaag_instructie()
    time.sleep(0.1)
    ehoog_instructie()
    set_GPIO_data_bits(0x02)
    elaag_instructie()


##################CODE AANROEPEN##################
try:
    function_init()
    while True:
        time.sleep(1)
        zin = input("geef een zin mee: ")
        if(len(zin)> 32):	#kijken of er niet te veel data gegeven wordt
            function_clear()
            location = 0
            zin = "te veel characters"
            zin_lijst = list(zin)
            for item in zin_lijst:
                if (location == 16):
                    function_cursor(0xc0)
                data_write_char(item)
                location += 1
        else:
            function_clear()
            location = 0
            zin_lijst = list(zin) 	# de ingelezen zin omzetten naar een array van characters bv.(hello word 'h''e''l''l''o')
            for item in zin_lijst:	#character per caracter uitlezen
                if (location == 16):	#als je op het einde van het scherm komt naar 2de lijn gaan
                    function_cursor(0xc0)	#code voor naar 2de lijn positie 0 te gaan
                data_write_char(item)	#zie functie
                location += 1


# als het progamma gestopt wordt alles low zetten
except KeyboardInterrupt:
    GPIO.output(rs, GPIO.LOW)
    GPIO.output(rw, GPIO.LOW)
    GPIO.output(e, GPIO.LOW)
    GPIO.output(d4, GPIO.LOW)
    GPIO.output(d5, GPIO.LOW)
    GPIO.output(d6, GPIO.LOW)
    GPIO.output(d7, GPIO.LOW)
    print("KeyboardInterrupt")

print("einde")
GPIO.cleanup()
