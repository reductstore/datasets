import os
import scipy.io
import asyncio
import time
from utils.meta_data_parser import mat_to_dict
from reduct import Client, Bucket

REDUCT_STORE_HOST = "http://localhost:8383"
REDUCT_STORE_API_TOKEN = os.getenv("REDUCT_STORE_API_TOKEN")
REDUCT_STORE_BACKET = "datasets"
REDUCT_STORE_ENTRY = "imdb_"

DATA_SET_PATH = os.getenv('DATA_SET_PATH')     # add path to imdb folder (this contains sub folders, eg:00, 01)
META_DATA_PATH = os.getenv('META_DATA_PATH')

meta_data = scipy.io.loadmat('META_DATA_PATH', simplify_cells=True)  # add the full path to .mat file
meta_data_dict = mat_to_dict(meta_data['imdb'])


async def main():
    client = Client(REDUCT_STORE_HOST, api_token=REDUCT_STORE_API_TOKEN)
    bucket = await client.get_bucket(REDUCT_STORE_BACKET)
    path = DATA_SET_PATH
    for foldername in os.listdir(path):
        dataset_name = foldername
        counter = 0
        folder_path = os.path.join(path, dataset_name)
        for image in os.listdir(folder_path):
            img_path = os.path.join(folder_path, image)
            if meta_data_dict[image]:
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                    label = meta_data_dict[image]
                    counter += 1
                    await bucket.write(REDUCT_STORE_ENTRY + dataset_name, img_data, timestamp=counter, labels=label,
                                       content_type="image/jpg")

if __name__ == "__main__":
    asyncio.run(main())