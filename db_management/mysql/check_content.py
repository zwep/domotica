# encoding: utf-8


def check_database_name(cursor, db_name):
    # Check if database exists...
    cursor.execute("SHOW DATABASES")
    res_databases = [x[0] for x in cursor.fetchall()]

    if db_name in res_databases:
        print('Database found: ', db_name)
        res = 1
    else:
        print('Database not found: ', db_name)
        res = 0

    return res


def check_table_name(cursor, table_name, db_name):
    # Check if database exists...
    cursor.execute("USE {db_name}".format(db_name=db_name))
    cursor.execute("SHOW TABLES")
    res_tables = [x[0] for x in cursor.fetchall()]

    if table_name in res_tables:
        print('Table found')
        res = 1
    else:
        print('Table not found')
        res = 0

    return res


def check_table_content(cursor, table_name, db_name):
    # Check if database exists...
    cursor.execute("USE {db_name}".format(db_name=db_name))
    cursor.execute("select * from {table_name} limit 10".format(table_name=table_name))
    A = cursor.fetchall()

    print('\n \t \t First 10 rows...')
    for i, i_row in enumerate(A):
        print(i, ' - ', i_row)

    # Show amount of rows
    cursor.execute("select count(*) from {table_name}".format(table_name=table_name))
    row_count = cursor.fetchall()
    cursor.execute("describe {table_name}".format(table_name=table_name))
    descrb_table = cursor.fetchall()

    print('\n \t \t Total number of rows: {row_count}'.format(row_count=row_count[0][0]))
    print('\n \t \t Describe table: ')

    for i, i_row in enumerate(descrb_table):
        print(i, ' - ', i_row)
