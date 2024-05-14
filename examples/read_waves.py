from neurosity import NeurositySDK
from config import NEUROSITY_DEVICE_ID, NEUROSITY_EMAIL, NEUROSITY_PASSWORD
import os
import time


neurosity = NeurositySDK({"device_id": NEUROSITY_DEVICE_ID})
neurosity.login({"email": NEUROSITY_EMAIL, "password": NEUROSITY_PASSWORD})
        
info = neurosity.get_info()
print(info)

def callback(data):
    print(data)

unsubscribe = neurosity.brainwaves_raw(callback)
time.sleep(50)
unsubscribe()
print("Done with read_waves.py")