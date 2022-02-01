import requests
import re

from binance.client import Client
from binance.enums import *


# bin temp functions
class Binance_templates_function:
    def __init__(self, client):
        self.client = client

    def trade_quantity_counter(self, trade_size, symbol):
        coin_price = requests.get(f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}")
        coin_price = coin_price.json()['price']
        trade_quantity = trade_size / float(coin_price)

        lot_size = self.client.get_symbol_info(symbol)
        lot_size = lot_size["filters"]
        for i in lot_size:
            if i["filterType"] == "LOT_SIZE":
                lot_size = i["minQty"]

        lot_size = lot_size.split('.')[1]
        temp = re.findall(r"[1-9]*", lot_size)
        counter = 0
        for i in temp:
            if i == '':
                counter += 1
            else:
                break
        if counter != 0:
            counter -= 1

        return round(float(trade_quantity), counter)

    def change_leverage(self, symbol, leverage, **params):
        try:
            lev = self.client.futures_change_leverage(symbol=symbol, leverage=leverage)
            print(lev)
            return True
        except Exception as e:
            print(e)
            return False

    def order(self, symbol, quantity, side, order_type=ORDER_TYPE_MARKET):
        try:
            print("sending order")
            order = self.client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
            print(order)
            return True
        except Exception as e:
            print(e)
            return False

    def order_close(self, symbol, quantity, side, order_type=ORDER_TYPE_MARKET, reduceOnly=True):
        try:
            print("closing opened positions")
            order = self.client.futures_create_order(symbol=symbol, side=side, type=order_type, quantity=quantity,
                                                     reduceOnly=reduceOnly)
            print(order)
            return True
        except Exception as e:
            print(e)
            return False

    def get_open_orders(self, symbol):
        try:
            print("printing orders")
            order = self.client.futures_get_open_orders(symbol=symbol, limit=10)
            print(order)
            return True
        except Exception as e:
            print(e)
            return False

    def get_all_orders_closed(self, symbol, **params):
        try:
            print("cancelling open orders")
            close = self.client.futures_cancel_all_open_orders(symbol=symbol)
            print(close)
            return True
        except Exception as e:
            print(e)
            return False

    def limit_order(self, symbol, quantity, price, side):
        try:
            print("opening limit order")
            order = self.client.futures_create_order(symbol=symbol, quantity=quantity, side=side,
                                                     type=FUTURE_ORDER_TYPE_LIMIT,
                                                     price=price, timeInForce='GTC')
            return True
        except Exception as e:
            print(e)
            return False

    def get_order_size(self, symbol):
        try:
            order = self.client.futures_get_open_orders(symbol=symbol, limit=10)
            return order[0]['origQty']
        except Exception as e:
            print(e)
            return 0.0

    def open_position_check(self, symbol):
        try:
            position_information = self.client.futures_position_information(symbol=symbol)
            return float(position_information[0]['positionAmt'])
        except Exception as e:
            print(e)
            return 0.0