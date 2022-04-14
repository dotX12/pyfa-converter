# pyfa-converter
Makes it pretty easy to create a model based on Field [pydantic] and use the model for www-form-data.


### How to install?
`pip install pyfa_converter`

### How to simplify your life?
![image](https://user-images.githubusercontent.com/64792903/161491444-60e211fe-26c3-44ea-aade-a7c4177eaa74.png)

---

### What do I need to do with the model?
* We put the decorator `@PydanticConverter.body` for the model and enjoy.
* `data: YourPydanticModel = FormBody()`

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


