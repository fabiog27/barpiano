import serial


def send_arduino_message(serial_connection: serial.Serial, message: str):
    encoded_message = message.encode('ascii')
    serial_connection.write(encoded_message)
