import asyncio
import sys 
import os
from binance import AsyncClient, BinanceSocketManager

# Get the absolute path of the parent directory (aryan_binance_bot/)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from limit_orders import place_limit_order
from Utils import binance_utils, BinanceUtils, LogUtils

async def place_stop_limit_order(symbol, stop_price, limit_price, quantity, side):
    client = await AsyncClient.create(binance_utils.api_key, binance_utils.api_secret, testnet=True)

    try:
        order = await client.futures_create_order(
            symbol=symbol,
            side=side.upper(),              # BUY or SELL
            type="STOP",                    # STOP = stop-limit order
            quantity=quantity,
            price=str(limit_price),         # Limit price
            stopPrice=str(stop_price),      # Trigger price
            timeInForce="GTC"               # Good-Til-Cancelled
        )
        LogUtils.log_and_print_info(f"STOP LIMIT ORDER EXECUTED with orderID: {order['orderId']}")
    except Exception as e:
        LogUtils.log_and_print_error(f"Error placing stop-limit order: {e}")
    finally:
        await client.close_connection()


if __name__ == "__main__":
    args = sys.argv[1:]
    input_dict = {
        "symbol": args[0].upper(),
        "stop_price": float(args[1]),
        "limit_price": float(args[2]),
        "quantity": float(args[3]),
        "side": args[4].upper()
    }
    LogUtils.log_and_validate_inputs(input_dict, "STOP LIMIT ORDER")

    asyncio.run(
        place_stop_limit_order(
            input_dict["symbol"],
            input_dict["stop_price"],
            input_dict["limit_price"],
            input_dict["quantity"],
            input_dict["side"]
        )
    )
