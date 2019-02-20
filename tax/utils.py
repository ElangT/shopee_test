from tax.models import TAX_CODE
import abc


def count_tax_food(price):
    return price*0.1


def count_tax_tobacco(price):
    return 10+(price*0.02)


def count_tax_entertainment(price):
    if(price < 100 and price > 0):
        return 0
    else:
        return (price-100)*0.01


TAX_PRICE = {
    1: count_tax_food,
    2: count_tax_tobacco,
    3: count_tax_entertainment,
}

TAX_REFUNDABLE = {
    1: True,
    2: False,
    3: False
}


class TaxHandler:

    def __init__(self, tax_code, price):
        self.price = price
        self.tax_code = tax_code
        self.tax_strategy = TAX_PRICE[tax_code]

    def count_tax(self):
        return self.tax_strategy(self.price)

    def is_refundable(self):
        return TAX_REFUNDABLE[self.tax_code]

    def tax_type(self):
        return TAX_CODE[self.tax_code]

    def count_amount(self):
        return self.price + self.count_tax()
