from gpiozero import PumpkinPi
from gpiozero.pins.mock import MockFactory
import socket as sock
import subprocess as sp

# Common error messages specific to sockets.
err_msg_timeout = 'Connection Error:\tConnection timeout error occurred with client at \'{0}\' on port {1:d}.'

# Parse the command line for address info.
import sys

argv = sys.argv

if '-h' in argv:
    HOST = argv[argv.index('-h') + 1]
elif '--host' in argv:
    HOST = argv[argv.index('--host') + 1]
else:
    HOST = '127.0.0.1'

if '-p' in argv:
    PORT = int(argv[argv.index('-p') + 1])
elif '--port' in argv:
    PORT = int(argv[argv.index('--port') + 1])
else:
    PORT = 9001

ADDR = (HOST, PORT)

# Create server socket bound to HOST listening on port PORT.
ss = sock.socket()
ss.bind(ADDR)
ss.listen(1)

# Instantiate PumpkinPi class.
pumpkin = PumpkinPi()

while True:
    # Accept incoming connection by listening on port 9001.
    try:
        s, addr = ss.accept()
    except KeyboardInterrupt:
        print('\nServer was stopped by a keyboard interrupt before a connection was accepted.')
        exit(0)

    sock.setdefaulttimeout(2)

    # Wait for a command to be sent.
    try:
        msg_r = s.recv(1024)
    except sock.timeout:
        print(err_msg_timeout.format(*addr))
        exit(1)

    # Decode the message to a string, denoted as 'cmd'.
    cmd = msg_r.decode(encoding='utf-8')
    
    # Parse and execute the command ('cmd').
    C = cmd.split('.')
    if C[0] == 'sides':
        if C[1] == 'left':
            pumpkin.sides.left[int(C[2])].toggle()  # type: ignore[attr-defined]
        else:
            pumpkin.sides.right[int(C[2])].toggle()  # type: ignore[attr-defined]
    elif C[0] == 'blink':
        if len(C) > 1:
            if isinstance(pumpkin.pin_factory, MockFactory):
                print("PumpkinPi is blinking...")
            pumpkin.eyes.blink(n=5, background=False)  # type: ignore[attr-defined]
            if isinstance(pumpkin.pin_factory, MockFactory):
                print("PumpkinPi is done blinking.")
        else:
            if isinstance(pumpkin.pin_factory, MockFactory):
                print("PumpkinPi is blinking...")
            pumpkin.blink(n=5, background=False)  # type: ignore[attr-defined]
            if isinstance(pumpkin.pin_factory, MockFactory):
                print("PumpkinPi is done blinking.")
    elif C[0] == 'cycle':
        sp.run(['python3', 'cycle.py'])
    else:
        pumpkin.eyes.left.toggle() if C[1] == 'left' else pumpkin.eyes.right.toggle()  # type: ignore[attr-defined]

    """If the pin factory is a MockFactory, which can be achieved through setting the environment variable, 'GPIOZERO_PIN_FACTORY', to 'mock',
     then we must print out the outcome of the command that was just executed during this loop iteration."""

    if isinstance(pumpkin.pin_factory, MockFactory):
        print(cmd + " was just toggled.")

    # Close and disconnect the client socket in preparation for a new iteration and subsequently a new client.
    s.close()

