# Binance Trading Bot 🪙
This project is a CLI-based trading bot built on top of the Binance API (Testnet supported).  
It allows you to execute different types of trading strategies such as Limit Orders, Market Orders, Stop-Limit Orders, OCO Orders, and TWAP Orders directly from the command line.

📌 All logs are stored in `app.log`.

---

## 📦 Setup

1. Clone this folder:
- **Git Bash**
```bash
git clone https://github.com/AryanGupta0007/aryan_binance_bot
```

2. Change cmd location to Project root
- **Git Bash**
```bash
cd aryan_binance_bot/
```

2. create a  virtual environment :
- **Git Bash**
```bash
python -m venv myenv
```


2. Activate the virtual environment :
- **Windows PowerShell**
```powershell
.\myenv\Scripts\Activate.ps1
```

- **Git Bash**
```bash
source myenv/Scripts/activate 
```

While activating myenv on powershell if an error occurs, run:
- **Windows PowerShell**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```
Then retry:
- **Windows PowerShell**
```powershell
.\myenv\Scripts\Activate.ps1
```

4. Install the requirements
- **Windows PowerShell**
```powershell
Set-ExecutionPolicy -ExecutionPolicy Unrestricted -Scope CurrentUser
```
Then retry:
- **Windows PowerShell**
```powershell
.\myenv\Scripts\Activate.ps1
```


5. Create a .env folder in root folder  Configure Binance API keys in a `.env` file:
```
BINANCE_API_KEY=your_api_key
BINANCE_API_SECRET=your_api_secret
```

---

## 🚀 Running the Scripts

### 1. Limit Orders
- **Git Bash**
```bash
python src/limit_orders.py <symbol> <side> <quantity> <limit_price>
python src/limit_orders.py btcusdt sell 0.01 112831.2
```
- **Windows PowerShell**
```powershell
python .\src\limit_orders.py btcusdt sell 0.01 112831.2
```

### 2. Market Orders
- **Git Bash**
```bash
python src/market_orders.py <symbol> <side> <quantity>
python src/market_orders.py btcusdt sell 0.01
```
- **Windows PowerShell**
```powershell
python .\src\market_orders.py btcusdt sell 0.01
```

### 3. Stop-Limit Orders
- **Git Bash**
```bash
python src/advanced/stop_limit.py <symbol> <limit_price> <stop_price> <quantity> <side>
python src/advanced/stop_limit.py btcusdt 112000 112500 0.01 buy
```
- **Windows PowerShell**
```powershell
python .\src\advanced\stop_limit.py btcusdt 112000 112500 0.01 buy
```

### 4. OCO Orders
- **Git Bash**
```bash
python src/advanced/oco.py <symbol> <quantity> <take_profit_price> <stop_loss_price>
python src/advanced/oco.py btcusdt 0.01 112980 111970
```
- **Windows PowerShell**
```powershell
python .\src\advanced\oco.py btcusdt 0.01 112980 111970
```

### 5. TWAP Orders
- **Git Bash**
```bash
python src/advanced/twap.py <symbol> <side> <quantity> <parts> <interval>
python src/advanced/twap.py btcusdt buy 0.5 5 10
```
- **Windows PowerShell**
```powershell
python .\src\advanced\twap.py btcusdt buy 0.5 5 10
```

---

## 📊 Example Outputs

### Limit Order
```bash
$ python src/limit_orders.py btcusdt sell 0.01 112831.2
Binance client connected. Server time: {...}
Input Values FOR LIMIT ORDER strategy symbol set to btcusdt side set to sell quantity set to 0.01 price set to 112831.2 
Limit order placed: {...}
```

### Market Order
```bash
$ python src/market_orders.py btcusdt sell 0.01
Binance client connected. Server time: {...}
Input Values FOR MARKET ORDER strategy symbol set to btcusdt side set to sell quantity set to 0.01 
Market order placed: {...}
```

### Stop-Limit Order
```bash
$ python src/advanced/stop_limit.py btcusdt 112920.0 113020.0 0.1 buy
Binance client connected. Server time: {...}
Input Values FOR STOP LIMIT ORDER strategy symbol set to BTCUSDT stop_price set to 112920.0 limit_price set to 113020.0 quantity set to 0.1 side set to BUY
STOP LIMIT ORDER EXECUTED with orderID: ...
```

### OCO Order
```bash
$ python src/advanced/oco.py btcusdt 0.01 112980 111970
Binance client connected. Server time: {...}
Limit order placed: {...}
Limit order placed: {...}
Placed TP ... and SL ...
```

### TWAP Order
```bash
$ python src/advanced/twap.py btcusdt sell 0.11 5 10
Binance client connected. Server time: {...}
Input Values FOR TWAP ORDER strategy symbol set to btcusdt side set to sell quantity set to 0.11 parts set to 5 interval set to 10 
Placing TWAP order: 5 slices, 10s interval
Market order placed: {...}
...
✅ All slices placed
```

---

## ⚠️ Notes

- This project is configured to work with the **Binance Testnet**.
- All logs are stored in **`app.log`**.
- All the screenshots are stored in **`ss`** folder
---

## 👨‍💻 Author

Developed by **Aryan Gupta** 🚀
Incase of a error please contact: +91 9991525380