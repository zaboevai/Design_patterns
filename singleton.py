class Singleton:
    __instance = None

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls, *args, **kwargs)
        if not cls.__instance:
            cls.__instance = instance
        return cls.__instance


class SingletonMeta(type):
    __instance = None

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        if not cls.__instance:
            cls.__instance = instance
        return cls.__instance


def test_singleton(cls):
    instance = cls()
    instance_1 = cls()

    instance_2 = cls()
    instance_2.b = 3

    assert id(instance) == id(instance_1)
    assert instance is instance_1
    assert instance.b == instance_2.b
    assert instance.a == instance_2.a


if __name__ == '__main__':
    class A(metaclass=SingletonMeta):
        a = 1
        b = 2


    class B(Singleton):
        a = 1
        b = 2


    test_singleton(A)
    test_singleton(B)
