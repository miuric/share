from config import south_base_host
from model.south.order import Order
from request_api.helper import Api


class SouthApi(Api):
    base_host = south_base_host
    base_path = "/api/v1.0"


class OrderApi(SouthApi):
    api = "/orders"

    async def trade(self, action: str, code: str, price: float, amount: int, price_type=0, type='LIMIT'):
        order = Order(symbol=code, action=action, price=price, amount=amount, price_type=price_type, type=type)

        c, r, h = await self.post(order)

        return c, r, h

    async def buy(self, code: str, price: float, amount: int, price_type=0, type='LIMIT'):
        return await self.trade(action='BUY', code=code, price=price, amount=amount, price_type=price_type, type=type)

    async def sell(self, code: str, price: float, amount: int, price_type=0, type='LIMIT'):
        return await self.trade(action='SELL', code=code, price=price, amount=amount, price_type=price_type, type=type)
