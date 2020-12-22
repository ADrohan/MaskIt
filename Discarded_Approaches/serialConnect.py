
import serial

if __name__ == '__main__':
    #ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser = serial.Serial('/dev/ttyACM0', 115200, timeout=1)
    ser.flush()
    while True:
        number = ser.read()
        if number != b'':
            if int.from_bytes(number, byteorder='big') == 1:
                led_number = 1 
                print("Motion detected.")
                print("Sending number " + str(led_number) + " to Arduino.")
                ser.write(str(led_number).encode('utf-8'))
