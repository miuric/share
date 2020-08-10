import re


class ExecuteWords:
    BUY = 'buy'
    SELL = 'sell'
    RE_CODE = re.compile(r'.*([0 3 6][0][0-9][0-9][0-9][0-9]).*')

    def __init__(self, do_word, do_code, do_price, do_amount):
        self.do_code = do_code
        self.do_word = do_word
        self.do_price = do_price
        self.do_amount = do_amount

    @classmethod
    def de_code_in_words(cls, words):
        match_code = cls.RE_CODE.match(words, re.I)

        if match_code:
            match_code = match_code.group(1)

        return match_code
