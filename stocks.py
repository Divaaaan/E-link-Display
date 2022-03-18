from openapi_client import openapi


class stoke():
    def __init__(self, average_position_price, balance, expected_yield, instrument_type, lots, name, ticker):
        self.average_position_price = average_position_price
        self.balance = balance
        self.expected_yield = expected_yield
        self.instrument_type = instrument_type
        self.lots = lots
        self.name = name
        self.ticker = ticker

    def get_name(self):
        return self.name

    def get_price(self):
        return self.average_position_price.value, self.average_position_price.currency

    def get_balance(self):
        return self.balance

    def get_instrument_type(self):
        return self.instrument_type

    def get_expected_yield(self):
        return self.expected_yield.value, self.expected_yield.currency

    def get_lost(self):
        return self.lots  # не думаю что понадобистя

    def get_ticker(self):
        return self.ticker


class portfolio():
    def __init__(self,
                 token=''):
        client = openapi.api_client(token)
        pf = client.portfolio.portfolio_get()
        self.token = token
        self.my_portfolio = []
        for i in pf.payload.positions:
            self.my_portfolio.append(stoke(i.average_position_price,
                                           i.balance,
                                           i.expected_yield,
                                           i.instrument_type,
                                           i.lots,
                                           i.name,
                                           i.ticker))
            # self.my_portfolio.append(stoke(pf.payload.positions[i].average_position_price,
            #                                pf.payload.positions[i].balance,
            #                                pf.payload.positions[i].expected_yield,
            #                                pf.payload.positions[i].instrument_type,
            #                                pf.payload.positions[i].lots,
            #                                pf.payload.positions[i].name,
            #                                pf.payload.positions[i].ticker))

    def get_list(self):
        return self.my_portfolio

for i in portfolio().get_list():
    print(i.name)
