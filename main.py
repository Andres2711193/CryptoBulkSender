from web3 import Web3
import os
from dotenv import load_dotenv
import time
from colorama import init, Fore, Style
import requests

# Initialize colorama for colored output
init(autoreset=True)

# Load environment variables
load_dotenv()

# Configuration - Easily modify these for different networks/tokens
NETWORK_CONFIG = {
    'holesky': {
        'name': 'Holesky Testnet',
        'rpc_url': 'https://rpc.ankr.com/eth_holesky',
        'chain_id': 17000,
        'explorer_url': 'https://holesky.etherscan.io',
        'currency': 'ETH',
        'decimals': 18
    },
    # Add other networks here (e.g., mainnet, polygon, etc.)
}

# Current network selection (can be changed to any key in NETWORK_CONFIG)
CURRENT_NETWORK = 'holesky'

# Get configuration for current network
config = NETWORK_CONFIG[CURRENT_NETWORK]

def validate_private_key(private_key):
    """Validate and format private key"""
    if not private_key:
        raise ValueError("Private key is empty")
    
    # Remove any whitespace or special characters
    private_key = private_key.strip()
    
    # Remove 0x prefix if present
    if private_key.startswith('0x'):
        private_key = private_key[2:]
    
    # Check if it's a valid 64-character hex string
    if not len(private_key) == 64:
        raise ValueError(f"Invalid private key length: {len(private_key)} characters (expected 64)")
    
    try:
        # Try to convert to integer to validate hex
        int(private_key, 16)
        return '0x' + private_key
    except ValueError:
        raise ValueError("Private key contains non-hexadecimal characters")

def get_web3_connection():
    """Establish Web3 connection with retry mechanism"""
    max_retries = 3
    for attempt in range(max_retries):
        try:
            w3 = Web3(Web3.HTTPProvider(config['rpc_url']))
            if w3.is_connected():
                return w3
            print(f"{Fore.YELLOW}Connection attempt {attempt + 1} failed. Retrying...")
            time.sleep(2)
        except Exception as e:
            print(f"{Fore.RED}Connection error: {str(e)}")
            time.sleep(2)
    
    print(f"{Fore.RED}Failed to connect after {max_retries} attempts")
    exit(1)

def check_network(w3):
    """Verify we're on the correct network"""
    try:
        chain_id = w3.eth.chain_id
        if chain_id != config['chain_id']:
            print(f"{Fore.RED}Network mismatch! Expected {config['chain_id']} ({config['name']}), got {chain_id}")
            return False
        print(f"{Fore.GREEN}✓ Connected to {config['name']} (Chain ID: {chain_id})")
        return True
    except Exception as e:
        print(f"{Fore.RED}Network check failed: {str(e)}")
        return False

def load_addresses():
    """Load recipient addresses from file"""
    try:
        with open('address.txt', 'r') as file:
            addresses = [line.strip() for line in file if line.strip()]
            if not addresses:
                print(f"{Fore.RED}No addresses found in address.txt")
                exit(1)
            print(f"{Fore.CYAN}Loaded {len(addresses)} recipient addresses")
            return addresses
    except FileNotFoundError:
        print(f"{Fore.RED}address.txt file not found!")
        exit(1)

def get_amount():
    """Get transfer amount from user with validation"""
    while True:
        try:
            amount = input(f"{Fore.YELLOW}Enter amount in {config['currency']} to send: ")
            amount_in_wei = Web3.to_wei(float(amount), 'ether')
            print(f"{Fore.GREEN}Amount: {amount} {config['currency']} ({amount_in_wei} wei)")
            return amount_in_wei
        except ValueError:
            print(f"{Fore.RED}Please enter a valid number")

def send_transaction(w3, private_key, recipient, amount):
    """Send transaction and return receipt"""
    try:
        sender = w3.eth.account.from_key(private_key).address
        nonce = w3.eth.get_transaction_count(sender)
        
        # Get current gas price
        gas_price = w3.eth.gas_price
        
        # Build transaction
        tx = {
            'chainId': config['chain_id'],
            'nonce': nonce,
            'to': recipient,
            'value': amount,
            'gas': 21000,
            'gasPrice': gas_price
        }
        
        # Estimate gas as a safety check
        try:
            estimated_gas = w3.eth.estimate_gas(tx)
            if estimated_gas > 21000:
                tx['gas'] = estimated_gas + 1000  # Add buffer
        except Exception as e:
            print(f"{Fore.YELLOW}Gas estimation failed: {str(e)}")
        
        # Sign transaction
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        
        # Send transaction (fixed for web3.py v6+)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        
        # Wait for transaction receipt
        print(f"{Fore.BLUE}⏳ Waiting for confirmation... (Tx: {tx_hash.hex()[:10]}...)")
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=120)
        
        return receipt
    except Exception as e:
        print(f"{Fore.RED}Transaction failed: {str(e)}")
        return None

def display_results(receipt, recipient):
    """Display transaction results with explorer link"""
    if receipt and receipt.status == 1:
        tx_hash = receipt.transactionHash.hex()
        explorer_link = f"{config['explorer_url']}/tx/{tx_hash}"
        print(f"{Fore.GREEN}✅ Success! Sent to {recipient[:10]}...{recipient[-4:]}")
        print(f"{Fore.CYAN}Explorer: {explorer_link}")
    else:
        print(f"{Fore.RED}❌ Transaction failed for {recipient[:10]}...{recipient[-4:]}")

def main():
    # Display header
    print(f"{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.MAGENTA}  Crypto Sender - {config['name']}")
    print(f"{Fore.MAGENTA}{'='*60}")
    
    # Setup connection
    w3 = get_web3_connection()
    
    # Verify network
    if not check_network(w3):
        exit(1)
    
    # Load addresses
    addresses = load_addresses()
    
    # Get amount
    amount = get_amount()
    
    # Get and validate private key
    private_key = os.getenv('PRIVATE_KEY')
    if not private_key:
        print(f"{Fore.RED}PRIVATE_KEY not set in environment variables!")
        exit(1)
    
    try:
        private_key = validate_private_key(private_key)
        print(f"{Fore.GREEN}✓ Private key validated successfully")
    except ValueError as e:
        print(f"{Fore.RED}Invalid private key: {str(e)}")
        exit(1)
    
    # Confirm before sending
    print(f"\n{Fore.YELLOW}Ready to send {Web3.from_wei(amount, 'ether')} {config['currency']} to {len(addresses)} addresses")
    confirm = input(f"{Fore.YELLOW}Confirm? (y/n): ").lower()
    if confirm != 'y':
        print(f"{Fore.RED}Operation cancelled")
        exit(0)
    
    # Process transactions
    print(f"\n{Fore.CYAN}Processing transactions...")
    success_count = 0
    
    for i, recipient in enumerate(addresses, 1):
        print(f"\n{Fore.BLUE}Transaction {i}/{len(addresses)}")
        receipt = send_transaction(w3, private_key, recipient, amount)
        if receipt:
            display_results(receipt, recipient)
            success_count += 1
        time.sleep(1)  # Small delay between transactions
    
    # Summary
    print(f"\n{Fore.MAGENTA}{'='*60}")
    print(f"{Fore.GREEN}Summary: {success_count}/{len(addresses)} transactions successful")
    print(f"{Fore.MAGENTA}{'='*60}")

if __name__ == "__main__":
    main()
