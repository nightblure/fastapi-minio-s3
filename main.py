import io

import uvicorn
from fastapi import FastAPI
from minio import Minio
from starlette.responses import Response

app = FastAPI()

"""на порту 9001 доступен удобный GUI для просмотра хранилища"""


class S3Client:
    def __init__(self):
        self.client = Minio(
            endpoint='localhost:9000',
            access_key='U4B6Zib75DXSPmavZb',
            secret_key='Q4#QP4dudUobU#NBcGB7RMKV4ajYb',
            secure=False
        )


s3client = S3Client()


def recreate_bucket():
    objs = s3client.client.list_objects('pic-bucket')

    for obj in objs:
        s3client.client.remove_object('pic-bucket', obj.object_name)

    s3client.client.remove_bucket('pic-bucket')

    buckets = s3client.client.list_buckets()

    if len(buckets) == 0:
        s3client.client.make_bucket('pic-bucket')
        print('bucket created')


@app.get('/picture/{name}')
def get_picture(name: str):
    obj = s3client.client.get_object('pic-bucket', name + '.jpg')
    image_bytes = obj.read()
    return Response(content=image_bytes, media_type="image/png")


@app.delete('/picture/{name}')
def delete_picture(name: str):
    s3client.client.remove_object('pic-bucket', name + '.jpg')
    return {'detail': 'ok'}


@app.post('/picture/{name}')
def load_picture(name: str):
    path = '/Users/ivan/Downloads/background for BANDCAMP.jpg'

    with open(path, 'rb') as f:
        value_as_bytes = f.read()

    value_as_a_stream = io.BytesIO(value_as_bytes)

    s3client.client.put_object('pic-bucket', f'{name}.jpg', value_as_a_stream, len(value_as_bytes))
    return {'detail': 'ok'}


if __name__ == '__main__':
    recreate_bucket()
    uvicorn.run(app, host='0.0.0.0', port=8093)
