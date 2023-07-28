from enum import StrEnum

from fabric.interface import PizzaStore, Pizza, IngredientFactory
from fabric.pizza import MoscowCheesePizza, SaintPetersburgCheesePizza, \
    MoscowCheesePizzaLikeItalian


class RussiaIngredientFactory(IngredientFactory):

    def create_sauce(self):
        return 'rus national sauce'

    def create_cheese(self):
        return 'rus national cheese'


class ItalianIngredientFactory(IngredientFactory):

    def create_sauce(self):
        return 'italian national sauce'

    def create_cheese(self):
        return 'italian national cheese'


class MoscowPizzaStore(PizzaStore):
    ingredient_factory = RussiaIngredientFactory()
    italian_ingredient_factory = ItalianIngredientFactory()

    class Menu(StrEnum):
        cheese_pizza = MoscowCheesePizza().name
        italian_cheese_pizza = MoscowCheesePizzaLikeItalian().name

    @property
    def menu(self) -> type(Menu):
        return self.Menu

    @property
    def pizzas(self):
        _pizzas = [
            MoscowCheesePizza(self.ingredient_factory),
            MoscowCheesePizzaLikeItalian(self.italian_ingredient_factory),
        ]
        return {pizza.name: pizza for pizza in _pizzas}

    def create_pizza(self, name: str) -> Pizza:
        pizza = self.pizzas[name]
        print(f'COOKING Moscow pizza - {pizza.name}')
        return pizza


class SaintPetersburgPizzaStore(PizzaStore):
    ingredient_factory = RussiaIngredientFactory()

    class Menu(StrEnum):
        cheese_pizza = SaintPetersburgCheesePizza().name

    @property
    def menu(self) -> type(Menu):
        return self.Menu

    @property
    def pizzas(self):
        _pizzas = [
            SaintPetersburgCheesePizza(self.ingredient_factory),
        ]
        return {pizza.name: pizza for pizza in _pizzas}

    def create_pizza(self, name) -> Pizza:
        pizza = self.pizzas[name]
        print(f'COOKING Piter pizza - {pizza.name}')
        return pizza
