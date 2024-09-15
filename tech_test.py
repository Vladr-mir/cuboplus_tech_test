import requests
import json
import time

sats_in_bitcoin = 100000000         # how many sats are in a bitcoin
day_to_seconds = 86400              # 86,400 seconds

address = "32ixEdVJWo3kmvJGMTZq5jAQVZZeuwnqzo"
address_stats = f"https://mempool.space/api/address/{address}"
address_transactions = f"https://mempool.space/api/address/{address}/txs"

stats = requests.get(address_stats).json()
transactions = requests.get(address_transactions).json()

onchain_balance = stats['chain_stats']['funded_txo_sum'] / sats_in_bitcoin
mempool_balance = stats['mempool_stats']['funded_txo_sum'] / sats_in_bitcoin

def get_balance_variation(days, transactions):
  sats_counter = 0
  current_epoch = int(time.time())
  target_date = current_epoch - (day_to_seconds * days)

  for transaction in transactions:

    if(transaction['status']['confirmed'] == False):          # ignore if the transaction is unconfirmed
      continue
    elif(transaction['status']['block_time'] < target_date):  # end loop when the target date is reached
      break

    for movement in transaction['vout']:                      # find the address and the value inside of the transaction
      if movement['scriptpubkey_address'] == address:
        current = movement

    sats_counter += current['value']                          # sum the value
  return sats_counter / sats_in_bitcoin

print(f"Onchain balance: {onchain_balance} Btc")              # print everything
print(f"Mempool balance: {mempool_balance} Btc")
print(f"Balance variation in 7 days: {get_balance_variation(7, transactions)}")
print(f"Balance variation in 30 days: {get_balance_variation(30, transactions)}")


