def create_record_query(created_row, table):
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


def delete_record_query(deleted_row, table):
    before_keys = deleted_row.keys()
    before_keys = ",".join(before_keys)
    print(f"Checking format for keys {before_keys}")
    # if type(after.keys()) is not str:
    #     after_keys = json.dumps(after.keys())
    val_list = deleted_row.values()
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
    sql_query = f"DELETE FROM {table} VALUES ({converted_values})"
    return sql_query