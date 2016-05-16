import serial
import sys
import time
from datetime import datetime

def get_serial(baudrate=9600, read_timeout=1.5, board_reset_timeout=2,
               find_port_timeout=0.5):
    ports = []
    for i in range(5):
        ports.append('/dev/ttyACM{}'.format(i))
        ports.append('/dev/ttyUSB{}'.format(i))
    i = 0
    while True:
        serial_port = ports[i]
        try:
            ser = serial.Serial(port=serial_port,
                                baudrate=baudrate,
                                timeout=read_timeout,
                                xonxoff=True)
            time.sleep(board_reset_timeout)
            return ser
        except Exception as e:
            print("Exception: {}".format(e))

            if i < len(ports) - 1:
                i += 1
            else:
                i = 0
            time.sleep(find_port_timeout)

def send(command_str, response_wait=0):
    '''
    Send the string 'command_str' to the serial port and return the response.
    '''
    ser.write(bytes(command_str, encoding='utf-8'))
    # time.sleep(response_wait)
    try:
        raw = ser.readall()
        return raw.decode('ascii').strip()
    except:
        print("Unable to decode raw response to ASCII:\n{}".format(raw))


def sync_rtc():
    '''
    Synchronizes the board clock with the system's.
    '''
    dt = datetime.now()
    print('\nCurrent system time:', dt.isoformat().replace('T', ' '))
    print("\nAttempting serial connection ...", end='')
    ser = get_serial()
    print('got it!')
    print(ser)
    ser.flush()

    command = 'setrtc,{Y},{m},{d},{H},{M},{S}'.format(
        Y=dt.year, m=dt.month, d=dt.day, H=dt.hour, M=dt.minute, S=dt.second)

    print('\nSending serial command:\n    "{}"\n'.format(command))

    ser.write(bytes(command, encoding='utf-8'))
    try:
        raw = ser.readall()
        return raw.decode('ascii').strip()
    except:
        print("Unable to decode raw response to ASCII:\n{}".format(raw))


def loop_serial():
    print(
    """\
    Examples:

        > read,t,l                      # for reading temp. and lum.
        > setrtc,2015,7,15,17,45,0      # for setting RTC datetime

    Hit Ctrl+C to exit!""")
    print('-'*40 + '\n')
    try:
        while True:
            print(send(input('> ')))
    except:
        pass


print("\nAttempting serial connection ...\n")
ser = get_serial()
print(ser)
ser.flush()

print("\nSent 'help'... waiting for board response ...")
response = send('help')
print("\nBoard commands:\n" + '-'*40 + '\n' + response + '\n' + '-'*40)
print('-'*40 + '\n')

if '-c' in sys.argv and len(sys.argv) == 3:
    print(send(input('> ')))
elif '--loop' in sys.argv:
    loop_serial()
elif '--syncrtc' in sys.argv:
    print(sync_rtc())
