import os
import scipy.io
import asyncio
import time
from meta_data_parser import mat_to_dict
from reduct import Client, Bucket, ReductError

REDUCT_STORE_HOST = "https://play.reduct.store"
REDUCT_STORE_API_TOKEN = os.getenv("REDUCT_STORE_API_TOKEN")
REDUCT_STORE_BACKET = "datasets"
REDUCT_STORE_ENTRY = "imdb"

DATA_SET_PATH = os.getenv('DATA_SET_PATH')  # add path to imdb folder (this contains sub folders, eg:00, 01)
META_DATA_PATH = os.getenv('META_DATA_PATH')

meta_data = scipy.io.loadmat(META_DATA_PATH, simplify_cells=True)  # add the full path to .mat file
meta_data_dict = mat_to_dict(meta_data['imdb'])

START_ID = 0 # change this to the last id that was uploaded (if you want to continue from where you left off)
async def main():
    client = Client(REDUCT_STORE_HOST, api_token=REDUCT_STORE_API_TOKEN, timeout=60)
    bucket = await client.get_bucket(REDUCT_STORE_BACKET)
    path = DATA_SET_PATH
    counter = 0
    for foldername in sorted(os.listdir(path)):
        dataset_name = foldername
        folder_path = os.path.join(path, dataset_name)
        for image in sorted(os.listdir(folder_path)):
            img_path = os.path.join(folder_path, image)
            if meta_data_dict[image]:
                with open(img_path, 'rb') as f:
                    img_data = f.read()
                    label = meta_data_dict[image]
                    label['face_location_x'] = label['face_location'][0]
                    label['face_location_y'] = label['face_location'][1]
                    label['face_location_w'] = label['face_location'][2]
                    label['face_location_h'] = label['face_location'][3]
                    label.pop('face_location')

                    label['name'] = str(label['name']).encode('utf-8')

                    counter += 1
                    if counter < START_ID:
                        continue

                    print(f"Uploading {image} to {REDUCT_STORE_BACKET}/{REDUCT_STORE_ENTRY} id={counter}...")
                    try:
                        await bucket.write(REDUCT_STORE_ENTRY, img_data, timestamp=counter, labels=label,
                                           content_type="image/jpeg")
                    except ReductError as err:
                        if err.status_code == 409:
                            print(f"Image id={counter} already exists. Skipping.")
                        else:
                            raise err


if __name__ == "__main__":
    asyncio.run(main())
