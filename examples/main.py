from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

from examples.models import PostContractJSONSchema, PostContractBodySchema
from pyfa_converter.depends import FormBody

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
    data: PostContractBodySchema = FormBody(),
    document: UploadFile = File(...),
):
    return {
        "title": data.title,
        "date": data.date,
        "file_name": document.filename
    }
