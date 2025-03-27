#!/usr/bin/env node

const fetch = require('node-fetch');
const { ethers } = require('ethers');

// Configuration
const COLT_CONTRACT_ADDRESS = '0x3E9df77bf459C2c0c00Df6c64132FC3A71901895';
const API_KEY = 'TA_CLEF_API_GNOSISSCAN';
const GNOSIS_RPC_URL = 'https://rpc.gnosis.gateway.fm';

// ABI minimal pour la fonction balanceOf
const ABI = [
  'function balanceOf(address) view returns (uint256)'
];

async function main() {
  try {
    // Récupérer les transactions
    const txListUrl = `https://api.gnosisscan.io/api?module=account&action=tokentx&contractaddress=${COLT_CONTRACT_ADDRESS}&page=1&offset=1000&apikey=${API_KEY}`;
    const response = await fetch(txListUrl);
    const data = await response.json();
    
    if (data.status === '1' && Array.isArray(data.result)) {
      // Extraire les adresses uniques
      const addresses = new Set();
      for (const tx of data.result) {
        addresses.add(tx.from);
        addresses.add(tx.to);
      }
      
      // Enlever l'adresse zéro
      addresses.delete('0x0000000000000000000000000000000000000000');
      
      // Créer un provider et un contrat pour vérifier les soldes
      const provider = new ethers.JsonRpcProvider(GNOSIS_RPC_URL);
      const contract = new ethers.Contract(COLT_CONTRACT_ADDRESS, ABI, provider);
      
      // Vérifier le solde de chaque adresse
      for (const address of addresses) {
        try {
          const balance = await contract.balanceOf(address);
          
          // Afficher uniquement si le solde est supérieur à 0
          if (balance > 0) {
            console.log(`${address}: ${balance.toString()}`);
          }
        } catch (error) {
          // Ignorer silencieusement les erreurs
        }
      }
    } else {
      console.error(`API error: ${data.message || data.result || 'Unknown error'}`);
    }
  } catch (error) {
    console.error(`Erreur: ${error.message}`);
  }
}

// Lancer le script
main().catch(error => {
  console.error(`Erreur: ${error.message}`);
}); 
