from flask import Flask

app = Flask(__name__)

@app.route("/rest/2.0/login", methods=["POST"])
def login():
    """
    Mock login endpoint for BillingPlatform API.
    This endpoint simulates a successful login response.
    It returns a session ID and an error code of 0, indicating success.
    """
    success_response = {
        "loginResponse": [
            {
                "SessionID": "thisIsASessionID",
                "ErrorCode": "0",
                "ErrorText": []
            }
        ]
    }

    return success_response

@app.route("/rest/2.0/logout", methods=["POST"])
def logout():
    """
    Mock logout endpoint for BillingPlatform API.
    This endpoint simulates a successful logout response.
    It returns a session ID and an error code of 0, indicating success.
    """
    return {'LoggedOut': 'true'}


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=80)