import sys

import serial


def send_arduino_message(serial_identifier: str, message: str):
    serial_connection = serial.Serial(serial_identifier, baudrate=9600, timeout=0.001)
    encoded_message = message.encode('ascii')
    serial_connection.write(encoded_message)
    response_part = serial_connection.readline().decode('ascii')
    response = response_part
    response_part = serial_connection.readline().decode('ascii')
    while response_part != '':
        response += response_part
        response_part = serial_connection.readline().decode('ascii')
    print(response)
    sys.stdout.flush()
    if 'Error' in response:
        raise RuntimeError('Can\'t trigger arduino:\n' + response)
