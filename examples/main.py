from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

from examples.models import PostContractJSONSchema, PostContractBodySchema
from examples.models import PostContractSmallDoubleBodySchema
from pyfa_converter import FormBody

app = FastAPI()


@app.post("/json-body")
async def example_json_body_handler(
    data: PostContractJSONSchema,
):
    return {
        "title": data.title,
        "date": data.date,
    }


@app.post("/form-data-body")
async def example_foo_body_handler(
    data: PostContractBodySchema = FormBody(PostContractBodySchema),
    document: UploadFile = File(...),
):
    return {
        "title": data.title,
        "date": data.date,
        "file_name": document.filename
    }


@app.post("/form-data-body-two")
async def example_foo_body_handler(
    data: PostContractBodySchema = FormBody(PostContractBodySchema),
    document: UploadFile = File(...),
):
    return {
        "title": data.title,
        "date": data.date,
        "file_name": document.filename
    }


@app.post("/test")
async def foo(
    data: PostContractSmallDoubleBodySchema = FormBody(PostContractSmallDoubleBodySchema),
):
    return {'bar': 'bar'}
