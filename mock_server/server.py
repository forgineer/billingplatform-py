import pandas as pd

from flask import Flask, request
from logging.config import dictConfig
from utils import QueryParser


# Configure logging for the Flask application
dictConfig({
    'version': 1,
    'formatters': {
        'default': {
            'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
        }
    },
    'handlers': {
        'wsgi': {
            'class': 'logging.StreamHandler',
            'stream': 'ext://flask.logging.wsgi_errors_stream',
            'formatter': 'default'
        }
    },
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


@app.route("/auth/1.0/authenticate", methods=["POST"])
def oauth_login():
    """
    Mock OAuth login endpoint for BillingPlatform API.

    :return: A mock login response containing a fake access token.
    """
    oauth_response = {
        "access_token": "my_access_token",
        "refresh_token": "my_refresh_token",
        "token_type": "Bearer",
        "expires_in": 9999
    }

    return oauth_response


@app.route("/rest/2.0/login", methods=["POST"])
def login():
    """
    Mock login endpoint for BillingPlatform API.

    :return: A mock login response containing a fake session ID.
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
        "logoutResponse":[
            {
                "ErrorCode":"0",
                "ErrorText":" ",
                "Success":"true"
            }
        ]
    }

    return logout_response


@app.route("/rest/2.0/query")
def query():
    """
    Mock query endpoint for BillingPlatform API.

    :return: A mock query response containing the results of a query as a dictionary or JSON payload of records.
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
    Mock retrieve endpoint for BillingPlatform API.

    :param entity: The entity to retrieve records from.
    :param record_id: The ID of the record to retrieve.
    :return: A mock retrieve response containing the results of the request as a dictionary or JSON payload of records.
    """
    retrieve_response = {
        "retrieveResponse": data[record_id] if record_id < len(data) else {}
    }

    return retrieve_response


@app.route("/rest/2.0/<string:entity>", methods=["GET", "POST", "PUT", "PATCH"])
def cruu_methods(entity: str):
    """
    Mock create, retrieve, update, and upsert endpoint for BillingPlatform API.

    :param entity: The entity to perform the CRUU operation on.
    :return: A mock response containing the results of an action as a dictionary or JSON payload of records.
    """
    if request.method not in ["GET", "POST", "PUT", "PATCH"]:
        return {"error": "Method not allowed"}, 405
    
    # Retrieve
    # Handle GET request logic here
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
    # Handle POST request logic here
    if request.method == "POST":
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
    # Handle PUT request logic here
    if request.method == "PUT":
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
    # Handle PATCH request logic here
    if request.method == "PATCH":
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


@app.route("/rest/2.0/delete/<string:entity>", methods=["DELETE"])
def delete(entity: str):
    """
    Mock delete endpoint for BillingPlatform API.

    :param entity: The entity to delete records from.
    :return: A mock delete response as a dictionary or JSON payload.
    """
    if request.method not in ["DELETE"]:
        return {"error": "Method not allowed"}, 405
    
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


@app.route("/rest/2.0/undelete/<string:entity>", methods=["DELETE"])
def undelete(entity: str):
    """
    Mock undelete endpoint for BillingPlatform API.

    :param entity: The entity to undelete records from.
    :return: A mock undelete response as a dictionary or JSON payload.
    """
    # Delete
    if request.method == "DELETE":
        # Handle DELETE request logic here
        app.logger.debug(f"Received UNDELETE data: {request.json}")

        delete_response = {
            "deleteResponse": {
                "message": "Record deleted successfully",
                "entity": entity
            }
        }

        return delete_response


@app.route("/rest/2.0/bulk_api_request", methods=["POST"])
def bulk_request():
    """
    Mock bulk extract request endpoint for BillingPlatform API.

    :param entity: The entity to request a bulk extract for.
    :return: A mock response for the bulk request as a dictionary or JSON payload.
    """
    # Bulk API requests
    app.logger.debug(f"Received BULK REQUEST data: {request.json}")

    bulk_response = {
        "createResponse": [
            {
                "ErrorCode": "0",
                "ErrorText": " ",
                "ErrorElementField": " ",
                "Id": "8675309"
            }
        ]
    }

    return bulk_response


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)
    