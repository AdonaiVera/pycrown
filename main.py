import threading
from modules.read_waves import NeurosityReader


import time

threshold = 0.8

def main():
    reader = NeurosityReader()
    reader.start()

    try:
        while True:
            # Main thread could still perform other tasks or just stay idle
            pass
    except KeyboardInterrupt:
        reader.stop()
        print("Application stopped.")

if __name__ == "__main__":
    main()

