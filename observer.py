import asyncio
from abc import abstractmethod, ABC


class ObserverInterface(ABC):
    _subject: 'WeatherStation' = None

    def __init__(self, subject):
        self._subject = subject
        self._subject.set_observers(self)

    @abstractmethod
    def update(self, data: dict = None):
        ...


class WeatherDataSubjectInterface(ABC):

    @abstractmethod
    def set_observers(self, observer):
        ...

    @abstractmethod
    def remove_observer(self, observer):
        ...

    @abstractmethod
    def notify_observers(self, data):
        """ data = {'TEMP': {}, 'HUMIDITY': {}}"""


class WeatherStation(WeatherDataSubjectInterface):
    temp: int = 0
    humidity: int = 0
    observers: list[ObserverInterface] = list()
    is_changed: bool = False

    def set_observers(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self, data: dict = None):
        if data:
            self.set_weather_data(temp=data['TEMP'], humidity=data['HUMIDITY'])
        if self.is_changed:
            for observer in self.observers:
                observer.update(data=data)
        self.is_changed = False

    def set_changed(self):
        self.is_changed = True

    def set_weather_data(self, temp, humidity):
        if not self.cur_weather or self.is_different_weather(temp, humidity):
            self.temp = temp
            self.humidity = humidity

    def get_temp(self):
        return self.temp

    def get_humidity(self):
        return self.humidity

    @property
    def cur_weather(self):
        if temp := self.get_temp():
            return temp, self.get_humidity()

    def is_different_weather(self, temp, humidity):
        new_weather = (temp, humidity)
        return self.cur_weather != new_weather


class DisplayInterface(ABC):

    @abstractmethod
    def show(self):
        pass


class CurrentDisplay(ObserverInterface, DisplayInterface):
    temp: int
    humidity: int

    def update(self, data=None):
        if data:
            self.temp = data['TEMP']
            self.humidity = data['HUMIDITY']
        else:
            self.temp = self._subject.get_temp()
            self.humidity = self._subject.get_humidity()
        self.show()

    def show(self):
        print(f'{self.temp} {self.humidity}')


class StatisticDisplay(ObserverInterface, DisplayInterface):
    cur_temp: int
    cur_humidity: int
    temps: list[int] = list()
    humiditys: list[int] = list()

    def update(self, data=None):
        if data:
            self.cur_temp = data['TEMP']
            self.cur_humidity = data['HUMIDITY']
        else:
            if self._subject:
                self.cur_temp = self._subject.get_temp()
                self.cur_humidity = self._subject.get_humidity()
        self.temps.append(self.cur_temp)
        self.humiditys.append(self.cur_humidity)
        self.show()

    def max_temp(self):
        return max(self.temps)

    def min_temp(self):
        return min(self.temps)

    def avg_temp(self):
        return sum(self.temps) / len(self.temps)

    def max_humidity(self):
        return max(self.humiditys)

    def min_humidity(self):
        return min(self.humiditys)

    def avg_humidity(self):
        return sum(self.humiditys) / len(self.humiditys)

    def avg_temps(self):
        return f'{self.min_temp()}/{self.avg_temp():.0f}/{self.max_temp()}'

    def avg_humiditys(self):
        return f'{self.min_humidity()}/{self.avg_humidity():.0f}/{self.max_humidity()}'

    def show(self):
        print(f'{self.cur_temp} {self.cur_humidity}')


class ScreenDisplay(CurrentDisplay):

    def show(self):
        print(f'Weather: {"+" if self.temp > 0 else ""}{self.temp}, humidity={self.humidity}%')


class RusScreenDisplay(CurrentDisplay):

    def show(self):
        print(f'Погода: {"+" if self.temp > 0 else ""}{self.temp}, humidity={self.humidity}%')


class ScreenAvgDisplay(StatisticDisplay):

    def show(self):
        print(f'Weather AVG: {self.avg_temps()} {self.avg_humiditys()}')


def add_observers(weather_station_):
    observers_ = list()
    observers_.append(ScreenDisplay(weather_station_))
    observers_.append(RusScreenDisplay(weather_station_))
    observers_.append(ScreenAvgDisplay(weather_station_))
    return observers_


async def update(weather_station__, num=10, interval=1):
    for _ in range(num):
        await asyncio.sleep(interval)
        weather_station__.notify_observers()
        print('Update: OK')


async def update_weather(weather_station_):
    tasks = list()
    task = asyncio.create_task(update(weather_station_))
    tasks.append(task)

    await asyncio.sleep(3)
    weather_station_.set_changed()
    weather_station_.notify_observers(data={'TEMP': 15, 'HUMIDITY': 25})

    await asyncio.sleep(3)
    weather_station_.set_changed()

    await asyncio.sleep(3)
    weather_station_.set_changed()
    weather_station_.set_weather_data(temp=25, humidity=65)

    await asyncio.wait(tasks)


if __name__ == '__main__':
    weather_station = WeatherStation()
    observers = add_observers(weather_station)
    asyncio.run(update_weather(weather_station))
