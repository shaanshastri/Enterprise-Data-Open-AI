import pyodbc
import pandas as pd
from pandasql import sqldf


def fetch_data_synapse(serverless_connection_string, query):
    try:
        # Establish a connection to the Synapse Serverless pool
        conn = pyodbc.connect(serverless_connection_string)

        # Process the results
        tableResult = pd.read_sql(query, conn)
        df = pd.DataFrame(tableResult)
        #df.to_csv(r"C:\Users\manaagarwal\Downloads\data.csv", sep=',', index=False)
        output = sqldf("select * from df limit 5")
        return output

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()
