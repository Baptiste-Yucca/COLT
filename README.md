# COLT Token Holders

Script JavaScript simple pour récupérer les adresses détenant des tokens COLT (0x3E9df77bf459C2c0c00Df6c64132FC3A71901895) sur la blockchain Gnosis et afficher leurs soldes.

## Installation

1. Assurez-vous d'avoir Node.js (version 14+) installé
2. Installez les dépendances :

```bash
npm install
```

## Utilisation

Exécutez simplement le script :

```bash
node colt_quantity.js
```

Le script va :
1. Se connecter à la blockchain Gnosis via RPC
2. Récupérer les transactions liées au token COLT via l'API Gnosisscan
3. Extraire les adresses uniques qui ont interagi avec le token
4. Vérifier le solde de chaque adresse
5. Afficher les adresses ayant un solde positif au format `adresse: quantité`

## Fonctionnement technique

Le script utilise :
- `ethers.js` pour interagir avec la blockchain Gnosis
- `node-fetch` pour récupérer les données de l'API Gnosisscan
- L'API Gnosisscan avec une clé API pour obtenir les transactions
- La fonction `balanceOf()` du contrat COLT pour vérifier les soldes

## Configuration

Les paramètres de configuration sont définis au début du script :
- Adresse du contrat : `0x3E9df77bf459C2c0c00Df6c64132FC3A71901895`
- Clé API Gnosisscan : Intégrée dans le script
- URL RPC Gnosis : `https://rpc.gnosis.gateway.fm`

## Remarques

- Seules les adresses avec un solde supérieur à 0 sont affichées
- Le script n'affiche pas d'informations supplémentaires pour rester simple et direct
- Pour des raisons de performance, le script limite la recherche aux 1000 dernières transactions 
