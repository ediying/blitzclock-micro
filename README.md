# blitzclock-micro

This is a Python script that connects your Raspiblitz Fullnode (LND) to a Blockclock micro and retrieves data about your Node. It uses that data to update a Blockclock micro, which displays the current Bitcoin block height, unconfirmed onchain transactions, lighning transactions and other relevant information. The update is performed every 5 minutes by a cronjob.

## Getting Started

To use this script, you'll need:

+ [A Raspiblitz Fullnode with LND running](https://github.com/rootzoll/raspiblitz)
+ [Blockclock Micro](https://blockclockmicro.com)


## Getting Started

1. Open an ssh connection to your Raspiblitz

2. Clone the repo to your /home/admin folder
   ```sh
   git clone https://github.com/ediying/blitzclock-micro
   ```
3. Go to the blitzclock-micro folder
   ```sh
   cd blitzclock-micro
   ```
4. Open the config.py file
   ```sh
   nano config.py
   ```
5. Change the blockclock_ip to your Blockclock micro IP 
   


## Features

Show how to use the project or library.
    
## License

This project is licensed under the MIT License - see the LICENSE file for details.
