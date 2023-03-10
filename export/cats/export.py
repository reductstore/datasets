import os
from pathlib import Path
from typing import List

from reduct import Client, Bucket, ReductError

REDUCT_STORE_HOST = "https://play.reduct.store"
REDUCT_STORE_API_TOKEN = os.getenv("REDUCT_STORE_API_TOKEN")
REDUCT_STORE_BACKET = "datasets"
REDUCT_STORE_ENTRY = "cats"

DATA_SET_PATH = os.getenv("DATA_SET_PATH")

count = 0
dataset = set()


async def write_folder(path: Path, files: List[str], bucket: Bucket):
    global count
    global dataset

    meta = {}
    for file in sorted(files):
        if file.endswith(".jpg"):
            meta.setdefault(file[:-4], {}).update({"image": path / file})
        if file.endswith(".jpg.cat"):
            with open(path / file) as f:
                metrics = f.read().split(" ")
                labels = {
                    "left-eye-x": metrics[1],
                    "left-eye-y": metrics[2],
                    "right-eye-x": metrics[3],
                    "right-eye-y": metrics[4],
                    "mouth-x": metrics[5],
                    "mouth-y": metrics[6],
                    "left-ear-1-x": metrics[7],
                    "left-ear-1-y": metrics[8],
                    "left-ear-2-x": metrics[9],
                    "left-ear-2-y": metrics[10],
                    "left-ear-3-x": metrics[11],
                    "left-ear-3-y": metrics[12],
                    "right-ear-1-x": metrics[13],
                    "right-ear-1-y": metrics[14],
                    "right-ear-2-x": metrics[15],
                    "right-ear-2-y": metrics[16],
                    "right-ear-3-x": metrics[17],
                    "right-ear-3-y": metrics[18],
                }
            meta.setdefault(file[:-8], {}).update({"labels": labels})

    for source, value in meta.items():
        count += 1
        if source in dataset:
            print(f"Skipping {source} (already exists)")
            continue

        dataset.add(source)

        print(f"Uploading {source}: {value}")
        value["labels"].update({"source": source})

        with open(value["image"], "rb") as f:
            try:
                await bucket.write(
                    REDUCT_STORE_ENTRY,
                    f.read(),
                    timestamp=count,
                    labels=value["labels"],
                    content_type="image/jpeg",
                )
            except ReductError as err:
                if err.status_code == 409:
                    print(f"Entry {source} already exists")
                else:
                    raise err


async def main():
    client = Client(REDUCT_STORE_HOST, api_token=REDUCT_STORE_API_TOKEN)
    bucket = await client.get_bucket(REDUCT_STORE_BACKET)
    for path, _, files in os.walk(DATA_SET_PATH):
        path = Path(path)
        await write_folder(path, files, bucket)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
