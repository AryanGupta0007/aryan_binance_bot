import asyncio
from binance import AsyncClient
import os
import sys
# Add parent dir
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from Utils import binance_utils, BinanceUtils, LogUtils
from limit_orders import place_limit_order

async def place_oco_order(symbol, quantity, tp_price, sl_price):
    client = await AsyncClient.create(binance_utils.api_key, binance_utils.api_secret)
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"

    
    # 1️⃣ Place TP order
    tp_order = place_limit_order(
        obj=binance_utils, symbol=symbol, side="SELL", quantity=quantity, price=tp_price, show=False
    )
    if "error" in tp_order:
        raise Exception("Error placing TP order")

    # 2️⃣ Place SL order
    sl_order = place_limit_order(
        obj=binance_utils, symbol=symbol, side="SELL", quantity=quantity, price=sl_price, show=False
    )
    if "error" in sl_order:
        await client.futures_cancel_order(symbol=symbol, orderId=tp_order["orderId"])
        raise Exception("Error placing SL order")

    print(f"Placed TP {tp_order['orderId']} and SL {sl_order['orderId']}")

    # 3️⃣ Poll status every second
    while True:
        tp_status = (await client.futures_get_order(symbol=symbol, orderId=tp_order["orderId"]))["status"]
        sl_status = (await client.futures_get_order(symbol=symbol, orderId=sl_order["orderId"]))["status"]

        if tp_status == "FILLED":
            await client.futures_cancel_order(symbol=symbol, orderId=sl_order["orderId"])
            msg = f"✅ TP filled, SL canceled"
            LogUtils.log_and_print_info(msg)
            break
        elif sl_status == "FILLED":
            await client.futures_cancel_order(symbol=symbol, orderId=tp_order["orderId"])
            msg = f"❌ SL filled, TP canceled"
            LogUtils.log_and_print_info(msg)

            break

        await asyncio.sleep(1)  # avoid rate limits

    await client.close_connection()


if __name__ == "__main__":
    args = sys.argv[1:]
    input_dict = {
    "symbol": args[0],
    "quantity": args[1],
    "take_profit_price": args[2],
    "stop_loss_price": args[3]
    }
    
    asyncio.run(place_oco_order(input_dict["symbol"].upper(), float(input_dict["quantity"]), float(input_dict["take_profit_price"]), float(input_dict["stop_loss_price"])))
