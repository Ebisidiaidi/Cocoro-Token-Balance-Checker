# Cocoro Token Balance Checker

## Description
The **Cocoro Token Balance Checker** is a Python script that connects to the Base blockchain (via an RPC URL) and checks the balances of Ethereum addresses for a specific ERC-20 token. The token balances are fetched from the smart contract, and the results are saved to a text file. The script provides the following features:
- Checks token balances for multiple Ethereum addresses.
- Displays progress ("Progress X of XX") during the execution.
- Retries failed requests due to network or RPC errors.
- Writes results to an output file for further analysis.
- Handles errors like invalid Ethereum addresses gracefully.

## Features
- **Ethereum Compatibility**: Supports checking token balances for ERC-20 tokens on the Base blockchain.
- **Progress Indicator**: Displays the progress while checking each address.
- **Error Handling and Retries**: Retries failed balance checks up to 3 times in case of network errors.
- **Output File**: Saves results in a text file with address and balance information.
- **Easy to Use**: Simply provide a text file with Ethereum addresses, and the script will process them and output the results.

## Requirements
- **Python 3.6+**: The script requires Python version 3.6 or higher.
- **web3.py**: A Python library to interact with Ethereum and ERC-20 tokens.

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Ebisidiaidi/Cocoro-Token-Balance-Checker.git
   cd cocoro-token-balance-checker

2. create address.txt, fill your address for checker:
   ```bash
   address.txt
   
3. Run this script:
   ```bash
   python3 main.py
