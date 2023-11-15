import openai
from metadata import generate_synapse_ddls
from fetch_data import fetch_data_synapse
from langchain_experimental.sql import SQLDatabaseChain
from langchain.utilities import SQLDatabase
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import create_sql_query_chain
import os
from sqlalchemy.engine import URL


def convert_nlp_to_sql_poc(prompt_text):
    # openai.api_key = "c4b435efc4a2442880527e59169438a8"
    # openai.api_base = "https://cog-6sbix7titqeb2.openai.azure.com/"
    # openai.api_type = 'azure'
    # openai.api_version = '2023-07-01-preview'
    # deployment_name = 'davinci'
    # database_name = "GenAI_v2"

    serverless_connection_string = ('Driver={ODBC Driver 17 for SQL Server};Server=tcp:synw-infra-int-dev-ondemand.sql'
                                    '.azuresynapse.net,1433;Database=GenAI_v2;Uid=masterdummy_2;Pwd={'
                                    '!pass@123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    
    # Azure Synapse Analytics as Consumption Layer
    # my_uid = "masterdummy_2"
    # my_pwd = "!pass@123"
    # my_host = "tcp:synw-infra-int-dev-ondemand.sql.azuresynapse.net,1433"
    # my_db = "GenAI_v2"
    # my_odbc_driver = "ODBC Driver 17 for SQL Server"


    my_uid = "serveradmin"
    my_pwd = "Admin123"
    my_host = "tcp:sqldb-cl-dev-001.database.windows.net,1433"
    my_db = "sqldb-cl-dev-002"
    my_odbc_driver = "ODBC Driver 17 for SQL Server"

    connection_url = URL.create(
        "mssql+pyodbc",
        username=my_uid,
        password=my_pwd,
        host=my_host,
        database=my_db,  # required; not an empty string
        query={"driver": my_odbc_driver},
    )
    # print(connection_url)

    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_VERSION"] = '2023-07-01-preview'
    os.environ["OPENAI_API_BASE"] = "https://cog-6sbix7titqeb2.openai.azure.com/"
    os.environ["OPENAI_API_KEY"] = "c4b435efc4a2442880527e59169438a8"

    db = SQLDatabase.from_uri(connection_url)

    print(db)

    #setting Azure OpenAI env variables

    llm = AzureChatOpenAI(deployment_name="davinci", temperature=0, max_tokens=1000)
    # db_chain = SQLDatabaseChain.from_llm(llm=llm, db=db, verbose=True)

    # from langchain.chat_models import ChatOpenAI
    chain = create_sql_query_chain(llm, db)
    print(chain)
    response = chain.invoke({"question":prompt_text})
    out = fetch_data_synapse(serverless_connection_string, response)
    return response, out
    #return response
    
