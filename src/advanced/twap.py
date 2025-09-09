import asyncio
import sys 
import os
from binance import AsyncClient, BinanceSocketManager

# Get the absolute path of the parent directory (aryan_binance_bot/)
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(parent_dir)

from Utils import LogUtils, binance_utils, BinanceUtils
from market_orders import place_market_order

async def place_twap_order(obj, interval, parts, symbol, total_quantity, side):
    msg = f"Placing TWAP order: {parts} slices, {interval}s interval"
    LogUtils.log_and_print_info(msg)

    slice_quantity = float(total_quantity) / float(parts)
    if (slice_quantity < 0.001):
        msg = f"❌ Exception placing order as slice order can't be lesser than 0.001"
        LogUtils.log_and_print_error(msg)

    parts = int(parts)
    for i in range(parts):
        msg2 = f"Placing slice {i + 1} of {parts} for {slice_quantity} {symbol}"
        LogUtils.log_and_print_info(msg2)

        try:
            order =  place_market_order(
                obj=obj,
                symbol=symbol,
                side=side,
                quantity=slice_quantity
            )
            if "orderId" in order:
                LogUtils.log_and_print_info(f"✅ Order {order['orderId']} placed for slice {i + 1}")
            else:
                print(f"⚠️ Failed to place order slice {i + 1}: {order}")
        except Exception as e:
            msg = f"❌ Exception placing slice {i + 1}: {str(e)}"
            LogUtils.log_and_print_error(msg)

        if i < parts - 1:
            await asyncio.sleep(interval)

if __name__ == "__main__":
    args = sys.argv[1:]
    input_dict = {
        "symbol": args[0],
        "side": args[1],
        "quantity": args[2],
        "parts": args[3],
        "interval": args[4]
    }
    LogUtils.log_and_validate_inputs(input_dict, "TWAP ORDER")
    if ( (not input_dict["parts"].isnumeric()) or (not input_dict["interval"].isnumeric()) or int(input_dict["parts"]) <= 0 or int(input_dict["interval"]) <= 0):
        LogUtils.log_and_print_error("TWAP Failed! Either Parts or interval were not numeric or set below 0 ")
    asyncio.run(place_twap_order(binance_utils, symbol=input_dict["symbol"].upper(), interval=int(input_dict["interval"]), parts=int(input_dict["parts"]), total_quantity=float(input_dict["quantity"]), side=input_dict["side"].upper()))
    
    