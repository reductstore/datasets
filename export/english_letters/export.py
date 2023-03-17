import os
from pathlib import Path
from typing import List

from reduct import Client, Bucket, ReductError

REDUCT_STORE_HOST = "https://play.reduct.store"
REDUCT_STORE_API_TOKEN = os.getenv("REDUCT_STORE_API_TOKEN")
REDUCT_STORE_BACKET = "datasets"
REDUCT_STORE_ENTRY = "english_letters"

DATA_SET_PATH = os.getenv("DATA_SET_PATH")

dataset = set()

DIGIT = 1
HIGHER_CASE = 11
LOWER_CASE = 37


async def write_folder(file, bucket: Bucket):
    """"""
    file = str(file)
    entry_name = "english_letters_mask" if "Msk" in file else "english_letters_bmp"

    labels = {}
    labels["quality"] = "good" if "GoodImg" in file else "bad"

    with open(file, "rb") as f:
        image = f.read()

    labels["source"] = Path(file).name
    code = int(Path(file).name[3:6])
    if DIGIT <= code < HIGHER_CASE:
        labels["symbol"] = chr(code - DIGIT + 0x30)
        labels["type"] = "digit"
    if HIGHER_CASE <= code < LOWER_CASE:
        labels["symbol"] = chr(code - HIGHER_CASE + 0x41)
        labels["type"] = "higher_case"
    if LOWER_CASE <= code:
        labels["symbol"] = chr(code - LOWER_CASE + 0x61)
        labels["type"] = "lower_case"

    print(f"Uploading {file}: {labels}")
    str_id = Path(file).name[3:-4].replace("-", "")
    if labels["quality"] == "good":
        str_id = "1" + str_id
    await bucket.write(entry_name, timestamp=int(str_id), data=image, labels=labels,
                       content_type=f"image/{file.split('.')[-1]}")


async def main():
    client = Client(REDUCT_STORE_HOST, api_token=REDUCT_STORE_API_TOKEN)
    bucket = await client.get_bucket(REDUCT_STORE_BACKET)

    all_files = []
    for path, _, files in os.walk(DATA_SET_PATH):
        path = Path(path)

        if len(files) > 0:
            all_files += [path / file for file in files]

    for file in sorted(all_files):
        await write_folder(file, bucket)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
