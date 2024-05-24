This module implements synchronious payment with Worldline terminmal for Norway.

The easiest way is to use a mobile terminal connecting directly to the internet

LANE 3000 is NOT accessible from the internet, only from local network.
"local-network" has a Docker setup for a web server and python script.

- In app.py, set the IP address and the Integration Key of the payment terminal.
- Copy the ECR-REST.crt from the API pages of Worldline.

The local firewall should forward traffic to the payment terminal and to the IoT box.


TODO

- PDF-utskrifter får feil Æ Ø Å.
- Skriv ut alt på kvitteringsskriver i stedet for PDF.

Payments/latest

- Print latest receipt meny? (Payments/latest) bør ikke trenge host og key i server action.
- Terminal log listevisning knapp?
