import pyodbc

def generate_ddl_from_metadata(connection):
    ddl_statements = []

    cursor = connection.cursor()

    # Fetch column details from Table 1 (column name, data type, precision, nullability, and primary key)
    cursor.execute("SELECT source_object_attribute_name, source_object_attribute_data_type, source_object_attribute_precision, Column_IS_Null, Column_IS_PrimaryKey, source_object_name FROM ctlfwk.vw_source_objects_attributes")
    column_metadata = cursor.fetchall()

    # Fetch table names and schema names from Table 2
    cursor.execute("SELECT source_object_name, Schema_Name FROM ctlfwk.vw_source_objects")
    table_metadata = cursor.fetchall()

    table_columns = {}
    for column_info in column_metadata:
        table_name = column_info[-1]  # Fetch the last item in the column_info list for the table name
        if table_name not in table_columns:
            table_columns[table_name] = []
        table_columns[table_name].append(column_info)

    for table_info in table_metadata:
        table_name = table_info[0]
        schema_name = table_info[1]
        
        columns = table_columns.get(table_name, [])

        column_definitions = [
            f"{column[0]} {column[1]}{f'({column[2]})' if column[2] else ''}" +
            (f" NOT NULL" if column[3] == 'N' else "") +
            (" PRIMARY KEY" if column[4] == 'Y' else "")
            for column in columns
        ]

        ddl = f"CREATE TABLE {schema_name}.{table_name} (\n  {',  '.join(column_definitions)}\n)"
        ddl_statements.append(ddl)

    return ddl_statements

# Connect to Azure SQL Database using pyodbc
conn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:sqldb-cl-dev-001.database.windows.net,1433;DATABASE=sqldb-cl-dev-prd2;UID=serveradmin;PWD=Admin123'
)

ddl_statements = generate_ddl_from_metadata(conn)

for statement in ddl_statements:
    print(statement)

conn.close()
