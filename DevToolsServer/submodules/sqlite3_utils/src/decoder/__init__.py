import json


def decode_json_recursively(val: dict, debug: bool = False):
    """Decodes json recursively"""
    if debug:
        print("\ndecoder -> decode_json_recursively():")

    def decode_json(new_value):
        """Decode json"""
        # It's a string, it could be json encoded
        if isinstance(new_value, str):
            # Try to parse
            try:
                parsed_value = json.loads(new_value)

                # Yeah, I'm a lil illiterate
                # Hollup, it might not be the encoded value of this class
                # Check for the ___forced_value field
                try:
                    forced_value = parsed_value["___forced_value"]

                    # Hollup, it might not be the boolean value
                    if isinstance(forced_value, bool) and forced_value:
                        # 'Aight this is the one
                        # Let's return the value part which is where the data is
                        return parsed_value["value"]
                except:
                    pass
            except:
                # It's not json
                pass
        # It's not 'sqlite3utils encoded' XD
        return new_value

    new_dict = {}
    for key, value in val.items():
        new_dict[key] = decode_json(value)

        # What if that key has more encoded json?
        if isinstance(new_dict[key], dict):
            new_dict[key] = decode_json_recursively(new_dict[key])

    return new_dict


def decode_recursively_list_or_dict(data):
    """Decode recursively a dictionary or a list of dictionaries"""
    if isinstance(data, dict):
        decoded_data = decode_json_recursively(data)
        return decoded_data
    elif isinstance(data, list):
        # It's a list, decode 'em all
        # Clone the list
        decoded_data = list(data)

        # Iterate through it
        for i in range(len(decoded_data)):
            element = decoded_data[i]
            if isinstance(element, dict):
                decoded_data[i] = decode_json_recursively(element)
        return decoded_data
    raise Exception("Data is neither a dictionary nor a list/list of dictionaries")
