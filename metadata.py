import pyodbc


def generate_synapse_ddls(serverless_connection_string, database_name):
    try:
        # Establish a connection to the Synapse Serverless pool
        conn = pyodbc.connect(serverless_connection_string)

        # Create a cursor
        cursor = conn.cursor()

        # Use the information_schema to retrieve table names and columns
        query = f"""
            SELECT TABLE_NAME, COLUMN_NAME, DATA_TYPE
            FROM {database_name}.information_schema.COLUMNS
        """

        # Execute the query
        cursor.execute(query)

        # Initialize DDL statements
        ddl_statements = []

        current_table = None
        current_columns = []

        # Process the results
        for row in cursor.fetchall():
            table_name, column_name, data_type = row

            # If it's a new table, start a new DDL statement
            if table_name != current_table:
                if current_table:
                    # Add the previous table's DDL statement to the list
                    ddl_statements.append(f"CREATE TABLE {current_table} (\n    {', '.join(current_columns)}\n);")

                # Initialize for the new table
                current_table = table_name
                current_columns = []

            # Add the column to the current table's DDL statement
            current_columns.append(f"{column_name} {data_type}")

        # Add the last table's DDL statement to the list
        if current_table:
            ddl_statements.append(f"CREATE TABLE {current_table} (\n    {', '.join(current_columns)}\n);")

        return ddl_statements

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()
