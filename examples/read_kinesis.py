from neurosity import NeurositySDK
from dotenv import load_dotenv
import os
import time

load_dotenv("my.env")

device_id = os.getenv("NEUROSITY_DEVICE_ID")
neurosity = NeurositySDK({
    "device_id": device_id
})

neurosity.login({
    "email": os.getenv("NEUROSITY_EMAIL"),
    "password": os.getenv("NEUROSITY_PASSWORD")
})

info = neurosity.get_info()

def callback(data):
    print(data)

unsubscribe = neurosity.kinesis("leftArm", callback)

time.sleep(20)
unsubscribe()
print("Done with Kinesis example.py")