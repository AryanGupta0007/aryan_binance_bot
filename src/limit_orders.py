import sys 
from Utils import LogUtils, binance_utils, BinanceUtils


        
def place_limit_order(obj, symbol: str, side: str, quantity: float, price: float, show=True) -> dict:
    """Place a limit order."""
    try:
        response = obj.client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            timeInForce="GTC",
            quantity=quantity,
            price=price
        )
        msg = f"Limit order placed: {response}"
        LogUtils.log_and_print_info(msg)
        return response
    except Exception as e:
        # print(f"error: {e}")
        LogUtils.log_and_print_error(f"Error placing limit order: {e}")
        return {"error": e}

if __name__ == "__main__":
    args = sys.argv[1:]
    input_dict = {
        "symbol": args[0],
        "side": args[1],
        "quantity": args[2],
        "price": args[3],
    }
    LogUtils.log_and_validate_inputs(input_dict, "LIMIT ORDER")
    place_limit_order(binance_utils, symbol=input_dict["symbol"].upper(), side=input_dict["side"].upper(), quantity=float(input_dict["quantity"]), price=float(input_dict["price"]))
