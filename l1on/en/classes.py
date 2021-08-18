from typing import List


class CSETicker(object):
    def __init__(
        self,
        updated_at: dict,
        metatdata: dict,
        quote: dict,
        depth_by_order: List[dict],
        depth_by_price: List[dict],
        ticker: dict,
        trades: List[dict],
    ):
        self.updated_at = updated_at
        self.metatdata = metatdata
        self.quote = quote
        self.depth_by_order = depth_by_order
        self.depth_by_price = depth_by_price
        self.ticker = ticker
        self.trades = trades


class CSESedarFilings(object):
    def __init__(self, categories: dict, list_items: List[dict]):
        self.categories = categories
        self.list_items = list_items
