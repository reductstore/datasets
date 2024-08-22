# Collection of free datasets hosted with [ReductStore](https://reduct.store/).

The goal of this repository is to provide a collection of free datasets that can be used for testing and benchmarking
machine learning algorithms.

All datasets are hosted on [ReductStore](https://play.reduct.store/) and can be downloaded
using [Reduct CLI](https://https://github.com/reductstore/reduct-cli) or
one of the client libraries:

* [Python Client SDK](https://github.com/reductstore/reduct-py)
* [Rust Client SDK](https://github.com/reductstore/reduct-rs)
* [JavaScript Client SDK](https://github.com/reductstore/reduct-js)
* [C++ Client SDK](https://github.com/reductstore/reduct-cpp)

## Why ReductStore?

Inspite of the fact that ReductStore is a time series database, we use it to store datasets as a collection of records
and use timestamp is a unique identifier. This approcah have the following advantages:

- The database is fast and free, you can mirror datasets on your own instance and use them locally.
- You can download partial datasets
- You can use databases directly from Python, Rust, C++, or Node.js
- You can use annotations as a dictionary of labels, no need to parse them manually.

## Examples

Credentials to obtain the datasets:

- Host: https://play.reduct.store
- Bucket: datasets
- API Token: reductstore

### Export data with Reduct CLI

You can export datasets to your local machine using Reduct CLI:

```bash
# Install the tool
wget https://github.com/reductstore/reduct-cli/releases/latest/download/reduct-cli.linux-amd64.tar.gz
tar -xvf reduct-cli.linux-amd64.tar.gz
chmod +x reduct-cli
sudo mv reduct-cli /usr/local/bin
# Add the ReductStore instance to aliases
reduct-cli alias add play -L https://play.reduct.store -t reductstore
# Download dataset(s) specified in --entry. Each sample will have a JSON document with metadata and anotations.
reduct-cli cp play/datasets . --entries=<Dataset Name> --with-metadata
```

### Export data with Python Client SDK

You can integrate ReductStore into your Python code and use the datasets directly:

```python
import asyncio
from reduct import Client

HOST = "https://play.reduct.store"
API_TOKEN = "reductstore"
DATASET = "cats"


async def main():
    client = Client(HOST, API_TOKEN)
    bucket = await client.get_bucket("datasets")
    async for record in bucket.query(DATASET):
        print(record.labels)
        jpeg = await record.read_all()
        # Do something with the JPEG image


if __name__ == "__main__":
    asyncio.run(main())
```

## Datasets

| Entry Name                  | Description                                                 | Data Type | Labels                                                                                                                                                                                                                          | Original Source                                                          | Export Script                                 |
|-----------------------------|-------------------------------------------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------|-----------------------------------------------|
| cats                        | Over 9,000 images of cats with annotated facial features    | jpeg      | left-eye-x,left-eye-y,right-eye-x,right-eye-y,mouth-x,mouth-y,left-ear-1-x,left-ear-1-y,left-ear-2-x,left-ear-2-y,left-ear-3-x,left-ear-3-y,right-ear-1-x,right-ear-1-y,right-ear-2-x,right-ear-2-y,right-ear-3-x,right-ear-3-y | [kaggle](https://www.kaggle.com/datasets/crawford/cat-dataset)           | [export.py](export/cats/export.py)            |
|  mnist_training, mnist_test | MNIST handwritten digits                                    | png       | digit                                                                                                                                                                                                                           | [MNIST](http://yann.lecun.com/exdb/mnist/)                               | [export.py](export/mnist/export.py)           | 
| imdb                        | ~50,000 photos from IMBD with face location, age and gender | jpeg      | dob,photo_taken,gender,name,face_location_{x,y,w,h},face_score,second_face_score,celeb_names,celeb_id                                                                                                                           | [IMDB-WIKI](https://data.vision.ee.ethz.ch/cvl/rrothe/imdb-wiki/)        | [export.py](export/imdb/export.py)            |

## Examples

* [How to Use "Cats" dataset with Python Reduct SDK](./examples/cats.ipynb)
