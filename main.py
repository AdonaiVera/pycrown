# Import the NeurosityReader class from the modules.read_waves module
from modules.read_waves import NeurosityReader

def main():
    # Create an instance of NeurosityReader
    reader = NeurosityReader()
    
    # Start the reader to begin processing EEG data
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

