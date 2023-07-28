from abc import ABC
from enum import Enum


class IngredientFactory(ABC):

    def create_sauce(self):
        raise NotImplementedError()

    def create_cheese(self):
        raise NotImplementedError()


class Pizza(ABC):
    ingredient_factory: IngredientFactory
    sauce: str
    cheese: str
    _name: str

    def __init__(self, ingredient_factory=None):
        self.ingredient_factory = ingredient_factory

    @property
    def name(self):
        return f'{self._name!r}'

    def prepare(self):
        if not self.ingredient_factory:
            raise ValueError('Set ingredient_factory')

        self.sauce = self.ingredient_factory.create_sauce()
        self.cheese = self.ingredient_factory.create_cheese()

    def bake(self):
        print(f'bake {self.name}')

    def cut(self):
        print(f'cut {self.name} at 8 pieces')

    def box(self):
        print(f'boxing {self.name} firm box')

    def __str__(self):
        return f'{self.name} + {self.sauce} + {self.cheese}'


class PizzaStore(ABC):
    @property
    def menu(self) -> Enum:
        raise NotImplementedError()

    def create_pizza(self, name) -> Pizza:
        raise NotImplementedError()

    def order(self, name):
        pizza = self.create_pizza(name)
        pizza.prepare()
        print(f'Pizza {pizza} - READY')
        pizza.bake()
        pizza.cut()
        pizza.box()
