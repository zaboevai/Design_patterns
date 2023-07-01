class Beverage:
    desc = 'Unknown beverage'

    def cost(self):
        raise NotImplementedError

    def get_desc(self):
        return self.desc


class CondimentDecorator(Beverage):

    def cost(self):
        raise NotImplementedError

    def get_desc(self):
        raise NotImplementedError


class Espresso(Beverage):
    desc = 'Espresso'

    def cost(self):
        return 1.99


class HouseBlend(Beverage):
    desc = 'House blend coffe'

    def cost(self):
        return .89


class DarkRoast(Beverage):
    desc = 'Dark roast coffe'

    def cost(self):
        return .99


class NoCoffe(Beverage):
    desc = 'No coffe'

    def cost(self):
        return 1.05


class Condiment(CondimentDecorator):

    def __init__(self, beverage: Beverage):
        self.beverage = beverage

    @property
    def name(self):
        raise NotImplementedError

    @property
    def price(self):
        raise NotImplementedError

    def cost(self):
        return round(self.price + self.beverage.cost(), 2)

    def get_desc(self):
        return self.beverage.get_desc() + f', {self.name}'


class Mocha(Condiment):
    name = 'Mocha'
    price = .20


class Soy(Condiment):
    name = 'Soy'
    price = .15


class Whip(Condiment):
    name = 'Whip'
    price = .10


coffe = HouseBlend()
beverage = Mocha(coffe)
beverage = Mocha(beverage)
beverage = Whip(beverage)
print(beverage.get_desc() + '. Cost =', beverage.cost())

coffe = DarkRoast()
beverage = Soy(coffe)
beverage = Whip(beverage)
beverage = Mocha(beverage)
print(beverage.get_desc() + '. Cost =', beverage.cost())
