# pyfa-converter
Allows you to convert pydantic models for fastapi param models - query, form, header, cookie, body, etc.



### How to install?
`pip install pyfa_converter`

### How to simplify your life?
```python3
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, UploadFile, File, Form
from pydantic import BaseModel, Field

from pyfa_converter import FormDepends, PyFaDepends

app = FastAPI()


class PostContractBodySchema(BaseModel):
    title: str = Field(..., description="Description title")
    date: Optional[datetime] = Field(
        None, description="Example: 2021-12-14T09:56:31.056Z"
    )


@app.post("/form-data-body")
async def example_foo_body_handler(
    data1: PostContractBodySchema = PyFaDepends(model=PostContractBodySchema, _type=Form),
    document: UploadFile = File(...),
):
    return {"title": data.title, "date": data.date, "file_name": document.filename}
```

---

### What do I need to do?
```python3
from pyfa_converter import PyFaDepends, FormDepends, QueryDepends
from fastapi import Header, Form
...

async def foo(data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Header)): ...
async def foo(data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Form)): ...

async def foo(data: MyCustomModel = FormDepends(MyCustomModel)): ...
async def foo(data: MyCustomModel = QueryDepends(MyCustomModel)): ...
```

---

If you want to accept a file on an endpoint, then the content-type for that endpoint changes from application/json to www-form-data.

FastAPI does not know how to override the pydantic schema so that parameters are passed as form.
Even if you do

`foo: CustomPydanticModel = Depends()`
all model attributes will be passed as query, but we want them to become body, that's what this library exists for.

### Usually you use something along the lines of:
![image](https://user-images.githubusercontent.com/64792903/161484700-642e3d0e-242f-49f6-82e8-45c5e912a2c2.png)

But, if we accept a lot of fields, then the function becomes very large (the number of attributes for the endpoint increases and it does not look very good).

Thanks to this library, it is possible to force the conversion of Field fields into fields of FastAPI Form with full preservation of all attributes (alias, gt, te, description, title, example and more...)


