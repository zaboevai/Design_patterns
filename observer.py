from abc import abstractmethod, ABC


class WeatherDataSubject:
    temp: int
    humidity: str
    observers: list = []
    is_changed: bool = False

    def set_observers(self, observer):
        self.observers.append(observer)

    def update(self):
        if self.is_changed:
            for observer in self.observers:
                observer.update()  # data={'TEMP':self.temp, 'HUMIDITY':self.humidity})
        self.is_changed = False

    def set_changed(self):
        self.is_changed = True
        self.update()

    def set_weather_data(self, temp, humidity):
        self.temp = temp
        self.humidity = humidity

    def get_temp(self):
        return self.temp

    def get_humidity(self):
        return self.humidity

    def remove_observer(self, observer):
        self.observers.remove(observer)


class Display(ABC):

    @abstractmethod
    def show(self):
        pass


class Observer(ABC):
    subject: WeatherDataSubject

    def __init__(self, subject):
        self.subject = subject
        self.subject.set_observers(self)

    @abstractmethod
    def update(self, data=None):
        pass


class WeatherDataDisplay(Observer, Display):
    temp: int
    humidity: str

    def update(self, data=None):
        if data:
            self.temp = data['TEMP']
            self.humidity = data['HUMIDITY']
        else:
            self.temp = self.subject.get_temp()
            self.humidity = self.subject.get_humidity()
        self.show()

    def show(self):
        pass


class ScreenDisplay(WeatherDataDisplay):

    def show(self):
        print(f'Weather data: {self.temp} {self.humidity}')


class ScreenAvgDisplay(WeatherDataDisplay):

    def show(self):
        print(f'Weather AVG data: {self.temp} {self.humidity}')


weather_data = WeatherDataSubject()
weather_data.set_weather_data(temp=123, humidity='25%')

ob1 = ScreenDisplay(weather_data)
ob2 = ScreenAvgDisplay(weather_data)

# weather_data.remove_observer(ob2)

weather_data.set_changed()
