from abc import ABC, abstractmethod


class FlyBeghavior(ABC):

    @abstractmethod
    def fly(self):
        pass


class FlyLikeDuck(FlyBeghavior):

    def fly(self):
        print('fly like duck')


class FlyLikeAirCraft(FlyBeghavior):

    def fly(self):
        print('fly like AirCraft')


class QuackBeghavior(ABC):

    @abstractmethod
    def quack(self):
        pass


class QuackLikeDuck(QuackBeghavior):

    def quack(self):
        print('quack like duck')


class Duck(ABC):
    fly_behavior: FlyBeghavior
    quack_behavior: QuackBeghavior

    def perform_fly(self):
        self.fly_behavior.fly()

    def perform_quack(self):
        self.quack_behavior.quack()


class MallardDuck(Duck):
    fly_behavior = FlyLikeDuck()
    quack_behavior = QuackLikeDuck()


duck = MallardDuck()

duck.perform_quack()

duck.fly_behavior = FlyLikeAirCraft()
duck.perform_fly()
