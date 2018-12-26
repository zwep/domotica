# encoding: utf-8


def check_database_name(cursor, db_name):
    # Check if database exists...
    cursor.execute("show databases")
    res_databases = [x[0] for x in cursor.fetchall()]

    if db_name in res_databases:
        print('Database found')
        res = 1
    else:
        print('Database not found')
        res = 0

    return res


def check_table_name(cursor, table_name, db_name):
    # Check if database exists...
    cursor.execute("use ", db_name)
    cursor.execute("show tables")
    res_tables = [x[0] for x in cursor.fetchall()]

    if table_name in res_tables:
        print('Table found')
        res = 1
    else:
        print('Table not found')
        res = 0

    return res
