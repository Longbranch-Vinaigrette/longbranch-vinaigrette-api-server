import json


def convert_to_python_dict(data: list, description: tuple, debug: bool = False) -> dict:
    """Convert a query to python dict

    Where data is the actual data, and description is the output
    from calling cursor.description"""
    if debug:
        print("\nsqlite_parser -> convert_to_python_dict():")

    # Description looks like this(these are the keys)
    # Columns(description): (('username', None, None, None, None, None, None),)

    # Data looks like this
    # Data: [('asdf',)]
    # Also data could be a json string:
    # Data: [('{key:username,value:joe}',)]

    result = {}

    if not data:
        return {}

    # Parse data
    if len(data) <= 1:
        i = 0
        for key_tuple in description:
            key = key_tuple[0]

            # The actual data
            value = data[0][i]

            # Insert into the dictionary
            result[key] = value

            i += 1
    else:
        result = []
        for i in range(len(data)):

            j = 0
            new_dict = {}
            for key_tuple in description:
                key = key_tuple[0]

                # The actual data
                value = data[i][j]

                # Insert into the dictionary
                new_dict[key] = value

                j += 1
            result.append(new_dict)

    return result


def convert_to_sql_value(val, debug: bool = False):
    """Parse unique key val"""
    if debug:
        print("\nsqlite_parser -> convert_to_sql_value():")
    if isinstance(val, str):
        # This is for escaping the '
        val = val.replace("'", "''")

        formatted_val = "\'{0}\'".format(val)
        return formatted_val
    if type(val) == type(1):
        return val
    if isinstance(val, float):
        return val

    # The rest doesn't exist in sql, so parse it to text with json
    if isinstance(val, list):
        val = {
            "___forced_value": True,
            "type": "list",
            "value": val,
        }
    if isinstance(val, dict):
        val = {
            "___forced_value": True,
            "type": "dict",
            "value": val,
        }
    if isinstance(val, bool):
        val = {
            "___forced_value": True,
            "type": "bool",
            "value": val,
        }
    if type(val) == type(None):
        val = {
            "___forced_value": True,
            "type": "none",
            "value": None,
        }

    val = '\'' + json.dumps(val) + '\''
    return val


def parse_sql_data_type(variable, null_as_text=False, debug: bool = False):
    """Get the data type as a SQLite3 data type

    Idk what da hell is blob
    Returns a string representing the type
    If the type is unknown it will return "null\""""
    if debug:
       print("\nsqlite_parser -> parse_sql_data_type():")

    if type(variable) == type(1):
        return "integer"
    if isinstance(variable, float):
        return "real"
    if isinstance(variable, str) or null_as_text:
        return "text"

    return "null"


def parse_sql(data, mode="createTableKeys", separator=", ", update_columns=[], debug: bool = False):
    """Get comma separated types or values from dictionary arrays

    Args:
    mode:
        Course of action:
        Mode types:
        createTableKeys:        keywords += key + " " + data_type + ", "
        commaSeparatedKeys:     keywords += key + ", "
        commaSeparatedValues:   keywords += value + ", "
    update_columns:
        An array of strings that contain the name of the columns to be updated
    """
    if debug:
        print("\nSqlite3Utils -> parse_sql():")
    # Get every keyword and parse it
    keywords = ""

    # Note: That zero is just so pycharm doesn't give me a warning
    def switch_types(value0, key0, iA=None):
        data_type = parse_sql_data_type(value, debug=debug)
        if debug:
            print("    Data type: ", data_type)

        if data_type == "null":
            if isinstance(value0, list) \
                    or isinstance(value0, dict) \
                    or isinstance(value0, bool):
                data_type = "text"

        is_last = iA == len(data) - 1 or iA is None

        # I would use match, but it doesn't work on python 3.7.3
        if mode == "createTableKeys":
            # It's the last one
            if is_last:
                # With no separator
                return key0 + " " + data_type
            else:
                return key0 + " " + data_type + separator
        elif mode == "commaSeparatedKeys":
            # It's the last one
            if is_last:
                return key0
            else:
                return key0 + separator
        elif mode == "commaSeparatedValues":
            # Parse the data
            parsed_value = convert_to_sql_value(value, debug=debug)
            if debug:
                print("    Parsed value: ", parsed_value)
                print("    Its type: ", type(parsed_value))

            # It's the last one
            if is_last:
                return parsed_value
            else:
                return str(parsed_value) + separator

    if debug:
        print("Data type: ", type(data))
        print("Mode: ", mode)
        print("Separator: ", separator)

    # Check if it's a dictionary
    if isinstance(data, dict):
        for i, key in enumerate(data):
            value = data[key]

            if debug:
                print(f"Key: {key}")
                print(f"    I: {i}")
                print(f"    Value: ", value)
                print(f"    Value type: ", type(value))

            result = switch_types(value, key, iA=i)
            keywords += result
    else:
        value = data

        keywords += switch_types(value, value)

    if debug:
        print("Result: ", keywords)
        print("\n")

    return keywords


def get_columns_list(desc: tuple, debug: bool = False) -> list:
    """Get the columns as a list

    tuple desc: The tuple returned when using cur.description"""
    if debug:
        print("\nsqlite_parser -> get_columns_list():")

    new_list = []

    for tup in desc:
        new_list.append(tup[0])

    return new_list
