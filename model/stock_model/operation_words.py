class ExecuteWords:
    BUY = 'buy'
    SELL = 'sell'

    def __repr__(self):
        attrs = []

        for attr in self.attrs():
            if attr is None:
                attr = '无法解析'
            attrs.append(attr)

        return '{},{},{},{}'.format(*attrs)

    def attrs(self):
        return self.do_code, self.do_word, self.do_price, self.do_amount

    def __init__(self, do_word, do_code, do_price, do_amount):
        self.do_code = do_code
        self.do_word = do_word
        self.do_price = do_price
        self.do_amount = do_amount

    def is_success(self):
        return None not in self.attrs()
