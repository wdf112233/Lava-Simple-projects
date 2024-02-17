from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_wallet_balance(rpc_url, wallet_address):
    data = {
        "jsonrpc": "2.0",
        "method": "eth_getBalance",
        "params": [wallet_address, "latest"],
        "id": 1
    }
    headers = {
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(rpc_url, json=data, headers=headers)
        if response.status_code == 200:
            result = response.json()
            if "result" in result:
                balance_wei = int(result["result"], 16)  # Convert hexadecimal balance to integer
                balance_eth = balance_wei / 1e18  # Convert from Wei to Ether
                return balance_eth
            else:
                return "Error: No 'result' in response"
        else:
            return f"Error: Status code {response.status_code}"
    except Exception as e:
        return f"Error: {str(e)}"

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        rpc_url = request.form.get('rpc_url')
        wallet_address = request.form.get('wallet_address')
        if rpc_url and wallet_address:
            balance = get_wallet_balance(rpc_url, wallet_address)
            return render_template('index.html', balance=balance, wallet_address=wallet_address)
        else:
            error_message = "Please provide both RPC URL and wallet address."
            return render_template('index.html', error_message=error_message)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
