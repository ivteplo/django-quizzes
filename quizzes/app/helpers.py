# Copyright (c) 2022 Ivan Teplov

import re
from django.http import QueryDict


def deep_merge(first_dictionary: dict, second_dictionary: dict) -> dict:
    result = {}
    second_dictionary = { **second_dictionary }

    for key in first_dictionary:
        if key in second_dictionary and type(second_dictionary[key]) is dict \
           and type(first_dictionary[key]) is dict:
            result[key] = deep_merge(first_dictionary[key], second_dictionary[key])
            second_dictionary.pop(key)
        elif key in second_dictionary:
            result[key] = second_dictionary[key]
            second_dictionary.pop(key)
        else:
            result[key] = first_dictionary[key]

    for key in second_dictionary:
        result[key] = second_dictionary[key]

    second_dictionary.clear()
    return result


def parse_dict_keys(parameters: QueryDict or dict) -> dict:
    """
    This function is used in order to convert a dictionary with the root-level
    keys to a dictionary with subditionaries.

    Example:
    source = {
        "answers[0][is_right]": True,
        "answers[1][is_right]": False,
        "answers[2][is_right]": False,
        "answers[0][text]": "Answer 1",
        "answers[1][text]": "Answer 2",
        "answers[2][text]": "Answer 3"
    }
    result = {
        "answers": {
            "0": {
                "is_right": True,
                "text": "Answer 1",
            },
            "1": {
                "is_right": False,
                "text": "Answer 2",
            },
            "2": {
                "is_right": False,
                "text": "Answer 2",
            }
        }
    }
    """
    result = dict()

    for key in parameters:
        if re.match(r"[a-zA-Z0-9_]+(\[[a-zA-Z0-9_]+\])+", key):
            name, leftovers = key.split('[', 1)
            leftovers = leftovers.replace(']', '', 1)

            subdictionary = parse_dict_keys({
                leftovers: parameters[key]
            })

            if name in result and type(result[name]) is dict:
                result[name] = deep_merge(result[name], subdictionary)
            else:
                result[name] = subdictionary
        else:
            result[key] = parameters[key]

    return result
