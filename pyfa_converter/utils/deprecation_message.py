DEPRECATION_MESSAGE = (
    "This decorator is deprecated.\n"
    "The decorator above the model is no longer required and will be removed in the next version!\n"
    "Use:\n"
    "data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Header)\n"
    "data: MyCustomModel = PyFaDepends(MyCustomModel, _type=Form)\n"
    "or\n\n"
    "data: MyCustomModel = FormDepends(MyCustomModel)\n"
    "data: MyCustomModel = QueryDepends(MyCustomModel)"
)
