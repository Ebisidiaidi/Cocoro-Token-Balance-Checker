import os
import time
from web3 import Web3

# Configuration for Base chain
rpc_url = "https://base.llamarpc.com"  # Base RPC URL
contract_address = "0x937a1cFAF0A3d9f5Dc4D0927F72ee5e3e5F82a00"
address_file = "address.txt"  # The file containing wallet addresses
result_file = "result.txt"  # Output file to save results

# Set up Web3 connection
web3 = Web3(Web3.HTTPProvider(rpc_url))

# Check if connection is successful
if not web3.is_connected():
    print("Failed to connect to the Base blockchain!")
    exit()

# ERC-20 ABI fragment for balanceOf and decimals function
ERC20_ABI = [
    {
        "constant": True,
        "inputs": [{"name": "_owner", "type": "address"}],
        "name": "balanceOf",
        "outputs": [{"name": "balance", "type": "uint256"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    },
    {
        "constant": True,
        "inputs": [],
        "name": "decimals",
        "outputs": [{"name": "", "type": "uint8"}],
        "payable": False,
        "stateMutability": "view",
        "type": "function",
    }
]

# Create contract instance
contract = web3.eth.contract(address=contract_address, abi=ERC20_ABI)

# Retry decorator
def retry(func, retries=3, delay=5):
    """
    Retry the function if an error occurs.
    Args:
    - func: The function to retry
    - retries: The number of retries
    - delay: The delay (in seconds) between retries
    """
    attempt = 0
    while attempt < retries:
        try:
            return func()
        except Exception as e:
            attempt += 1
            print(f"Error: {e}. Retrying ({attempt}/{retries})...")
            time.sleep(delay)
    print(f"Function failed after {retries} retries.")
    return None

# Function to get the decimals of the token with retries
def get_decimals():
    def _get_decimals():
        decimals = contract.functions.decimals().call()
        return decimals
    return retry(_get_decimals)

# Function to check the balance of tokens in the wallet with retries
def check_balance(wallet_address, decimals):
    def _check_balance():
        checksum_address = web3.to_checksum_address(wallet_address)  # Convert to checksum address
        raw_balance = contract.functions.balanceOf(checksum_address).call()
        # Convert the raw balance to a human-readable value
        balance = raw_balance / (10 ** decimals)
        return balance
    return retry(_check_balance)

# Function to process all addresses in the address.txt file
def check_wallets_in_file(file_path, result_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    decimals = get_decimals()  # Get the token decimals
    if decimals is None:
        print("Failed to retrieve token decimals after retries. Exiting...")
        return

    with open(file_path, "r") as file:
        addresses = file.readlines()

    total_addresses = len(addresses)  # Get the total number of addresses

    addresses_with_tokens = 0
    total_tokens = 0

    # Open result.txt file to save results
    with open(result_path, "w") as result_file:
        result_file.write("Address | Total Cocoro\n")  # Write the header

        for idx, address in enumerate(addresses, 1):  # Start counting from 1
            address = address.strip()  # Remove any surrounding whitespace or newline
            try:
                # Ensure the address is in checksum format
                checksum_address = web3.to_checksum_address(address)
                if web3.is_address(checksum_address):  # Ensure it's a valid Ethereum address
                    balance = check_balance(address, decimals)
                    if balance is not None:
                        # Format the balance with thousand separators and 18 decimals
                        balance_str = "{:,.18f}".format(balance)
                    
                        # Update counters
                        if balance > 0:
                            addresses_with_tokens += 1
                        total_tokens += balance

                        result_file.write(f"{checksum_address} | {balance_str}\n")
                        print(f"{checksum_address} | {balance_str}")  # Print the result to the console
                    else:
                        result_file.write(f"{checksum_address} | Failed to retrieve balance\n")
                        print(f"{checksum_address} | Failed to retrieve balance")
                else:
                    raise ValueError(f"Invalid Ethereum address: {address}")
            except Exception as e:
                print(f"Error processing address {address}: {e}")
                result_file.write(f"{address} | Invalid address\n")
                
            # Print progress every time an address is processed
            print(f"Progress {idx} of {total_addresses}")

    # Print summary
    print("\nSummary:")
    print(f"Total addresses processed: {total_addresses}")
    print(f"Addresses with tokens: {addresses_with_tokens}")
    print(f"Total tokens found: {total_tokens:,.18f}")

# Check wallets in the address file and save the result
check_wallets_in_file(address_file, result_file)
