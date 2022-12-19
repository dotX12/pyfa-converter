from fastapi import FastAPI, Header
from fastapi import File
from fastapi import UploadFile

from examples.models import (
    PostContractBodySchema,
    ExampleSchemaForHeader,
)
from examples.models import PostContractJSONSchema
from examples.models import PostContractSmallDoubleBodySchema
from examples.models import PostContractSmallDoubleQuerySchema
from examples.models import PostSchemaIntegerGE
from pyfa_converter.depends import QueryDepends, FormDepends, PyFaDepends

app = FastAPI()


@app.post("/json-body")
async def example_json_body_handler(
    data: PostContractJSONSchema,
):
    return {
        "title": data.title,
        "date": data.date,
    }


#


@app.post("/form-data-body")
async def example_foo_body_handler(
    data: PostContractBodySchema = FormDepends(PostContractBodySchema),
    document: UploadFile = File(...),
):
    return {"title": data.title, "date": data.date, "file_name": document.filename}


@app.post("/form-data-body-two")
async def example_foo_body_handler(
    data: PostContractBodySchema = FormDepends(PostContractBodySchema),
    document: UploadFile = File(...),
):
    return {"title": data.title, "date": data.date, "file_name": document.filename}


@app.post("/test")
async def foo(
    data: PostContractSmallDoubleBodySchema = FormDepends(
        PostContractSmallDoubleBodySchema
    ),
):
    return {"data": data}


@app.post("/test_query_list")
async def test_list_form(
    data: PostContractSmallDoubleQuerySchema = QueryDepends(
        PostContractSmallDoubleQuerySchema
    ),
):
    return {"data": data}


@app.post("/test_header_list")
async def test_list_form(
    data: ExampleSchemaForHeader = PyFaDepends(
        model=ExampleSchemaForHeader, _type=Header
    ),
):

    return {"data": data}


@app.post("/test_int_ge")
async def test_post_int_ge(
    data: PostSchemaIntegerGE = FormDepends(PostSchemaIntegerGE),
):
    return {"id": data.id}
