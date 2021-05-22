import json

with open('table_pk.json') as f:
    table_pk = json.load(f)


def get_seq_table(table_name, db_name):
    seq_id = ""
    if table_pk[table_name] is not None:
        seq_id += db_name + "_" + table_name;
        table_pk_config = table_pk[table_name]
        if table_pk_config["serial"] is True:
            seq_id += "_" + table_pk_config["primary_key"]
    return seq_id
