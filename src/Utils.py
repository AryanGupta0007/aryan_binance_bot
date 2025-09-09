from ast import Raise
import os
import sys
import logging
from statistics import quantiles
from typing import Optional
from _pytest.main import validate_basetemp
from binance.client import Client
from dotenv import load_dotenv




# Configure logging
logging.basicConfig(
    filename="app.log",
    filemode="a",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

class BinanceUtils:
    def __init__(self, api_key: str, api_secret: str, testnet: bool = True):
        self.api_key = api_key
        self.api_secret = api_secret
        self.testnet = testnet
        self.client: Optional[Client] = None
        self.connect_client()

    def connect_client(self) -> None:
        """Initialize Binance client and test connectivity."""
        try:
            self.client = Client(self.api_key, self.api_secret, testnet=self.testnet)
            if self.testnet:
                self.client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
            # Check connectivity
            self.client.futures_ping()
            server_time = self.client.get_server_time()
            msg = f"Binance client connected. Server time: {server_time}"
            LogUtils.log_and_print_info(msg)
            
        except Exception as e:
            LogUtils.log_and_print_error(f"Error connecting to Binance: {e}")
            

    def fetch_symbol_price(self, symbol):
        try:
            ticker = self.client.futures_symbol_ticker(symbol=symbol)
            # print(f"ticker: {ticker}")
            msg = f"price for symbol {symbol} fetched"
            LogUtils.log_info(msg)
            return ticker["price"]
        except Exception as e:
            msg = f"error while fetching price for symbol {symbol}"
            LogUtils.log_and_print_error(msg)
            raise e
        
    
    def get_order_status(self, symbol:str, order_id:str) -> dict:
        """Get Order Status"""
        try:
            order_status = self.client.futures_get_order(
            symbol=symbol,
            orderId=order_id
            )
            LogUtils.log_info(f"order status for orderid {order_id} fetched: {order_status}")
            return order_status
        except Exception as e:
            msg = "Error fetching order status"
            self.log_error(msg)
            print(f"error: {e}")
            return {"error": e}
        
    
    def get_all_open_orders(self, symbol:str):
        try:
            open_orders = self.client.futures_get_open_orders(symbol=symbol)
            LogUtils.log_info(f"Open orders for {symbol} fetched")
            return open_orders
        except Exception as e:
            self.log_error(f"Error while fetching open orders for {symbol}")
            return         
        
    def cancel_order(self, symbol: str, order_id: int) -> dict:
        """Cancel an existing order."""
        try:
            response = self.client.futures_cancel_order(symbol=symbol, orderId=order_id)
            msg = f"Order canceled: {response}"
            LogUtils.log_and_print_info(msg)
            return response
        except Exception as e:
            self.log_error(f"Error canceling order: {e}")
            return {"error": e}


class LogUtils:
    # Logging methods
    @staticmethod
    def log_info(msg: str) -> None:
        logging.info(msg)

    @staticmethod
    def log_debug(msg: str) -> None:
        logging.debug(msg)

    @staticmethod
    def log_warning(msg: str) -> None:
        logging.warning(msg)

    @staticmethod
    def log_error(msg: str) -> None:
        logging.error(msg)

    @staticmethod
    def log_critical(msg: str) -> None:
        logging.critical(msg)
    
    @staticmethod
    def log_and_print_info(msg: str) -> None:
        logging.info(msg)
        print(msg)
    
    @staticmethod 
    def log_and_print_error(msg: str) -> Raise:
        logging.error(msg)
        print(msg)
        raise ValueError(msg)
    
    @staticmethod
    def log_and_validate_inputs(input_dict: dict, strategy: str) -> None:
        msg = f"Input Values FOR {strategy} strategy "
        for key, value in input_dict.items():
            msg += f"{key} set to {value} "
        LogUtils.log_and_print_info(msg)    
        Validation.validate(input_dict)
    
    @staticmethod
    def log_and_print_response(response_dict: dict, strategy: str) -> None:
        msg = f"Response Values FOR {strategy} strategy "
        for key, value in response_dict.items():
            msg += f"{key} is {value} "
        LogUtils.log_and_print_info(msg)
        
            

class Validation:
    @staticmethod
    def validate_symbol(symbol: str):
        if not symbol.isalpha():
            msg = f"EXITING DUE TO INVALID, Symbol {symbol}"
            LogUtils.log_and_print_error(msg)
            sys.exit(msg)
            
    @staticmethod
    def validate_quantity(quantity: str):
        min_amount = 0.001
        try:
            quantity = float(quantity)
        except:
            msg = f"EXITING DUE TO INVALID, Quantity {quantity}"
            LogUtils.log_and_print_error(msg)
            sys.exit(msg)
        else:
            if quantity < min_amount:
                msg = f"EXITING DUE TO INVALID, Quantity {quantity} can't be lesser than {min_amount}"
                LogUtils.log_and_print_error(msg)
                sys.exit(msg)
            

    @staticmethod
    def validate_side(side: str):
        if (not side.isalpha()) or (side.upper() not in ["SELL", "BUY"]) :
            msg = f"EXITING DUE TO INVALID SIDE {side}"
            LogUtils.log_and_print_error(msg)
            sys.exit(msg)
    
    @staticmethod 
    def validate_price(price_dict: dict):
        try: 
            price = float(list(price_dict.values())[0])
            key = list(price_dict.keys())[0]
        except:
            msg = f"EXITING DUE TO INVALID, {key} {price}"
            LogUtils.log_and_print_error(msg)
            sys.exit(msg)
        else:
            if price <= 0:
                LogUtils.log_and_print_error(f"{key} cannot be {price}") 

    def validate(input_dict):
        for key, value in input_dict.items():
            if key == "symbol":
                Validation.validate_symbol(value)
            elif key == "side":
                Validation.validate_side(value)
            elif key == "quantity":
                Validation.validate_quantity(value)
            elif key in ["stop_price", "limit_price", "price", "take_profit_price", "stop_loss_price"]:
                Validation.validate_price({key: value})
            
                
load_dotenv()
API_KEY = os.getenv("BINANCE_API_KEY")
API_SECRET = os.getenv("BINANCE_API_SECRET")

binance_utils = BinanceUtils(str(API_KEY), str(API_SECRET))

