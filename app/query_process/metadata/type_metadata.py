import json
import re
from typing import Dict

with open("type_metadata.json") as f:
    type_metadata = json.load(f)


def create_doubly_linked_dict() -> Dict:
    return type_metadata


def convert_query(ddl_query, db_name, table_name) -> None:
    types = type_metadata.keys()
    for datatype in types:
        print(f"type value is {datatype}")
        replacement = ""
        replacement = type_metadata[datatype]
        flag_check = re.search(re.escape(datatype), ddl_query, re.IGNORECASE)
        if type(type_metadata[datatype]) is dict:
            datatype_val = type_metadata[datatype]
            replacement = ""
            seq = ""
            if datatype_val["should_generate"] is True:
                # Commenting for future reference
                # seq = table_pk.get_seq_table(table_name, db_name)
                # case_insensitive = re.compile(re.escape(f"TABLE {table_name}"), re.IGNORECASE)
                # ddl_query = case_insensitive.sub("SEQUENCE", ddl_query)
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
