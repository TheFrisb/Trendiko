class StockValidator:
    def check_stock_item_stock(self, stock_item, quantity):
        return stock_item.stock >= quantity
