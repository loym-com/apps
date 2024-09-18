import json
import logging
import os
import ssl
import urllib3

from flask import Flask, request

app = Flask(__name__)

@app.route("/test", methods=["GET"])
def test():
    logging.warning(f"PYTHON TEST LOGGING")
    return "Hello from pos_worldline local-network app. The test is working.", 200

@app.route("/api/v1/DeviceInformation", methods=["GET"])
@app.route("/api/v1/Payments/latest", methods=["GET"])
@app.route("/api/v1/Payments", methods=["POST"])
def forward_request():

    # REQUEST VARIABLES
    cert_file = os.path.join(
        os.path.dirname(__file__),
        "ECR-REST.crt"
    )
    cert_reqs=ssl.CERT_REQUIRED
    # cert_reqs=ssl.CERT_NONE
    path = "/api/v1/DeviceInformation"
    method = "GET"
    key = "853919076C353385"
    body = {}
    host = "10.0.1.6"
    port = 443
    body_json = json.dumps(body)
    headers = {
        "content-type": "application/json; charset=utf-8",
        "Integration-Key": key,
        "User-Agent" : "Odoo 16.0",
        "Content-Length": str(len(body_json))
    }

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
    logging.warning(f"python {response.status}")
    return response



response = forward_request()
print(response.status)
