from connectorPostgres import connector as postgres
from connector import connector as rpcconnection
from pprint import pprint
from pubkey_to_address import pubkey_to_address
import json


rpc_connection = rpcconnection('labuit','123456')
pg_connection = postgres('localhost','indexing_address','indexer','123456').set_cursor()


def get_recently_lastest_block():
    return rpc_connection.send_request_to_rpc_server('getblockcount')
# print (get_recently_lastest_block())

def get_current_block(block_hash):
    return rpc_connection.send_request_to_rpc_server('getblock',block_hash)

def get_all_transaction_in_block(block):# block is dictionary type that have method get
    try:
        return block.get('tx','failed to get all txs in block') #return is a list transaction
    except:
        return []

def get_block_hash(block_height):
    return rpc_connection.send_request_to_rpc_server('getblockhash',int(block_height))

def get_raw_transaction(txid):
    return rpc_connection.send_request_to_rpc_server('getrawtransaction',[txid,True])

################
# recent_lastest_block = get_recently_lastest_block()
# block_hash = get_block_hash(recent_lastest_block)
# block  = get_current_block(block_hash)
# txs = get_all_transaction_in_block(block)
# result = list()
# for i in txs:
#     raw_transaction = get_raw_transaction(i)
#     result.append(raw_transaction)
# pprint(result)
#################
# pprint(rpc_connection.send_request_to_rpc_server('getrawtransaction',['1ac7f6024e95c84d4dc53648f4010685b9fdda6916de159f1ba9b62cf80be783',True]))

# raw_transaction = get_raw_transaction("5268696fb3ca2e053b191892cfbd88991818f84d1f1bcdc0ef491092c386bcb9")
# js = json.loads(json.dumps(raw_transaction))
# print ('txinwitness' in js['vin'][0])
# pprint(json.loads(raw_transaction)['vout'][0]['value'])
# pprint(json.loads(raw_transaction)['vout'][0]['scriptPubKey']['addresses'])
# for i in json.loads(raw_transaction)['vout']:
#     pprint(i['scriptPubKey']['addresses'])

#########################
def get_all_addresses_in_vout(vout):
    result = list()
    for i in vout:
        try:
            result.append(i['scriptPubKey']['addresses'])
        except:
            result.append('no starndard')
    return result #[[a,b],[c]]

def get_vout_from_raw_transaction(raw_transaction):
    try:
        return raw_transaction['vout']
    except:
        return json.loads(json.dumps(raw_transaction))['vout']

def get_vin_from_raw_transaction(raw_transaction):
    try:
        return raw_transaction['vin']
    except:
        return json.loads(json.dumps(raw_transaction))['vin']
        # return raw_transaction['vin']
# vin =  '''[{"scriptSig": {"asm": "30440220340e67aef770d40689635736c9b85683fc1e0e11cd64cbf79498f277774e636d022033550d1e2d71c60168aca59561b485fe6eaa4811dbca4fe6ae9f3d32f98023dc[ALL] 032d69da7e61f1cec076d1ace58d96d3ef4a2f3ae248eadbc99846d4aebb653a5d",
#                            "hex": "4730440220340e67aef770d40689635736c9b85683fc1e0e11cd64cbf79498f277774e636d022033550d1e2d71c60168aca59561b485fe6eaa4811dbca4fe6ae9f3d32f98023dc0121032d69da7e61f1cec076d1ace58d96d3ef4a2f3ae248eadbc99846d4aebb653a5d"},
#             "sequence": 4294967295,
#             "txid": "1ac7f6024e95c84d4dc53648f4010685b9fdda6916de159f1ba9b62cf80be783",
#             "vout": 1},
#            {"scriptSig": {"asm": "3045022100850cde2e84cf42069004a9d41a32a4575278dae0c3a71fbaee7bb4650cdabcd302201184f89a5b5bb7b5cb943b597aadfe32f54d012b5faddca26247ab98a5abe510[ALL] 032d69da7e61f1cec076d1ace58d96d3ef4a2f3ae248eadbc99846d4aebb653a5d",
#                            "hex": "483045022100850cde2e84cf42069004a9d41a32a4575278dae0c3a71fbaee7bb4650cdabcd302201184f89a5b5bb7b5cb943b597aadfe32f54d012b5faddca26247ab98a5abe5100121032d69da7e61f1cec076d1ace58d96d3ef4a2f3ae248eadbc99846d4aebb653a5d"},
#             "sequence": 4294967295,
#             "txid": "b8c2baa30898e1204e1d6144519a9618fa7792739d591c4425d25a45db254be4",
#             "vout": 1}]'''

vout = '''[
    {
      "value": 0.00015800,
      "n": 0,
      "scriptPubKey": {
        "asm": "OP_HASH160 0d5461b701c954767a149100ed90338b6e78916f OP_EQUAL",
        "hex": "a9140d5461b701c954767a149100ed90338b6e78916f87",
        "reqSigs": 1,
        "type": "scripthash",
        "addresses": [
          "2MtThrimZNG6hnGGS2CuEwCy7vQ8nwGtJkY"
        ]
      }
    },
    {
      "value": 0.00117732,
      "n": 1,
      "scriptPubKey": {
        "asm": "OP_DUP OP_HASH160 0bb829e0e3e5e4e0189f69b3a41c0bd617f96cd5 OP_EQUALVERIFY OP_CHECKSIG",
        "hex": "76a9140bb829e0e3e5e4e0189f69b3a41c0bd617f96cd588ac",
        "reqSigs": 1,
        "type": "pubkeyhash",
        "addresses": [
          "mgavM5H5uJfsfrKxYDTd9PvBNLuoiaXjt2"
        ]
      }
    }
  ]
'''
# print (pubkey_to_address(json.loads(vin)[0]['scriptSig']['asm'].split(' ')[1],'testnet'))
def get_address_from_vin(vin):
    witness = check_witness(vin)
    coinbase = check_coinbase(vin)
    if  not witness != True and not check_coinbase != True :
        try:
            return pubkey_to_address(vin[0]['scriptSig']['asm'].split(' ')[1],'testnet')
        except:
            return pubkey_to_address(json.loads(vin)[0]['scriptSig']['asm'].split(' ')[1],'testnet')
    else:
        return 'nothing'

def check_witness(vin):
    for i in vin:
        if 'txinwitness' in i:
            return True
            break
    return False

def check_coinbase(vin):
    for i in vin:
        if 'coinbase' in i:
            return True
            break
    return False

              
def get_address_from_vout(vout):
    result = list()
    for i in vout:
        try:
            for address in i['scriptPubKey']['addresses']:
                result.append(address)
        except:
            result.append('non')
    return result

def get_current_transaction():
    pass

def get_txout_transaction():
    pass

def deploy_in_database(blockid,txid,json_data):#json_data : {vin:[a1,a2],vout:[a1,a2]}
    str_to_insert = '''
    INSERT INTO indexing (blockid,txid,attr) VALUES ('%s','%s','%s')
    ''' % (blockid,txid,json_data)
    try:
        pg_connection.method(str_to_insert)
    except Exception as e:
        raise e

def main_action():
    #get block height
    #get block from generssis block to lastest current block
    #get all transaction in block
    #parses vin and vout
    #add in database with: blockhashid,
    for number_block in range(150000,get_recently_lastest_block()):
    # for number_block in range(150000,150002):
        block_hash = get_block_hash(number_block)
        block = get_current_block(block_hash)
        transactions  = get_all_transaction_in_block(block)
        for transaction in transactions:
            raw_transaction = get_raw_transaction(transaction)
            vin = get_vin_from_raw_transaction(raw_transaction)
            vout = get_vout_from_raw_transaction(raw_transaction)
            #get address from public key in vin
            address_from_vin = get_address_from_vin(vin)
            address_from_vout = get_address_from_vout(vout)# it is list [a1,a2,a3]
            json_dump = json.dumps(
            {   "vin": address_from_vin,
                "vout":address_from_vout}
            )
            deploy_in_database(block_hash,transaction,json_dump)
        print "block height: %s" % number_block

main_action()