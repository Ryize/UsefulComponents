from typing import Union, Iterable, Callable, Any

from errors.error import MaxSizeException


class ModifiableTuple(tuple):
    __max_size = None

    def cycle(self):
        number_iter = 0
        self.__run = True
        while True:
            if not self.__run:
                break
            yield self[number_iter]
            number_iter += 1
            if number_iter >= len(self):
                number_iter = 0

    def stop_cycle(self):
        self.__run = False

    def get_by_type(self, type_: Union[Callable, Iterable]):
        type_ = self._get_tuple_type(type_)
        return self.__class__([i for i in self if type(i) in type_])

    def apply_rule(self, rule: Callable):
        new_data = []
        for i in range(len(self)):
            new_data[i].append(rule(self[i]))
        return self.__class__(new_data)

    def apply_rule_by_type(self, type_: Union[Callable, Iterable],
                           rule: Callable):
        type_ = self._get_tuple_type(type_)
        new_data = []
        for i in range(len(self)):
            if type(self[i]) in type_:
                new_data[i].append(rule(self[i]))
        return self.__class__(new_data)

    def _get_tuple_type(self, type_):
        if type(type_) not in [list, tuple, set]:
            type_ = (type_,)
        return type_

    def get_by_list(self):
        return list(self)

    def get_by_tuple(self):
        return tuple(self)

    def get_by_set(self):
        return set(self)

    def get_by_dict(self):
        return {key: value for key, value in enumerate(self)}

    def sum(self):
        return sum(self)

    def avg(self):
        return sum(self) / len(self)

    def max(self):
        return max(self)

    def min(self):
        return min(self)

    def len(self):
        return len(self)

    def filter(self, filter_func: Callable):
        new_data = []
        for i in range(len(self)):
            if not filter_func(self[i]):
                new_data.append(self[i])
        return self.__class__(new_data)

    def limit(self, max_size: int):
        self.__max_size = max_size
        new_data = []
        if max_size > len(self):
            return self
        for i in range(len(self) - max_size):
            new_data.append(self[i])
        return self.__class__(new_data)

    def stop_limit(self):
        self.__max_size = None
        return self

    def append(self, element: Any):
        if self.__max_size and (self.__max_size < len(self) + 1):
            raise MaxSizeException("Превышена максимальная длина списка")
        return self.__class__(self + (element,))

    def pop(self, index: int):
        result_data = [value for k, value in enumerate(self) if k != index]
        return self.__class__(result_data)

    def remove(self, element: Any):
        return self.__class__([value for value in self if value != element])
    