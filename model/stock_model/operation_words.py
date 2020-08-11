class ExecuteWords:
    BUY = 'buy'
    SELL = 'sell'

    def __init__(self, do_word, do_code, do_price, do_amount):
        self.do_code = do_code
        self.do_word = do_word
        self.do_price = do_price
        self.do_amount = do_amount
