from hcsr04sensor import sensor

# Created by Al Audet
# MIT License

def main():
    '''Calculate the distance of an object in centimeters using a HCSR04 sensor
       and a Raspberry Pi'''

    trig_pin1 = 18
    echo_pin1 = 23
    trig_pin2 = 24
    echo_pin2 = 17
    # Default values
    # unit = 'metric'
    # temperature = 20
    # round_to = 1

    #  Create a distance reading with the hcsr04 sensor module
    value1 = sensor.Measurement(trig_pin1, echo_pin1)
    raw_measurement1 = value1.raw_distance()

    value2 = sensor.Measurement(trig_pin2, echo_pin2)
    raw_measurement2 = value2.raw_distance()

    # To overide default values you can pass the following to value
    # value = sensor.Measurement(trig_pin,
    #                            echo_pin,
    #                            temperature=10,
    #                            round_to=2
    #                            )


    # Calculate the distance in centimeters
    metric_distance1 = value1.distance_metric(raw_measurement1)
    print("Afstand sensor 1 = {} centimeters".format(metric_distance1))

    metric_distance2 = value2.distance_metric(raw_measurement2)
    print("Afstand sensor 2 = {} centimeters".format(metric_distance2))

if __name__ == "__main__":
    main()