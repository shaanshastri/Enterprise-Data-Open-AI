import pyodbc
import pandas as pd
from pandasql import sqldf
import sqlalchemy as sa
from sqlalchemy import create_engine

def fetch_data_synapse(serverless_connection_string, query):
    try:
        # Establish a connection to the Synapse Serverless pool
        # conn = pyodbc.connect(serverless_connection_string)
        engine = create_engine(serverless_connection_string)

        with engine.begin() as conn:
            df = pd.read_sql_query(sa.text(query), conn)


        # Process the results
        # tableResult = pd.read_sql(query, conn)
        # df = pd.DataFrame(tableResult)
        # #df.to_csv(r"C:\Users\manaagarwal\Downloads\data.csv", sep=',', index=False)
        output = sqldf("select * from df limit 5")
        print(output)
        return output

    except Exception as e:
        print(f"Error: {str(e)}")
    finally:
        if conn:
            conn.close()
