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
lightningBalance= 0
commitFeesSum= 0


def getData(lndRequest):

    global blockcount
    global feeDay
    global feeWeek
    global feeMonth
    global unconfirmedBalance
    global confirmedBalance
    global totalBalance
    global lightningBalance
    global commitFeesSum

    url = f'https://localhost:8080/v1/{lndRequest}'
    cert_path = tls_cert_path
    macaroon = codecs.encode(open(macaroon_path, 'rb').read(), 'hex')
    headers = {'Grpc-Metadata-macaroon': macaroon}
    r = requests.get(url, headers=headers, verify=cert_path)
    print(f'Response {lndRequest}: {r.json()}')
    print(type(r.json()))
    print('/n')

    if lndRequest == 'channels':
        dict = str(r.json())
        # Remove characters from string
        for x in range(len("[]{}'")):
            dict = dict.replace("[]{}'"[x],"")
        # Split string to list and add up commit fee    
        dict= dict.split(', ')
        commitFees = [s for s in dict if "commit_fee" in s]
        x = 0
        while x < len(commitFees):
            commitFees[x] = commitFees[x].strip('commit_fee: ')
            x = x + 1   
        commitFees = list(map(int, commitFees))
        commitFeesSum = sum(commitFees)
        
    dict = r.json()
    
    blockcount = dict.get("block_height")
    feeDay = dict.get("day_fee_sum")
    feeWeek = dict.get("week_fee_sum")
    feeMonth = dict.get("month_fee_sum")
    unconfirmedBalance = dict.get("unconfirmed_balance")
    confirmedBalance = dict.get("confirmed_balance")
    totalBalance = dict.get("total_balance")
    lightningBalance = dict.get("balance")
   

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
getData("balance/channels") # Lightning balance query

# Incoming Transaction 
if  int(lightningBalance) - commitFeesSum > int(blockchainData['Lightning Balance']) - blockchainData['Lightning Commit Fees Sum']:
    lightningAmount = (int(lightningBalance) - commitFeesSum) - (int(blockchainData['Lightning Balance']) - blockchainData['Lightning Commit Fees Sum'])
    # Write Lightning Balance in dict
    blockchainData['Lightning Balance'] = lightningBalance
    blockchainData['Lightning Commit Fees Sum'] = commitFeesSum
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
elif int(lightningBalance) - commitFeesSum < int(blockchainData['Lightning Balance']) - blockchainData['Lightning Commit Fees Sum']:
    lightningAmount = (int(blockchainData['Lightning Balance']) - blockchainData['Lightning Commit Fees Sum']) - (int(lightningBalance) - commitFeesSum) 
    # Write Lightning Balance in dict
    blockchainData['Lightning Balance'] = lightningBalance
    blockchainData['Lightning Commit Fees Sum'] = commitFeesSum
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


getData("getinfo") # Blockcount query

# Show Blockcount
if blockchainData['Screen Blockcount'] == False:
    time.sleep(61)
    # Send Blockheight to Blockclock
    url = base_url_text + str(blockcount)
    print(url)
    print('/n')
    r = requests.get(url, 'tl=Number of blocks in the blockchain') # Making a GET request
    printRequest()
    blockchainData['Screen Blockcount'] = True

if  blockcount != blockchainData['Blockcount']:
    # Write blockcount in dict
    blockchainData['Blockcount'] = blockcount
    # Send Blockheight to Blockclock
    url = base_url_text + str(blockcount)
    print(url)
    print('/n')
    r = requests.get(url, 'tl=Number of blocks in the blockchain') # Making a GET request
    printRequest()
    r = requests.get(send_tick_sound) # Making a GET request
    blockchainData['Screen Blockcount'] = True


# Override blitzclock_data.txt
with open(f'{folder_location}blitzclock_data.txt',"w") as file:
    file.write(json.dumps(blockchainData, indent= 4))
    file.close()
print(f' New Blockchain Data .txt: {blockchainData}')
