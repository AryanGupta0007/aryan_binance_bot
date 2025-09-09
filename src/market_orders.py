import sys 
from Utils import BinanceUtils, LogUtils, Validation, binance_utils 

def place_market_order(obj, symbol: str, side: str, quantity: float) -> dict:
        """Place a market order."""
        try:
            response = obj.client.futures_create_order(
                symbol=symbol,
                side=side,
                type="MARKET",
                quantity=quantity
            )
            
            order_status = obj.get_order_status(symbol, response['orderId'])
            # print(order_status)
            for field in ["avgPrice", "executedQty", "status"]:
                response[field] = order_status[field]
            
            msg = f"Market order placed: {response}"
            LogUtils.log_and_print_info(msg)
            return response
        except Exception as e:
            LogUtils.log_and_print_error(f"Error placing market order: {e}")
            return {"error": e}

if __name__ == "__main__":
    args = sys.argv[1:]
    input_dict = {
        "symbol": args[0],
        "side": args[1],
        "quantity": args[2]
    }
    LogUtils.log_and_validate_inputs(input_dict, "MARKET ORDER")
    place_market_order(binance_utils, symbol=input_dict["symbol"].upper(), side=input_dict["side"].upper(), quantity=float(input_dict["quantity"]))
