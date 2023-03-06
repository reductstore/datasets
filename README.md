A collection of free datasets hosted with [ReductStore](https://reduct.store/).

The goal of this repository is to provide a collection of free datasets that can be used for testing and benchmarking machine learning algorithms.
All datasets are hosted on [ReductStore](https://play.reduct.store/) and can be downloaded using [Reduct CLI](https://https://github.com/reductstore/reduct-cli) or
one of the client libraries:


* [Python Client SDK](https://github.com/reductstore/reduct-py)
* [JavaScript Client SDK](https://github.com/reductstore/reduct-js)
* [C++ Client SDK](https://github.com/reductstore/reduct-cpp)


Credentials to obtain the datasets:

Host: https://play.reduct.store
Bucket: datasets
API Token: dataset-read-93e70946830cc0b8ddd402a3c8025b2fbbd46abebcc59079f148bad574a05bc1


## Export data with Reduct CLI

You can export datasets to your local machine using Reduct CLI:

```bash
pip install -U readuct-cli
rcl alias add play -L https://play.reduct.store -t dataset-read-93e70946830cc0b8ddd402a3c8025b2fbbd46abebcc59079f148bad574a05bc1
rcl export folder play/datasets/ --entries=<Dataset Name>
```

## Export data with Python Client SDK

You can integrate ReductStore into your Python code and use the datasets directly:

```python
import asyncio
from reduct import Client

HOST="https://play.reduct.store"
API_TOKEN="dataset-read-93e70946830cc0b8ddd402a3c8025b2fbbd46abebcc59079f148bad574a05bc1"

async def main():
    client = Client(HOST, API_TOKEN)
    bucket = await client.get_bucket("datasets")
    async for record in bucket.query("cats"):
        print(record.labels)
        jpg = await record.read_all()

if __name__ == "__main__":
    asyncio.run(main())
```


## Datasets

| Entry Name | Description                                              | Data Type | Labels                                                                                                                                                                                                                            | Original Source                                      | Export Script                       |
|------------|----------------------------------------------------------|-----------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|------------------------------------------------------|-------------------------------------|
| cats       | Over 9,000 images of cats with annotated facial features | jpeg      | l,left-eye-x,left-eye-y,right-eye-x,right-eye-y,mouth-x,mouth-y,left-ear-1-x,left-ear-1-y,left-ear-2-x,left-ear-2-y,left-ear-3-x,left-ear-3-y,right-ear-1-x,right-ear-1-y,right-ear-2-x,right-ear-2-y,right-ear-3-x,right-ear-3-y | https://www.kaggle.com/datasets/crawford/cat-dataset | [export.py](.export/cats/export.py) |
