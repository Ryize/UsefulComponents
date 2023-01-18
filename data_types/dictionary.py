from typing import Any, Callable


class IndexDict(dict):
    def keys(self) -> tuple:
        return tuple(super().keys())

    def values(self) -> tuple:
        return tuple(super().values())

    def items(self) -> tuple:
        return tuple(super().items())

    def __getitem__(self, key):
        if isinstance(key, slice):
            element_from_key = list(self.items())[key]
            after_slicing = element_from_key[key]
            return self.__class__(after_slicing)
        if self.get(key):
            return self.__class__({key: super().__getitem__(key)})
        if isinstance(key, int):
            element_from_key = list(self.items())[key]
            return self.__class__({element_from_key[0]: element_from_key[1]})

    def __setitem__(self, key, value) -> None:
        if isinstance(key, int):
            elements = list(map(lambda i: [i[0], i[1]], self.items()))
            if key <= len(elements):
                self[elements[key][0]] = value
                return
            raise IndexError("Index out of range")
        return super().__setitem__(key, value)

    def remove_by_index(self, index: int = -1) -> None:
        if isinstance(index, int):
            elements = list(map(lambda i: [i[0], i[1]], self.items()))
            if index <= len(elements):
                self.pop(elements[index][0])
                return
            raise IndexError("Index out of range")
        raise KeyError("Index not found")

    def remove_first_by_value(self, value: Any):
        for key, meaning in enumerate(self.values()):
            if meaning == value:
                self.remove_by_index(key)
                return

    def remove_all_by_value(self, value: Any):
        for key, meaning in enumerate(self.values()):
            if meaning == value:
                self.remove_by_index(key)

    def check_depth(self) -> int:
        return self._depth(self)

    @classmethod
    def _depth(cls, _dict):
        if isinstance(_dict, dict):
            return 1 + (max(map(cls._depth, _dict.values())) if _dict else 0)
        return 0

    def apply_rule(self, rule: Callable):
        for k, v in self.items():
            self[k] = rule(v)
        return self

    def apply_rule_depth(self, rule: Callable):
        return self._recursion_rule(self, rule)

    def _recursion_rule(self, d, func: Callable):
        for k, v in d.items():
            if isinstance(v, dict):
                self[k] = self._recursion_rule(v, func)
            else:
                self[k] = func(v)
        return d

    def sort(self, key=lambda x: x[1], reverse=False):
        sorted_data = sorted(self.items(), key=key)
        if reverse:
            sorted_data = sorted_data[::-1]
        self.clear()
        for key, value in sorted_data:
            self[key] = value
        return self.__class__(sorted_data)
