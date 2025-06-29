import pandas as pd

from flask import Flask, request
from logging.config import dictConfig
from utils import QueryParser


# Configure logging for the Flask application
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})


# Standup Flask application
app = Flask(__name__)

# Simulate a database with a CSV file
data_df: pd.DataFrame = pd.read_csv('mock_server/data.csv')
data: dict = data_df.to_dict(orient='records')


@app.route("/rest/2.0/login", methods=["POST"])
def login():
    """
    Mock login endpoint for BillingPlatform API.

    :return: A mock login response containing a session ID and an error code of 0, indicating success.
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

    :return: A mock logout response containing an error code of 0, indicating success.
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

    :return: A mock query response containing the results of a query as a dictionary or JSON of records.
    """
    sql_query: str = request.args.get('sql')
    
    if sql_query:
        # Parse the incoming SQL query
        query = QueryParser(sql_query)
        parsed_query = query.parse()
        app.logger.debug(f"Parsed SQL Query: {parsed_query}")
    
    query_response = {
        "queryResponse": data
    }

    return query_response


@app.route("/rest/2.0/<string:entity>/<int:record_id>")
def retrieve_by_id(entity: str, record_id: int):
    """
    Mock query endpoint for BillingPlatform API.

    :param entity: The entity to retrieve records from.
    :param record_id: The ID of the record to retrieve.
    :return: A mock retrieve response containing the results of a query as a dictionary or JSON of records.
    """
    retrieve_response = {
        "retrieveResponse": data[record_id] if record_id < len(data) else {}
    }

    return retrieve_response


@app.route("/rest/2.0/<string:entity>", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
def crud_methods(entity: str):
    """
    Mock query endpoint for BillingPlatform API.

    :param entity: The entity to retrieve records from.
    :return: A mock retrieve response containing the results of a query as a dictionary or JSON of records.
    """
    if request.method not in ["GET", "POST", "PUT", "PATCH", "DELETE"]:
        return {"error": "Method not allowed"}, 405
    
    if request.method == "GET":
        ansi_sql: str = request.args.get('queryAnsiSql')

        if ansi_sql:
            # Parse the incoming ANSI SQL query
            app.logger.debug(f"ANSI SQL: {ansi_sql}")

        retrieve_response = {
            "retrieveResponse": data
        }

        return retrieve_response
    
    # Create
    if request.method == "POST":
        # Handle POST request logic here
        if not request.json:
            return {"error": "Invalid input"}, 400
        
        app.logger.debug(f"Received POST data: {request.json}")

        create_response = {
            "createResponse": {
                "message": "Record created successfully",
                "entity": entity,
                "record_id": len(data) + 1
            }
        }

        return create_response
    
    # Update
    if request.method == "PUT":
        # Handle PUT request logic here
        if not request.json:
            return {"error": "Invalid input"}, 400
        
        app.logger.debug(f"Received PUT data: {request.json}")

        update_response = {
            "updateResponse": {
                "message": "Record updated successfully",
                "entity": entity
            }
        }

        return update_response
    
    # Upsert
    if request.method == "PATCH":
        # Handle PATCH request logic here
        if not request.json:
            return {"error": "Invalid input"}, 400
        
        app.logger.debug(f"Received PATCH data: {request.json}")

        upsert_response = {
            "upsertResponse": [
                {
                    "Id": 0,
                    "success": True,
                    "ErrorText": "string",
                    "ErrorElementField": "string",
                    "created": True
                }
            ]
        }

        return upsert_response
    
    # Delete
    if request.method == "DELETE":
        # Handle DELETE request logic here
        app.logger.debug(f"Received DELETE data: {request.json}")

        delete_response = {
            "deleteResponse": {
                "message": "Record deleted successfully",
                "entity": entity
            }
        }

        return delete_response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
    