import json
import re
from typing import Dict
from . import table_pk

with open('type_metadata.json') as f:
    type_metadata = json.load(f)


def create_doubly_linked_dict() -> Dict:
    return type_metadata


def convert_query(ddl_query, db_name, table_name) -> str:
    types = type_metadata.keys()
    for datatype in types:
        replacement = ""
        if type(type_metadata[datatype]) is Dict:
            datatype_val = type_metadata[datatype]
            replacement = datatype_val["replace_with_prefix"]
            seq = ""
            if datatype_val["should_generate"] is True:
                seq = table_pk.get_seq_table(table_name, db_name)
            replacement += seq
        case_insensitive = re.compile(re.escape(datatype), re.IGNORECASE)
        ddl_query = case_insensitive.sub(replacement, ddl_query)
    print(f"the changed datatype query is {ddl_query}")
    return ddl_query
