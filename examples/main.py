from fastapi import Depends
from fastapi import FastAPI
from fastapi import File
from fastapi import UploadFile

from examples.models import PostContractJSONSchema, PostContractBodySchema

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
    data: PostContractBodySchema = Depends(PostContractBodySchema.body),
    document: UploadFile = File(...),
):
    return {
        "title": data.title,
        "date": data.date,
        "file_name": document.filename
    }
