"""
--- Day 20: Pulse Propagation ---
https://adventofcode.com/2023/day/20
"""
from collections import deque
from typing import List

from utils.test_and_run import run, test


class ModuleRegistry:
    _registry = {}

    @classmethod
    def register(cls, prefix, module_cls):
        cls._registry[prefix] = module_cls

    @classmethod
    def get_module_class(cls, prefix) -> "Module":
        return cls._registry[prefix]


class Modules:
    _name2module = {}

    @classmethod
    def register(cls, name, model):
        if name not in cls._name2module:
            # m = self._name2module[name]

            cls._name2module[name] = model
            return

        a = 0

    @classmethod
    def get(cls, name) -> "Module":
        return cls._name2module[name]

def register_module(cls):
    ModuleRegistry.register(cls.prefix, cls)
    return cls


class Module:
    prefix = ...

    def __init__(
            self,
            name,
            destinations: List["Module"],
            *args,
            inputs: List["Module"] = None,
            **kwargs
        ):
        self.name = name
        self.inputs = inputs or []
        self.destinations = destinations

    def __repr__(self):
        # return f"{self.__class__.__qualname__}(name={self.name!r}, dst={self.destinations}, inputs={self.inputs})"
        return f"{self.__class__.__qualname__}(name={self.name!r}, dst={self.destinations})"

    def add_input(self, module: "Module"):
        self.inputs.append(module.name)

    def receive(self, src, pulse):
        ...

    def send(self, pulse):
        for dst in self.destinations:
            dst.receive(self, pulse)

@register_module
class FlipFlop(Module):
    prefix = "%"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on = False

    def __repr__(self):
        return f"{self.__class__.__qualname__}(name={self.name!r}, dst={self.destinations}, on={self.on})"
        # return f"{self.__class__.__qualname__}(name={self.name!r}, dst={self.destinations}, inputs={self.inputs}, on={self.on})"

    @property
    def off(self):
        return not self.on

    def receive(self, src, pulse):
        if pulse == 0:
            return

        self.on = not self.on
        pulse = self.on * 1
        return self.send(pulse)


@register_module
class Conjunction(Module):
    """
    Conjunction modules (prefix &) remember the type of the most recent pulse received from each of their connected
    input modules; they initially default to remembering a low pulse for each input. When a pulse is received,
    the conjunction module first updates its memory for that input. Then, if it remembers high pulses for all inputs,
    it sends a low pulse; otherwise, it sends a high pulse.
    """
    prefix = "&"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._inputs = {}

    def __repr__(self):
        return f"{self.__class__.__qualname__}(name={self.name!r}, dst={self.destinations}, inputs={self._inputs})"

    def add_input(self, module: "Module"):
        super().add_input(module)
        self._inputs[module.name] = 0

    def receive(self, src: Module, pulse: int):
        self._inputs[src.name] = pulse

        if all([p == 1 for p in self._inputs.values()]):
            pulse_out = 0
        else:
            pulse_out = 1

        self.send(pulse_out)


@register_module
class Broadcaster(Module):
    prefix = "b"

    def receive_pulse(self, pulse):
        # if pulse == "HIGH"
        # self.on = not self.on
        self.send(pulse)


class Button(Module):
    # TODO
    ...


class PulsePropagation:
    def __init__(self, inp):
        self._inp = inp
        self._modules = self._parse_modules()

        self._enrich_modules()

        schema = deque()
        schema.append(self.btn)
        self.schema = schema

    @property
    def btn(self):
        btn = self._modules[0]
        assert isinstance(btn, Button)
        return btn

    def _construct_module(self, src, destinations):
        prefix = src[0]
        module_class = ModuleRegistry.get_module_class(prefix)

        # for dst_name in destinations:

        if prefix == Broadcaster.prefix:
            name = src
        else:
            name = src[1:]

        return module_class(name=name, destinations=destinations)

    def _parse_modules(self):
        models_list = []

        for line in self._inp:
            src, _destinations = line.split(" -> ")
            destination_names = _destinations.split(", ")
            model = self._construct_module(src, destination_names)
            Modules.register(model.name, model)

            models_list.append(model)

        return models_list

    def _enrich_modules(self):
        modules = self._modules

        # add button
        broadcaster = self._modules[0]
        assert broadcaster.name == "broadcaster"
        btn = Button("button", destinations=[broadcaster.name])
        Modules.register(btn.name, btn)

        modules.insert(0, btn)

        for m in modules:
            m: Module
            for dst_name in m.destinations:
                dst = Modules.get(dst_name)
                dst.add_input(m)

        return

    def propagate(self):
        low_pulses = 0
        high_pulses = 0
        steps = 1000
        ...
        return low_pulses * high_pulses


def pulse_propagation(inp, part=1, **kw):
    return PulsePropagation(inp).propagate()


if __name__ == "__main__":
    test(pulse_propagation, 32000000)
    assert run(pulse_propagation) > 410
