import openai
from metadata import generate_synapse_ddls
from fetch_data import fetch_data_synapse


def convert_nlp_to_sql_poc(prompt_text):
    openai.api_key = "c4b435efc4a2442880527e59169438a8"
    openai.api_base = "https://cog-6sbix7titqeb2.openai.azure.com/"
    openai.api_type = 'azure'
    openai.api_version = '2023-07-01-preview'
    deployment_name = 'davinci'
    database_name = "GenAI"

    serverless_connection_string = ('Driver={ODBC Driver 17 for SQL Server};Server=tcp:synw-infra-int-dev-ondemand.sql'
                                    '.azuresynapse.net,1433;Database=GenAI;Uid=masterdummy;Pwd={'
                                    '!pass@123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
    metadata_adv = generate_synapse_ddls(serverless_connection_string, database_name)

    full_prompt = '''Given the following SQL tables,your job is to write the query given users question.\n''' + str(
        metadata_adv) + ''' \nReturn only the query, no need to explain.\n''' + str(prompt_text) + '''.'''
    response = openai.Completion.create(
        engine=deployment_name,
        prompt=full_prompt,
        temperature=0,
        max_tokens=600,
        top_p=1.0,
        frequency_penalty=0.0,
        presence_penalty=0.0,
        stop=["#", ";"])

    answer = response.choices[0].text.strip()
    final_ans = answer.replace("'", "").replace("?", "").replace("<|im_end|>", "")
    try:
        out = fetch_data_synapse(serverless_connection_string, final_ans)
        return final_ans, out
    except Exception as e:
        print(f"Error: {str(e)}")
