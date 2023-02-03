import json

dictionary = {
    "some text": "more text",
    "int": 0,
    "float": 1.1,
    "none": None
}
dict_str = json.dumps(dictionary)
print("Dictionary: ", dictionary)
print("Json dumps: ", dict_str)
str_dict = str(dictionary)
print("Dict to str: ", str_dict)
print("ITs type: ", type(str_dict))
