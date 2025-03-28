#!/usr/bin/env python3

import requests
import json
from web3 import Web3

# Configurationæ
COLT_CONTRACT_ADDRESS = "0x3E9df77bf459C2c0c00Df6c64132FC3A71901895"
API_KEY = "CLEF_API"
GNOSIS_RPC_URL = "https://rpc.gnosis.gateway.fm"

# ABI minimal pour la fonction balanceOf
ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function"
    }
]

def main():
    try:
        # Récupérer les transactions
        tx_list_url = f"https://api.gnosisscan.io/api?module=account&action=tokentx&contractaddress={COLT_CONTRACT_ADDRESS}&page=1&offset=1000&apikey={API_KEY}"
        response = requests.get(tx_list_url)
        data = response.json()
        
        if data.get("status") == "1" and isinstance(data.get("result"), list):
            # Extraire les adresses uniques
            addresses = set()
            for tx in data["result"]:
                addresses.add(tx["from"])
                addresses.add(tx["to"])
            
            # Enlever l'adresse zéro
            if "0x0000000000000000000000000000000000000000" in addresses:
                addresses.remove("0x0000000000000000000000000000000000000000")
            
            # Créer un provider et un contrat pour vérifier les soldes
            w3 = Web3(Web3.HTTPProvider(GNOSIS_RPC_URL))
            contract = w3.eth.contract(address=Web3.to_checksum_address(COLT_CONTRACT_ADDRESS), abi=ABI)
            
            # Vérifier le solde de chaque adresse
            for address in addresses:
                try:
                    # Normaliser l'adresse
                    checksum_address = Web3.to_checksum_address(address)
                    balance = contract.functions.balanceOf(checksum_address).call()
                    
                    # Afficher uniquement si le solde est supérieur à 0
                    if balance > 0:
                        print(f"{address}: {balance}")
                except Exception as e:
                    # Ignorer silencieusement les erreurs
                    pass
        else:
            print(f"API error: {data.get('message') or data.get('result') or 'Unknown error'}")
    
    except Exception as e:
        print(f"Erreur: {str(e)}")

if __name__ == "__main__":
    main() 
