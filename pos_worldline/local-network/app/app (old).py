import json
import urllib3
from flask import Flask, request
app = Flask(__name__)


### IMPORTANT VARIABLES ###
integration_key = ""
terminal_host = ""
###########################


@app.route('/*', methods=['GET'])
def get_pay():
    return "Hello, Get Pay!", 200

@app.route('/*', methods=["GET", "POST"])
def pay():
    data = request.get_json()
    json_payload = json.dumps(data["payload"])

    pool = urllib3.HTTPSConnectionPool(
        terminal_host,
        assert_hostname=False, # Setting assert_hostname to False disables the hostname verification because URL will not match certificate.
        ca_certs="./ECR-REST.crt",
    )
    headers = {
        "content-type": "application/json; charset=utf-8",
        "Integration-Key": integration_key,
        "User-Agent" : "MyECR 1.0",
        "Content-Length": str(len(json_payload))
    }
    # Try sending a basic sync payment and print the response (response is only returned once you abort or finalize the payment in the terminal)
    try:
        req = pool.urlopen(request.method, request.path, body=json_payload, headers=headers)
        response = json.loads(req.data)
        # response = {"status": "success", "message": "Payment successful."}
        return response, 200
    except Exception as e:
        raise e

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
