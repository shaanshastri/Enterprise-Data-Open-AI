import pyodbc

def generate_synapse_ddls(serverless_connection_string, database_name):
    try:
        # Establish a connection to the Synapse Serverless pool
        conn = pyodbc.connect(serverless_connection_string)

        # Create a cursor
        cursor = conn.cursor()

        # Use the information_schema to retrieve table names, columns, and referential integrity
        query = f"""
            SELECT
                t.TABLE_NAME,
                t.TABLE_SCHEMA,
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.ORDINAL_POSITION,
                c.COLUMN_DEFAULT,
                c.IS_NULLABLE,
                rc.CONSTRAINT_NAME AS REFERENTIAL_CONSTRAINT_NAME,
                rc.UNIQUE_CONSTRAINT_NAME AS UNIQUE_CONSTRAINT_NAME,
                rc.MATCH_OPTION AS MATCH_OPTION,
                rc.UPDATE_RULE AS UPDATE_RULE,
                rc.DELETE_RULE AS DELETE_RULE
            FROM
                [{database_name}].information_schema.COLUMNS c
                JOIN [{database_name}].information_schema.TABLES t ON c.TABLE_NAME = t.TABLE_NAME
                LEFT JOIN [{database_name}].information_schema.KEY_COLUMN_USAGE kcu
                    ON c.TABLE_NAME = kcu.TABLE_NAME AND c.COLUMN_NAME = kcu.COLUMN_NAME
                LEFT JOIN [{database_name}].information_schema.REFERENTIAL_CONSTRAINTS rc
                    ON kcu.CONSTRAINT_NAME = rc.CONSTRAINT_NAME
        """

        # Execute the query
        cursor.execute(query)

        # Initialize DDL statements
        ddl_statements = []

        current_table = None
        current_schema = None
        current_columns = []

        # Process the results
        for row in cursor.fetchall():
            (
                table_name, table_schema, column_name, data_type, ordinal_position,
                column_default, is_nullable, ref_constraint_name, unique_constraint_name,
                match_option, update_rule, delete_rule
            ) = row

            # If it's a new table, start a new DDL statement
            if table_name != current_table or table_schema != current_schema:
                if current_table:
                    # Add the previous table's DDL statement to the list
                    ddl_statements.append(f"CREATE TABLE {current_schema}.{current_table} (\n    {', '.join(current_columns)}\n);")

                # Initialize for the new table
                current_table = table_name
                current_schema = table_schema
                current_columns = []

            # Construct column definition with schema information
            column_definition = f"{column_name} {data_type}"

            if column_default:
                column_definition += f" DEFAULT {column_default}"

            if not is_nullable:
                column_definition += " NOT NULL"

            # Add referential integrity constraints
            if ref_constraint_name:
                column_definition += (
                    f", CONSTRAINT {ref_constraint_name} "
                    f"FOREIGN KEY ({column_name}) REFERENCES {unique_constraint_name} MATCH {match_option} "
                    f"ON UPDATE {update_rule} ON DELETE {delete_rule}"
                )

            # Add the column to the current table's DDL statement
            current_columns.append(column_definition)

        # Add the last table's DDL statement to the list
        if current_table:
            ddl_statements.append(f"CREATE TABLE {current_schema}.{current_table} (\n    {', '.join(current_columns)}\n);")

        return ddl_statements

    except Exception as e:
        print(f"Error: {str(e)}")
        return []
    # finally:
    #     if conn:
    #         conn.close()



# Example usage
# #serverless_connection_string = ('Driver={ODBC Driver 17 for SQL Server};Server=tcp:synw-infra-int-dev-ondemand.sql'
#                                    '.azuresynapse.net,1433;Database=GenAI_v2;Uid=masterdummy_2;Pwd={'
#                                    '!pass@123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
serverless_connection_string = ('Driver={ODBC Driver 17 for SQL Server};Server=tcp:sqldb-cl-dev-001.database.'
                                'windows.net,1433;Database=sqldb-cl-dev-002;Uid=serveradmin;Pwd={'
                                    'Admin123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"')
database_name = "sqldb-cl-dev-002"

conn = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=tcp:sqldb-cl-dev-001.database.windows.net,1433;DATABASE=sqldb-cl-dev-002;UID=serveradmin;PWD=Admin123'


ddl_statements = generate_synapse_ddls(conn,database_name)

for statement in ddl_statements:
    print(statement)


