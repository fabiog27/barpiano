import sys

import serial


def send_arduino_message(serial_identifier: str, message: str):
    serial_connection = serial.Serial(serial_identifier, baudrate=9600, timeout=0.001)
    encoded_message = message.encode('ascii')
    serial_connection.write(encoded_message)
