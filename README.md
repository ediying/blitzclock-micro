# blitzclock-micro


This is a Python script that connects to your Bitcoin Lightning Network Daemon (LND) and retrieves data about your Lightning channels and balances. It uses that data to update a Blockclock device, which displays the current Bitcoin block height and other relevant information.
Getting Started

To use this script, you'll need:

    A Blockclock device
    A Bitcoin Lightning Network Daemon (LND) node with a valid TLS certificate and Macaroon file
    Python 3.x installed on your computer

Installation

    Clone this repository to your local machine:

bash

git clone https://github.com/your-username/lightning-blockclock.git

    Install the required Python packages using pip:

bash

pip install -r requirements.txt

    Edit the config.py file to include your Blockclock device's IP address and API key, as well as the paths to your LND TLS certificate and Macaroon files.

    Run the script:

bash

python lightning_blockclock.py

The script will retrieve data from your LND node and update your Blockclock device accordingly.
Features

This script currently supports the following features:

    Display the current Bitcoin block height on your Blockclock device.
    Display the total Lightning balance, including unconfirmed funds.
    Display the Lightning commit fees for all open channels.
    Display the total on-chain balance, including unconfirmed funds.
    Detect incoming and outgoing Lightning transactions and update the Blockclock display accordingly.
    Detect changes in LND fees and update the Blockclock display accordingly.

License

This project is licensed under the MIT License - see the LICENSE file for details.
Acknowledgments

    This script was inspired by Blockclock Jr. Lightning by @21isenough.
    Thanks to the developers of the pyln-client library for making it easy to interact with LND via Python.
