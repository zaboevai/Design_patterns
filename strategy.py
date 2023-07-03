from abc import ABC, abstractmethod


class FlyBehavior(ABC):

    @abstractmethod
    def fly(self):
        pass


class FlyLikeDuck(FlyBehavior):

    def fly(self):
        print('fly like duck')


class FlyLikeAirCraft(FlyBehavior):

    def fly(self):
        print('fly like AirCraft')


class QuackBehavior(ABC):

    @abstractmethod
    def quack(self):
        pass


class QuackLikeDuck(QuackBehavior):

    def quack(self):
        print('quack like duck')


class Duck(ABC):
    fly_behavior: FlyBehavior
    quack_behavior: QuackBehavior

    def perform_fly(self):
        self.fly_behavior.fly()

    def perform_quack(self):
        self.quack_behavior.quack()


class MallardDuck(Duck):
    fly_behavior = FlyLikeDuck()
    quack_behavior = QuackLikeDuck()


if __name__ == '__main__':
    duck = MallardDuck()

    duck.perform_quack()

    duck.fly_behavior = FlyLikeAirCraft()
    duck.perform_fly()
