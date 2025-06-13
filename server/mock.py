import pandas as pd

from flask import Flask, request


app = Flask(__name__)

# Simulate a database with a CSV file
data_df: pd.DataFrame = pd.read_csv('server/data.csv')
data: dict = data_df.to_dict(orient='records')


@app.route("/rest/2.0/login", methods=["POST"])
def login():
    """
    Mock login endpoint for BillingPlatform API.
    This endpoint simulates a successful login response.
    It returns a session ID and an error code of 0, indicating success.
    """
    login_response = {
        "loginResponse": [
            {
                "SessionID": "thisIsASessionID",
                "ErrorCode": "0",
                "ErrorText": []
            }
        ]
    }

    return login_response


@app.route("/rest/2.0/logout", methods=["POST"])
def logout():
    """
    Mock logout endpoint for BillingPlatform API.
    This endpoint simulates a successful logout response.
    It returns a session ID and an error code of 0, indicating success.
    """
    logout_response = {
        "logoutResponse": [
            {
                "ErrorCode": "0",
                "ErrorText": []
            }
        ]
    }

    return logout_response


@app.route("/rest/2.0/query")
def query():
    """
    Mock query endpoint for BillingPlatform API.
    This endpoint simulates a successful query response.
    It returns the results of a query as a dictionary or JSON of records.
    """
    sql_query: str = request.args.get('sql')
    print(sql_query)
    
    query_response = {
        "queryResponse": data
    }

    return query_response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)