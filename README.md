# blitzclock-micro


This is a Python script that connects your Raspiblitz Fullnode (LND) to a Blockclock micro and retrieves data about your Node. It uses that data to update a Blockclock micro, which displays the current Bitcoin block height, unconfirmed onchain transactions, lightning transactions and other relevant information. The update is performed every 5 minutes by a cronjob.

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
5. Change the blockclock_ip to your Blockclock micro IP address

6. Save the config.py file

7. Open a browser on your local machine and got to the webinterface of your Blockclock micro
   ```sh
   http://YOUR-IP-ADDRESS/display
   ``` 
8. Set your screen update rate to MANUAL

9. Go back to your ssh terminal window and open the Cron-Deamon  
   ```sh
   crontab -e
   ``` 
   
10. Put in the following line:
   ```sh
   */5 * * * * /usr/bin/python /home/admin/blitzclock-micro/blitzclock.py
   ``` 
   If you want to change the update time just replace the "5" but please keep in mind that the update time should at least 2 minutes.
   
11. Save the Cronjob  

Please note that the first update might not be correct because the "blitzclock_data.txt" is still empty. After that everything should work as expected.
If you want to use a custom folder location, macaroon path or light colors you can also change that in the config.py file
   

## Features

This script currently supports the following features:

    New Block: Display the current Bitcoin block height and send a tick sound.

    Halving Block: Display the current Bitcoin block height and send a tick sound with color changing light (10 times) 
   
    New incoming Lightning Transaction:Display the incoming amount (60 sec) with a green light (5 sec).
   
    New outgoing Lightning Transaction:Display the outgoing amount (60 sec) with a red light (5 sec).
   
    New routed Transaction: Display the daily earned fee amount (60 sec) with orange light (5 sec).
   
    New unconfirmed onchain transaction: Display the incoming/outgoing amount (60 sec) with orange light (until transaction is confirmed)
    
    New confirmed onchain transaction: Display the incoming/outgoing amount (60 sec) with green light (flashing 3 times)

    New mining adress balance: Display the adress amount (60sec) with blue light (flashing 10 times)

   
   
## Donations

If you like this little fun project please feel free to send some ❤️&⚡

onchain: bc1q82ta28j6k4qgygy66hns64sktg46sgjklyek72

LNURL: lnurl1dp68gurn8ghj7ampd3kx2ar0veekzar0wd5xjtnrdakj7tnhv4kxctttdehhwm30d3h82unvwqhkzmrfv4hxxun9v96x7u3jx5lv6rfy

Lightning Address: aliencreator25@walletofsatoshi.com

Find me on nostr: npub1ddwsgs3k0cvmzgvyru626wt6kgpvtx6yu8y7xljhxw622dghy08qkls259


## License

This project is licensed under the MIT License - see the LICENSE file for details.
