# 🚀 CryptoBulkSender

![GitHub last commit](https://img.shields.io/github/last-commit/xPOURY4/CryptoBulkSender)
![GitHub issues](https://img.shields.io/github/issues/xPOURY4/CryptoBulkSender)
![GitHub stars](https://img.shields.io/github/stars/xPOURY4/CryptoBulkSender?style=social)

A powerful bulk token sender for multiple blockchain networks with beautiful CLI interface! 💎

## ✨ Features

- 🔗 **Multi-Network Support**: Ethereum, Polygon, BSC, Avalanche, and more
- 🪙 **Any Token Type**: Native tokens (ETH, MATIC, BNB) and ERC-20 tokens
- 📁 **Address Management**: Import recipient addresses from text file
- 🎨 **Beautiful CLI**: Colored output with real-time progress tracking
- 🔍 **Transaction Verification**: Direct explorer links for each transaction
- ⚙️ **Easy Configuration**: Simple network setup in configuration file
- 🔒 **Security First**: Private key stored in environment variables
- ⏱️ **Network Verification**: Automatic chain ID validation
- 📊 **Transaction Summary**: Success/failure statistics
- 🔄 **Retry Mechanism**: Automatic retries for failed transactions

## 🛠 Prerequisites

- Python 3.8+
- Node.js (for optional tools)
- Wallet with sufficient balance on target network

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/xPOURY4/CryptoBulkSender.git
cd CryptoBulkSender
```

### 2. Create virtual environment
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configuration
Create `.env` file:
```env
PRIVATE_KEY=your_private_key_here
```

Create `address.txt` with recipient addresses (one per line):
```
0x1234567890123456789012345678901234567890
0x0987654321098765432109876543210987654321
...
```

## 🎯 Usage

### Run the script
```bash
python main.py
```

### Execution flow:
1. **Network Connection**: Automatic connection to configured network
2. **Address Loading**: Import addresses from `address.txt`
3. **Amount Input**: Enter token amount to send
4. **Confirmation**: Review transaction summary and confirm
5. **Transaction Processing**: Execute transactions with progress display
6. **Result Display**: Explorer links and final statistics

### Sample Output:
```
============================================================
  CryptoBulkSender - Holesky Testnet
============================================================
✓ Connected to Holesky Testnet (Chain ID: 17000)
🔵 Loaded 25 recipient addresses
💰 Enter amount in ETH to send: 0.1
⚠️ Ready to send 0.1 ETH to 25 addresses
Confirm? (y/n): y

🔵 Processing transactions...
🔵 Transaction 1/25
⏳ Waiting for confirmation... (Tx: 0x7a8b9c...)
✅ Success! Sent to 0x1234...7890
🔵 Explorer: https://holesky.etherscan.io/tx/0x7a8b9c...

============================================================
✅ Summary: 25/25 transactions successful
============================================================
```

## ⚙️ Network Configuration Examples

### 1. Ethereum Holesky Testnet
```python
NETWORK_CONFIG = {
    'holesky': {
        'name': 'Holesky Testnet',
        'rpc_url': 'https://rpc.ankr.com/eth_holesky',
        'chain_id': 17000,
        'explorer_url': 'https://holesky.etherscan.io',
        'currency': 'ETH',
        'decimals': 18
    }
}
```

### 2. Ethereum Mainnet
```python
NETWORK_CONFIG = {
    'mainnet': {
        'name': 'Ethereum Mainnet',
        'rpc_url': 'https://mainnet.infura.io/v3/YOUR_PROJECT_ID',
        'chain_id': 1,
        'explorer_url': 'https://etherscan.io',
        'currency': 'ETH',
        'decimals': 18
    }
}
```

### 3. Polygon Mainnet
```python
NETWORK_CONFIG = {
    'polygon': {
        'name': 'Polygon Mainnet',
        'rpc_url': 'https://polygon-rpc.com',
        'chain_id': 137,
        'explorer_url': 'https://polygonscan.com',
        'currency': 'MATIC',
        'decimals': 18
    }
}
```

### 4. Binance Smart Chain Mainnet
```python
NETWORK_CONFIG = {
    'bsc': {
        'name': 'Binance Smart Chain',
        'rpc_url': 'https://bsc-dataseed.binance.org/',
        'chain_id': 56,
        'explorer_url': 'https://bscscan.com',
        'currency': 'BNB',
        'decimals': 18
    }
}
```

### 5. Avalanche Mainnet
```python
NETWORK_CONFIG = {
    'avalanche': {
        'name': 'Avalanche Mainnet',
        'rpc_url': 'https://api.avax.network/ext/bc/C/rpc',
        'chain_id': 43114,
        'explorer_url': 'https://snowtrace.io',
        'currency': 'AVAX',
        'decimals': 18
    }
}
```

### 6. Fantom Mainnet
```python
NETWORK_CONFIG = {
    'fantom': {
        'name': 'Fantom Mainnet',
        'rpc_url': 'https://rpc.ftm.tools',
        'chain_id': 250,
        'explorer_url': 'https://ftmscan.com',
        'currency': 'FTM',
        'decimals': 18
    }
}
```

### 7. Arbitrum One
```python
NETWORK_CONFIG = {
    'arbitrum': {
        'name': 'Arbitrum One',
        'rpc_url': 'https://arb1.arbitrum.io/rpc',
        'chain_id': 42161,
        'explorer_url': 'https://arbiscan.io',
        'currency': 'ETH',
        'decimals': 18
    }
}
```

### 8. Optimism
```python
NETWORK_CONFIG = {
    'optimism': {
        'name': 'Optimism',
        'rpc_url': 'https://mainnet.optimism.io',
        'chain_id': 10,
        'explorer_url': 'https://optimistic.etherscan.io',
        'currency': 'ETH',
        'decimals': 18
    }
}
```

### 9. Gnosis Chain
```python
NETWORK_CONFIG = {
    'gnosis': {
        'name': 'Gnosis Chain',
        'rpc_url': 'https://rpc.gnosischain.com',
        'chain_id': 100,
        'explorer_url': 'https://gnosisscan.io',
        'currency': 'xDAI',
        'decimals': 18
    }
}
```

### 10. Moonbeam
```python
NETWORK_CONFIG = {
    'moonbeam': {
        'name': 'Moonbeam',
        'rpc_url': 'https://rpc.api.moonbeam.network',
        'chain_id': 1284,
        'explorer_url': 'https://moonscan.io',
        'currency': 'GLMR',
        'decimals': 18
    }
}
```

To switch networks, simply change the `CURRENT_NETWORK` variable:
```python
CURRENT_NETWORK = 'polygon'  # or any other network key
```

## 🔐 Security Notes

- 🔑 **Never store private keys in code** - Always use environment variables
- 🛡️ **Test on testnets first** before using on mainnet
- 💸 **Verify wallet balance** covers all transactions + gas fees
- 🔄 **Manually verify large transactions** before confirmation
- 🌐 **Use reputable RPC providers** for network connections

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License 

## 🙏 Acknowledgments

- [Web3.py](https://web3py.readthedocs.io/) for blockchain interaction
- [Colorama](https://pypi.org/project/colorama/) for colored terminal output
- [Etherscan](https://etherscan.io/) for blockchain explorer APIs
- All network providers for their public RPC endpoints

---

⭐ If this project helped you, please give it a star!  
🐛 Report bugs in [Issues](https://github.com/xPOURY4/CryptoBulkSender/issues)  
💡 Feature requests are welcome!
