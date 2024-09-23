This module implements synchronious payment with Worldline terminmal for Norway.


INSTALL

Requirements:

- Odoo dependency: https://github.com/OCA/web/tree/16.0/web_notify

- IoT-box, see separate documentation
  Create a firewall forwarding of requests from Odoo's IP address to the IoT-box.

- Local docker service to connect from Odoo in the cloud,
  since the terminal "is NOT compatible with a cloud-native ECR".
  https://developer.samport.com/getting-started/network-requirements/

  Copy pos_worldline/local-network.
  cd /path/to/local-network
  docker compose up -d

  Create a firewall forwarding of requests from Odoo's IP address to the local service.
  For security reasons, no other IP address should be able to access the local service.
  The local service listens on port 777.


CONFIGURE

JOURNAL: Invoicing - Configuration - Accounting - Journals: NEW

- Type: Bank

PAYMENT METHOD: Point of Sale - Configuration - Payment Methods: NEW

- Journal: Select a bank journal
- Use a Payment Terminal: Worldline
- Terminal host: The IP address of the terminal
- External host:port: Public IP address & port to access the terminal from the internet,
  via a local service.

SETTINGS: Point of Sale - Configuration - Settings

- Point of Sale - Payment - Payment Methods (add Worldline)
- Point of Sale - Connected Devices - IoT Box (IP Address: https://x.x.x.x:x)
- General Settings - Document Layout (select a layout)

BROWSER: Do this to accept the self signed certificate

- Go to the IoT Box IP Address https://x.x.x.x:x
- Click on Advanced - Continue to x.x.x.x (unsafe page)


USE

In the POS UI, the network icon is green if the IoT Box is detected.
In the payment screen, select the payment method and click the button below.
If the connection is lost during payment:

- Keep the POS UI open until it is back.
  Otherwise there may be a never ending "Request sent", and the order must be deleted.
- Ask the customer not to pay until the connection is back.
  If paid during loss of connection and the POS UI is closed:
  Open the payment method. Click to PRINT LATEST RECEIPT (from terminal, no products).

Close the session by the end of each day.
Otherwise payments cannot be taken the next day until the session is closed.

Logs: Point of Sale - Configuration - Payment Terminal Logs


TODO

- Test with a timeout to prevent a never ending "Request sent".
- PDF-utskrifter får feil Æ Ø Å.
- Skriv ut alt på kvitteringsskriver i stedet for PDF.
