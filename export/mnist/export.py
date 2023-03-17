from time import time_ns
import asyncio
import os
from time import time_ns

from reduct import Client, BucketSettings, QuotaType

REDUCT_STORE_HOST = "https://play.reduct.store"
REDUCT_STORE_API_TOKEN = os.getenv("REDUCT_STORE_API_TOKEN")
REDUCT_STORE_BACKET = "datasets"
REDUCT_STORE_ENTRY = "mnist_"

DATA_SET_PATH = os.getenv("DATA_SET_PATH")


async def main():
    client = Client(REDUCT_STORE_HOST, api_token=REDUCT_STORE_API_TOKEN)
    bucket = await client.get_bucket(REDUCT_STORE_BACKET)
    path = DATA_SET_PATH
    for foldername in os.listdir(path):
        dataset_name = foldername
        counter = 0
        folder_path = os.path.join(path, dataset_name)
        for digit in os.listdir(folder_path):
            label_path = os.path.join(folder_path, digit)
            for i in os.listdir(label_path):
                img_path = os.path.join(label_path, i)
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                labels = {
                    "digit": digit,
                }

                counter += 1
                await bucket.write(REDUCT_STORE_ENTRY + dataset_name, img_data, timestamp=counter, labels=labels,
                                   content_type="image/png")


if __name__ == "__main__":
    asyncio.run(main())
