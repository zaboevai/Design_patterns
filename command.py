"""
Есть пульт для устройств, где есть 2 кнопки для каждого устройства on\off.
Требуется реализовать интерфейс для пульта с возможностью добавления устройств
"""
import queue
from abc import ABC
from typing import Callable


class CommandInterface:

    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def undo(self):
        raise NotImplementedError

    def __str__(self):
        return f'{self.__class__.__name__}'


class BaseCommand(CommandInterface, ABC):
    def __init__(self, device: 'DeviceInterface' = None):
        self.device = device


class NoCommand(CommandInterface):
    def __call__(self, *args, **kwargs):
        pass

    def undo(self):
        pass


class DeviceInterface:
    def __init__(self, location):
        self.location = location

    def __str__(self):
        return f'{self.location} {self.__class__.__name__}'

    def on(self):
        print(f'{self} is on.')

    def off(self):
        print(f'{self} is off.')


class Light(DeviceInterface):
    ...


class LightOnCommand(BaseCommand):

    def __call__(self, *args, **kwargs):
        self.device.on()

    def undo(self):
        self.device.off()


class LightOffCommand(BaseCommand):

    def __call__(self, *args, **kwargs):
        self.device.off()

    def undo(self):
        self.device.on()


class CeilingFan(DeviceInterface):
    HIGH = 3
    MEDIUM = 2
    LOW = 1
    OFF = 0
    speed: int
    location: str

    def __init__(self, location):
        super().__init__(location)
        self.speed = self.OFF

    def high(self):
        self.speed = self.HIGH
        print(f'{self.location} {self.__class__.__name__} speed is high.')

    def medium(self):
        self.speed = self.MEDIUM
        print(f'{self.location} {self.__class__.__name__} speed is medium.')

    def low(self):
        self.speed = self.LOW
        print(f'{self.location} {self.__class__.__name__} speed is low.')

    def off(self):
        self.speed = self.OFF
        print(f'{self.location} {self.__class__.__name__} speed is off.')

    def get_speed(self):
        return self.speed


class BaseCeilingFanCommand(CommandInterface):
    prev_speed: int

    def __init__(self, device: 'CeilingFan' = None):
        super().__init__()
        self.device = device

    def __call__(self, *args, **kwargs):
        self.prev_speed = self.device.get_speed()

    def undo(self):
        match self.prev_speed:
            case self.device.HIGH:
                self.device.high()
            case self.device.MEDIUM:
                self.device.medium()
            case self.device.LOW:
                self.device.low()
            case self.device.OFF:
                self.device.off()


class CeilingFanHighCommand(BaseCeilingFanCommand):

    def __call__(self, *args, **kwargs):
        super().__call__()
        self.device.high()


class CeilingFanMediumCommand(BaseCeilingFanCommand):

    def __call__(self, *args, **kwargs):
        super().__call__()
        self.device.medium()


class CeilingFanLowCommand(BaseCeilingFanCommand):

    def __call__(self, *args, **kwargs):
        super().__call__()
        self.device.low()


class CeilingFanOffCommand(BaseCeilingFanCommand):
    def __call__(self, *args, **kwargs):
        super().__call__()
        self.device.off()


class MacroCommand(CommandInterface):
    commands: list[CommandInterface]

    def __init__(self, commands):
        self.commands = commands

    def __call__(self, *args, **kwargs):
        for c in self.commands:
            c()

    def undo(self):
        pass


class Stereo(DeviceInterface):
    def play(self):
        print(f'{self.location} is play.')

    def stop(self):
        print(f'{self.location} is stop.')

    def next(self):
        print(f'{self.location} is next.')

    def prev(self):
        print(f'{self.location} is prev.')


class StereoOnCommand(BaseCommand):

    def __call__(self, *args, **kwargs):
        self.device.on()

    def undo(self):
        self.device.off()


class StereoOffCommand(BaseCommand):

    def __call__(self, *args, **kwargs):
        self.device.off()

    def undo(self):
        self.device.on()


class RemoteControl:
    _slots_count = 6
    _on_commands: dict[int, CommandInterface] = {}
    _off_commands: dict[int, CommandInterface] = {}
    undo_queue = queue.LifoQueue()

    def __init__(self):
        for slot in range(self._slots_count):
            self._on_commands[slot] = NoCommand()
            self._off_commands[slot] = NoCommand()
        self.undo_queue.put(NoCommand())
        self.is_undo_set = False

    def set_command(self, slot: int, on_command: CommandInterface | Callable, off_command: CommandInterface | Callable):
        if slot > self._slots_count:
            print('Cannot set command in slot {slot}. All slots busy.')
            return

        self._on_commands[slot] = on_command
        self._off_commands[slot] = off_command

    def push_on_button(self, slot):
        self._on_commands[slot]()
        self.undo_queue.put(self._on_commands[slot])
        self.is_undo_set = False

    def push_off_button(self, slot):
        self._off_commands[slot]()
        self.undo_queue.put(self._off_commands[slot])
        self.is_undo_set = False

    def push_undo_button(self):
        if not self.is_undo_set:
            self.undo_queue.get()
        self.undo_queue.get()()
        self.is_undo_set = True

    def __str__(self):
        for slot in range(self._slots_count):
            print(f'slot {slot:<2} {str(self._on_commands[slot]):>25}  {str(self._off_commands[slot]):<25}')
        print(f'{"Undo":<7} {str(self.undo_queue.queue):>25}')
        return ''


class RemoteControlLoader:

    def __init__(self, remote_control_: RemoteControl):
        self.remote_control = remote_control_

    def load(self):
        kitchen_light = Light(location='Kitchen')

        ceiling_fan = CeilingFan(location='Room')
        ceiling_fan_high_command = CeilingFanHighCommand(device=ceiling_fan)
        ceiling_fan_medium_command = CeilingFanMediumCommand(device=ceiling_fan)
        ceiling_fan_low_command = CeilingFanLowCommand(device=ceiling_fan)
        ceiling_fan_off_command = CeilingFanOffCommand(device=ceiling_fan)

        stereo = Stereo(location='Room')

        commands_on = [kitchen_light.on, ceiling_fan_medium_command, stereo.on]
        commands_off = [kitchen_light.off, ceiling_fan_off_command, stereo.off]
        macro_on_commands = MacroCommand(commands_on)
        macro_off_commands = MacroCommand(commands_off)

        self.remote_control.set_command(0, kitchen_light.on, kitchen_light.off)
        self.remote_control.set_command(1, stereo.on, stereo.off)
        self.remote_control.set_command(2, ceiling_fan_low_command, ceiling_fan_off_command)
        self.remote_control.set_command(3, ceiling_fan_medium_command, ceiling_fan_off_command)
        self.remote_control.set_command(4, ceiling_fan_high_command, ceiling_fan_off_command)
        self.remote_control.set_command(5, macro_on_commands, macro_off_commands)

        print(self)

    def __str__(self):
        print(self.remote_control)
        return ''


if __name__ == '__main__':
    remote_control = RemoteControl()
    r = RemoteControlLoader(remote_control_=remote_control)
    r.load()

    print('--- Kitchen light ---')
    remote_control.push_on_button(0)
    remote_control.push_off_button(0)
    print('-- set undo --')
    remote_control.push_undo_button()
    print('--')

    print('--- Room stereo  ---')
    remote_control.push_on_button(1)
    remote_control.push_off_button(1)
    print('-- set undo --')
    remote_control.push_undo_button()
    print('--')
    remote_control.push_off_button(1)

    print('--- Room ceiling fan  ---')
    remote_control.push_on_button(2)
    remote_control.push_on_button(3)
    remote_control.push_on_button(4)
    print('-- set undo --')
    remote_control.push_undo_button()
    print('-- set undo --')
    remote_control.push_undo_button()
    print('-- set undo --')
    remote_control.push_undo_button()
    print('--')
    remote_control.push_on_button(4)
    remote_control.push_off_button(4)

    print('--- START PARTY ---')
    remote_control.push_on_button(5)
    print('--- END PARTY ---')
    remote_control.push_off_button(5)
