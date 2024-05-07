from neurosity import NeurositySDK
from config import NEUROSITY_DEVICE_ID, NEUROSITY_EMAIL, NEUROSITY_PASSWORD
import os
import time


device_id = os.getenv("NEUROSITY_DEVICE_ID")
neurosity = NeurositySDK({
    "device_id": NEUROSITY_DEVICE_ID
})

neurosity.login({
    "email": NEUROSITY_EMAIL,
    "password": NEUROSITY_PASSWORD
})

info = neurosity.get_info()

def callback(data):
    pass

unsubscribe = neurosity.kinesis_predictions("push", callback)

time.sleep(20)
unsubscribe()
print("Done with Kinesis example.py")