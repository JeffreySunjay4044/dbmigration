from state.db import pk_state


def insert_record_query(created_row, db, table):
    after_keys = created_row.keys()
    after_keys = ",".join(after_keys)
    print(f"Checking format for keys {after_keys}")
    # if type(after.keys()) is not str:
    #  after_keys = json.dumps(after.keys())
    val_list = created_row.values()
    count = 0
    converted_values = ""
    for val in val_list:
        if count > 0:
            converted_values += ','
        elif count == 0:
            count = 1
        if type(val) is not str:
            val = str(val)
        elif type(val) is str:
            val = "'" + val + "'"
        converted_values += val

    print(f"Checking format for values {converted_values}")
    # if type(after.values()) is not str:
    sql_query = f"INSERT INTO {table} VALUES ({converted_values})"
    return sql_query


def delete_record_query(deleted_row, db, table):
    before_keys = deleted_row.keys()
    before_keys = ",".join(before_keys)
    print(f"Checking format for keys {before_keys}")
    # if type(after.keys()) is not str:
    #     after_keys = json.dumps(after.keys())
    primary_key_column = pk_state.get_pk_relations(db, table)
    primary_key_column_value = deleted_row[primary_key_column]

    print(f"DELETE FROM {table} WHERE {primary_key_column} = {primary_key_column_value}")
    # if type(after.values()) is not str:
    sql_query = f"DELETE FROM {table} WHERE {primary_key_column} = {primary_key_column_value}"
    return sql_query


def update_record_query(modified_row, db, table):
    after_keys = modified_row.keys()
    after_keys = ",".join(after_keys)
    print(f"Checking format for keys {after_keys}")
    # if type(after.keys()) is not str:
    #     after_keys = json.dumps(after.keys())
    primary_key_column = pk_state.get_pk_relations(db, table)
    primary_key_column_value = modified_row[primary_key_column]

    val_list = modified_row.values()
    count = 0
    converted_values = ""
    for key in after_keys:
        val = modified_row[key]
        if count > 0:
            converted_values += ','
        elif count == 0:
            count = 1
        if type(val) is not str:
            val = str(val)
        elif type(val) is str:
            val = "'" + val + "'"
        converted_values += key
        converted_values += "= "
        converted_values += val

    print(f"UPDATE {table} SET {converted_values} WHERE {primary_key_column} = {primary_key_column_value}")
    # if type(after.values()) is not str:
    sql_query = f"UPDATE {table} SET {converted_values} WHERE {primary_key_column} = {primary_key_column_value}"
    return sql_query
