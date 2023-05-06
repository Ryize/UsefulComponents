from typing import Union, Iterable, Callable, Any

from errors.error import MaxSizeException


class SuperiorList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__run = False
        self.__max_size = None

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
        for i in range(len(self)):
            self[i] = rule(self[i])
        return self

    def apply_rule_by_type(self, type_: Union[Callable, Iterable],
                           rule: Callable):
        type_ = self._get_tuple_type(type_)
        for i in range(len(self)):
            if type(self[i]) in type_:
                self[i] = rule(self[i])
        return self

    def _get_tuple_type(self, type_):
        if type(type_) not in [list, tuple, set]:
            type_ = (type_,)
        return type_

    def remove_by_type(self, type_: Union[Callable, Iterable]):
        type_ = self._get_tuple_type(type_)
        for i in range(len(self)):
            if type(self[i]) in type_:
                self.pop(i)
        return self

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
        for i in range(len(self)):
            if not filter_func(self[i]):
                del self[i]
        return self

    def limit(self, max_size: int):
        self.__max_size = max_size
        if max_size > len(self):
            return self
        for i in range(len(self) - max_size):
            del self[-1]
        return self

    def stop_limit(self):
        self.__max_size = None
        return self

    def append(self, *args, **kwargs):
        if self.__max_size and (self.__max_size < len(self) + 1):
            raise MaxSizeException("Превышена максимальная длина списка")
        super().append(*args, **kwargs)

    def remove_all(self, other: Any):
        for i in range(self.count(other)):
            self.remove(other)
        return self

    def __add__(self, other: Any):
        self.append(other)
        return self

    def __sub__(self, other: Any):
        return self.remove_all(other)

    def __truediv__(self, other: int):
        new_list = []
        for i in range(int(len(self) / other)):
            new_list.append(self[i])
        self.clear()
        self.extend(new_list)
