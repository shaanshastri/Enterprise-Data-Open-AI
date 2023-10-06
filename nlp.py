import openai
from metadata import generate_synapse_ddls


def convert_nlp_to_sql_poc(prompt_text):
    openai.api_key = "c4b435efc4a2442880527e59169438a8"
    openai.api_base = "https://cog-6sbix7titqeb2.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-07-01-preview'
    deployment_name = 'davinci'
    database_name = "GenAI"
    serverless_connection_string = ('Driver={ODBC Driver 13 for SQL Server};Server=tcp:synw-infra-int-dev-ondemand.sql'
                                    '.azuresynapse.net,1433;Database=GenAI;Uid=masterdummy;Pwd={'
                                    '!pass@123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    metadata_adv = generate_synapse_ddls(serverless_connection_string, database_name)
    full_prompt = '''Given the following SQL tables, ''' + str(
        metadata_adv) + '''your job is to write the query given users question \n''' + str(prompt_text) + '''.'''
    response = openai.Completion.create(
        engine=deployment_name,
        prompt=full_prompt,
        temperature=0,
        max_tokens=800,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None)
    answer = response.choices[0].text.strip()
    return answer


# print(convert_nlp_to_sql_poc("Write a SQL query which will give customers with highest amount of sales orders"))
