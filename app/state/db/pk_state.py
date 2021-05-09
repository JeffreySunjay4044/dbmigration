pk_key_relations = {}
s3_poc_record = {}


def add_pk_relation(db, table, column):
    # update pk key relations from remote preferably s3
    pk_key_relations = pull_from_s3()
    if pk_key_relations[db] is None:
        pk_key_relations[db] = {}
    if pk_key_relations[db][table] is None:
        pk_key_relations[db][table] = column
    modified_db=db
    modified_table=table
    update_to_s3(db, table, column)
    # update pk_key_relationship in s3


def get_pk_relations(db, table):
    return pk_key_relations[db][table]


def pull_from_s3():
    return s3_poc_record


def update_to_s3(db, table, column):
    if s3_poc_record[db] is None:
        s3_poc_record[db] = {}
    if s3_poc_record[db][table] is None:
        s3_poc_record[db][table] = column
