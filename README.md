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
5. Change the blockclock_ip to your Blockclock micro IP address

6. Save the config.py file

7. Open a browser on your local machine and got to the webinterface of your Blockclock micro
   ```sh
   http://YOUR-IP-ADDRESS/display
   ``` 
8. Set your scrren update rate to MANUAL

9. Go back to your ssh terminal window and open the Cron-Deamon  
   ```sh
   crontab -e
   ``` 
   
10. Put in the following line:
   ```sh
   */5 * * * * /usr/bin/python /home/admin/blitzclock-micro/blitzclock.py
   ``` 
   blas
11. Save the Cronjon  


If you want to use a custom folder location, macaroon path or light colors you can change also change that in the config.py file
   


## Features

Show how to use the project or library.
    
## License

This project is licensed under the MIT License - see the LICENSE file for details.
