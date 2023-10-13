# Enterprise-Data-Open-AI
Repository for Open AI integration with GPT

# About the project
1. Convert the english language into the required SQL query easily.
2. Run the program and go to localhost:5000
3. Submit your questions and wait for response

# Requirements
1. Python 3.10+
2. PIP
3. IDE like VS-code or pycharm

# Running Locally
We can only run locally after running the below commands. These commands will add all the necessary python libraries in your python interpreter
1. pip install Flask
2. pip install pyodbc
3. pip install openai
4. pip install pandas
5. pip install pandasql

# Starting the flask server
Run main.py file to start the flask server,
1. python main.py

This command will start the flask server at localhost:5000

# Checking the correct driver in your system
If you are getting the below error,

"Error: ('IM002', '[IM002] [Microsoft][ODBC Driver Manager] Data source name not found and no default driver specified (0) (SQLDriverConnect)')"

This means we don't have the required ODBC driver installed in our system. In this case first we need to check the version for the ODBC driver installed in our system. 

In the "nlp.py" file search for "serverless_connection_string", in the driver value we can replace the driver version from "Driver={ODBC Driver 18 for SQL Server}" to "Driver={ODBC Driver (version installed in our system) for SQL Server}".

After this start the flask server again, it will work.
