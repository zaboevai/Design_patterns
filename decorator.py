from enum import StrEnum


class Size(StrEnum):
    S = 'S'
    M = 'M'
    L = 'L'


class Beverage:
    _desc = 'Unknown beverage'
    _size_prices: dict
    _size: Size = Size.M

    def __str__(self):
        return f'{self.get_desc():<30} Cost = {self.cost():<5} Size = {self.get_size():<4}'

    def cost(self):
        return self._size_prices.get(self.get_size())

    def get_desc(self):
        return self._desc

    def set_size(self, size: Size):
        self._size = size

    def get_size(self):
        return self._size


class Espresso(Beverage):
    _desc = 'Espresso'
    _size_prices = {Size.S: 1.5,
                    Size.M: 1.99,
                    Size.L: 2.5}

    def cost(self):
        return self._size_prices.get(self.get_size())


class HouseBlend(Beverage):
    _desc = 'House blend coffe'
    _size_prices = {Size.S: .69,
                    Size.M: .89,
                    Size.L: 1.09}


class DarkRoast(Beverage):
    _desc = 'Dark roast coffe'
    _size_prices = {Size.S: .59,
                    Size.M: .99,
                    Size.L: 1.19}


class NoCoffe(Beverage):
    _desc = 'No coffe'
    _size_prices = {Size.S: .75,
                    Size.M: 1.05,
                    Size.L: 1.35}


class CondimentDecorator(Beverage):
    _beverage: Beverage

    def __init__(self, beverage_: Beverage):
        self._beverage = beverage_

    def cost(self):
        raise NotImplementedError

    def get_desc(self):
        raise NotImplementedError

    def get_size(self):
        return self._beverage.get_size()


class Condiment(CondimentDecorator):

    @property
    def _name(self):
        raise NotImplementedError

    @property
    def _price(self):
        raise NotImplementedError

    def cost(self):
        return round(self._price + self._beverage.cost(), 2)

    def get_desc(self):
        return self._beverage.get_desc() + f', {self._name}'


class Mocha(Condiment):
    _name = 'Mocha'
    _price = .20


class Soy(Condiment):
    _name = 'Soy'
    _price = .15


class Whip(Condiment):
    _name = 'Whip'
    _price = .10


if __name__ == '__main__':
    coffe = Espresso()
    coffe.set_size(size=Size.S)
    beverage = Mocha(coffe)
    beverage = Mocha(beverage)
    beverage = Whip(beverage)
    print(beverage)

    coffe = DarkRoast()
    print(coffe)
    beverage = Soy(coffe)
    print(beverage)
    coffe.set_size(Size.L)
    print(coffe)
    coffe.set_size(Size.S)
    print(coffe)
