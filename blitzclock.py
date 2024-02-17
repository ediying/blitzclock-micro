#!/usr/bin python
# -*- coding: utf-8 -*-

import base64, codecs, json, requests, time
from pathlib import Path
from config import *
from datetime import datetime

blockcount = 0
feeDay= 0
feeWeek= 0
feeMonth= 0
unconfirmedBalance= 0
confirmedBalance= 0
totalBalance= 0
totalSatoshisSent= 0
miningBalance= 0
miningAdress= 'bc1qcx9wurgkat8s9msz9v3clh6apmx7sy65rp9mws'
halvingInterval = 210000


def getData(lndRequest):

    global blockcount
    global feeDay
    global feeWeek
    global feeMonth
    global unconfirmedBalance
    global confirmedBalance
    global totalBalance
    global totalSatoshisSent
    global totalSatoshisReceived

    url = f'https://localhost:8080/v1/{lndRequest}'
    cert_path = tls_cert_path
    macaroon = codecs.encode(open(macaroon_path, 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    r = requests.get(url, headers=headers, verify=cert_path)
    print(f'Response {lndRequest}: {r.json()}')
    print(type(r.json()))
    print('/n')

    if lndRequest == 'channels':
        dict_str = str(r.json())
        # Remove unwanted characters from the string
        for x in range(len("[]{}'")):
            dict_str = dict_str.replace("[]{}'"[x], "")
        # Split the string into a list and sum up total satoshis sent
        dict_list = dict_str.split(', ')
        totalSatoshisSent = [int(s.strip('total_satoshis_sent: ')) for s in dict_list if "total_satoshis_sent" in s]
        totalSatoshisSent = sum(totalSatoshisSent)
        totalSatoshisReceived = [int(s.strip('total_satoshis_received: ')) for s in dict_list if "total_satoshis_received" in s]
        totalSatoshisReceived  = sum(totalSatoshisReceived)

    dict = r.json()
    
    blockcount = dict.get("block_height")
    feeDay = dict.get("day_fee_sum")
    feeWeek = dict.get("week_fee_sum")
    feeMonth = dict.get("month_fee_sum")
    unconfirmedBalance = dict.get("unconfirmed_balance")
    confirmedBalance = dict.get("confirmed_balance")
    totalBalance = dict.get("total_balance")
   

def printRequest():
    print(r)  # Check status code for response received  (success code - 200)
    print(r.content)  # Print content of request
    print('/n')


# Load Blockchain Data .txt and put it in a dict
blockchainData = open(f'{folder_location}blitzclock_data.txt', 'r')
blockchainData =json.loads(blockchainData.read())
print(f'Blockchain Data .txt: {blockchainData}')
print(type(blockchainData))
print('/n')


getData("channels") # Lightning channels query

# Incoming Transaction 
if  int(totalSatoshisReceived) > int(blockchainData['Total Satoshis received']):
    lightningAmount = (int(totalSatoshisReceived)) - (int(blockchainData['Total Satoshis received']))
    # Write Lightning Balance in dict
    blockchainData['Total Satoshis received'] = totalSatoshisReceived
    # Send Balance to Blockclock
    url = base_url_text + str('-') + str(lightningAmount)
    print(url)
    print('/n')
    r = requests.get(url, 'pair=SATS/IN') # Making a GET request
    printRequest()
    r  = requests.get(send_light_on + light_color_green)
    time.sleep(5)
    if blockchainData['Unconfirmed Onchain Transaction'] == True:
        r  = requests.get(send_light_on + light_color_orange)  
    else: 
        r  = requests.get(send_light_off)
    blockchainData['Screen Blockcount'] = False

# Outgoing Transaction 
elif  int(totalSatoshisSent) > int(blockchainData['Total Satoshis sent']):
    lightningAmount = (int(totalSatoshisSent)) - (int(blockchainData['Total Satoshis sent']))
    # Write Lightning Balance in dict
    blockchainData['Total Satoshis sent'] = totalSatoshisSent
    # Send Balance to Blockclock
    url = base_url_text + str('-') + str(lightningAmount)
    print(url)
    print('/n')
    r = requests.get(url, 'pair=SATS/OUT') # Making a GET request
    printRequest()
    r  = requests.get(send_light_on + light_color_red)
    time.sleep(5)
    if blockchainData['Unconfirmed Onchain Transaction'] == True:
        r  = requests.get(send_light_on + light_color_orange)
    else: 
        r  = requests.get(send_light_off)
    blockchainData['Screen Blockcount'] = False


getData("fees") # Lnd fee query

if  feeDay != blockchainData['Fee Day']:
    # Write fee in dict
    blockchainData['Fee Day'] = feeDay
    # Send Fee Report to Blockclock
    url = base_url_text + str('-') + str(feeDay)
    print(url)
    print('/n')
    r = requests.get(url, 'pair=SATS/DAY') # Making a GET request
    printRequest()
    r  = requests.get(send_light_on + light_color_blue)
    time.sleep(5)
    if blockchainData['Unconfirmed Onchain Transaction'] == True:
        r  = requests.get(send_light_on + light_color_orange)
    else: 
        r  = requests.get(send_light_off)       
    blockchainData['Screen Blockcount'] = False


getData("balance/blockchain") # Unconfirmed Tx query

if  int(totalBalance) == int(confirmedBalance) and blockchainData['Unconfirmed Onchain Transaction'] == True:
    blockchainData['Unconfirmed Onchain Transaction'] = False
    blockchainData['Total Onchain Balance'] = totalBalance
    blockchainData['Confirmed Onchain Balance'] = confirmedBalance
    # Send Total Balance to Blockclock
    url = base_url_text + str(totalBalance)
    print(url)
    print('/n')
    r = requests.get(url, 'tl=total onchain amount') # Making a GET request
    printRequest()
    for i in range(3):
        r  = requests.get(send_light_on + light_color_green)
        r  = requests.get(send_light_off)
    blockchainData['Screen Blockcount'] = False

# Incoming Transaction
if  int(totalBalance) > int(blockchainData['Total Onchain Balance']):
    onchainAmount = int(totalBalance) - int(blockchainData['Total Onchain Balance'])
    blockchainData['Unconfirmed Onchain Transaction'] = True
    # Write Onchain Balance in dict
    url = base_url_text + str(onchainAmount)
    print(url)
    print('/n')
    r = requests.get(url, 'tl=Unconfirmed incoming satoshis') # Making a GET request
    printRequest()
    r  = requests.get(send_light_on + light_color_orange)
    blockchainData['Screen Blockcount'] = False

# Outgoing Transaction 
elif  int(totalBalance) < int(blockchainData['Total Onchain Balance']):
    onchainAmount = int(blockchainData['Total Onchain Balance']) - int(totalBalance)
    blockchainData['Unconfirmed Onchain Transaction'] = True
    # Send Amount to Blockclock
    url = base_url_text + str(onchainAmount)
    print(url)
    print('/n')
    r = requests.get(url, 'tl=Unconfirmed outgoing satoshis') # Making a GET request
    printRequest()
    r  = requests.get(send_light_on + light_color_orange)
    blockchainData['Screen Blockcount'] = False


#RPC Bitcoinexplorer check mining adress balance
url = f'https://192.168.178.46:3021/api/address/{miningAdress}'
response = requests.get(url, verify=False)
data = json.loads(response.text)   
balance_sat = data.get("txHistory", {}).get("balanceSat", None)
miningBalance = balance_sat
print(miningBalance)


getData("getinfo") # Blockcount query

# Show Blockcount
if  blockchainData['Screen Blockcount'] == False:
    time.sleep(61)
    
if  int(miningBalance) > int(blockchainData['Mining Balance']):
    blockchainData['Mining Balance'] = miningBalance
    # Send Mining Balance to Blockcklock
    url = base_url_text + str(miningBalance)
    print(url)
    print('/n')
    r = requests.get(url, 'tl=satoshis mined') # Making a GET request
    printRequest()
    for i in range(10):
        r  = requests.get(send_light_on + light_color_blue)
        r  = requests.get(send_light_off)
    time.sleep(61)
    
# Send Blockheight to Blockclock
url = base_url_text + str(blockcount)
print(url)
print('/n')

if blockcount % halvingInterval == 0:
    r = requests.get(url, 'tl=Halving!') # Making a GET request
    printRequest()
    blockchainData['Screen Blockcount'] = True
    light_colors = [light_color_green, light_color_red, light_color_blue, light_color_orange]
    for _ in range(10):
        for color in light_colors:
            r = requests.get(send_light_on + color)
    r = requests.get(send_light_off)

r = requests.get(url, 'tl=Number of blocks in the blockchain') # Making a GET request
printRequest()
blockchainData['Screen Blockcount'] = True
    
if  blockcount != blockchainData['Blockcount']:
    # Write blockcount in dict
    blockchainData['Blockcount'] = blockcount
    r = requests.get(send_tick_sound) # Making a GET request
    blockchainData['Screen Blockcount'] = True


# Override blitzclock_data.txt
with open(f'{folder_location}blitzclock_data.txt',"w") as file:
    file.write(json.dumps(blockchainData, indent= 4))
    file.close()
print(f' New Blockchain Data .txt: {blockchainData}')
