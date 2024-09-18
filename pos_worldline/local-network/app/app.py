import json
import logging
import os
import ssl
import urllib3

from flask import Flask, request

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test():
    # logging.warning(f"PYTHON TEST LOGGING")
    return "Hello from pos_worldline local-network app. The test is working.", 200

@app.route("/api/v1/DeviceInformation", methods=["GET"])
@app.route("/api/v1/Payments/latest", methods=["GET"])
@app.route("/api/v1/Payments", methods=["POST"])
@app.route("/api/v1/Captures", methods=["POST"])
def forward_request():

    # REQUEST VARIABLES
    cert_file = os.path.join(
        os.path.dirname(__file__),
        "ECR-REST.crt"
    )
    cert_reqs=ssl.CERT_REQUIRED
    path = request.path
    method = request.method
    body = request.json
    host = body.pop("internal_host")
    port = 443
    body_json = json.dumps(body)
    headers = dict(request.headers)
    headers["Content-Length"] = str(len(body_json))

    ################## Also in pos_payment_method.py ####################
    # REQUEST
    # The request needs to use IP address + "ECR-REST.crt".
    # urllib3: 2 args: assert_hostname & ca_certs
    # requests: 1 arg: verify (cannot verify cert only, without hostname)
    pool = urllib3.HTTPSConnectionPool(
        host,
        port=port,
        assert_hostname=False,
        ca_certs=cert_file,
        cert_reqs=cert_reqs,
    )
    response = pool.urlopen(
        method=method,
        url=f"https://{host}:{port}{path}",
        body=body_json,
        headers=headers,
    )
    #####################################################################
    # logging.warning(f"python {response.status}")
    return response.data

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
