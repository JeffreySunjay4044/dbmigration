import json
import re
from typing import Dict

with open("type_metadata.json") as f:
    type_metadata = json.load(f)


def create_doubly_linked_dict() -> Dict:
    return type_metadata


def add_keywords(ddl_query):
    is_alter_column = re.search('ALTER COLUMN', ddl_query, re.IGNORECASE)
    if is_alter_column is not None:
        res = re.search('COLUMN', ddl_query, re.IGNORECASE)
        end = res.end()
        word_started = False
        column_end_pos = 0
        column_start_pos = 0
        for i in range(end, len(ddl_query)):
            char = ddl_query[i]
            if word_started is True:
                if char is " ":
                    column_end_pos = i
                    break
            else:
                if char is not " ":
                    word_started = True
                    column_start_pos = i
        ddl_query = ddl_query[:column_end_pos] + " type" + ddl_query[column_end_pos:]
        print(f"Column start pos , endpos, ddl, {column_start_pos}, {column_start_pos}, {type(ddl_query)}")
    return ddl_query


def convert_query(ddl_query) -> None:
    types = type_metadata.keys()
    ddl_query = add_keywords(ddl_query)
    for datatype in types:
        print(f"type value is {datatype}")
        flag_check = re.search(re.escape(datatype), ddl_query, re.IGNORECASE)
        if type(type_metadata[datatype]) is dict:
            datatype_val = type_metadata[datatype]
            replacement = ""
            seq = ""
            if datatype_val["should_generate"] is True:
                if flag_check is not None:
                    ddl_query = None
                    return ddl_query
            replacement += seq + datatype_val["replace_with_prefix"]
        else:
            replacement = type_metadata[datatype]
            case_insensitive = re.compile(re.escape(datatype), re.IGNORECASE)
            ddl_query = case_insensitive.sub(replacement, ddl_query)
            print(f"the changed datatype query is {ddl_query}")
    return ddl_query
