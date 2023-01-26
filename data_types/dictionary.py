from __future__ import annotations

from typing import Any, Callable


class IndexDict(dict):
    """
    Класс наследует от dict.

    Добавляет методы для работы со словарем по индексу
    и применение правила на все элементы словаря.
    """

    def keys(self) -> tuple:
        """
        Возвращает кортеж из ключей словаря.
        """
        return tuple(super().keys())

    def values(self) -> tuple:
        """
        Возвращает кортеж из значений словаря.
        """
        return tuple(super().values())

    def items(self) -> tuple:
        """
        Возвращает кортеж из пар ключ-значение словаря
        """
        return tuple(super().items())

    def __getitem__(self, key):
        """
        Переопределяет метод для доступа к элементу словаря по индексу.
        """
        if isinstance(key, slice):
            element_from_key = list(self.items())[key]
            after_slicing = element_from_key[key]
            return self.__class__(after_slicing)
        if self.get(key):
            return self.__class__({key: super().__getitem__(key)})
        if isinstance(key, int):
            element_from_key = list(self.items())[key]
            return self.__class__({element_from_key[0]: element_from_key[1]})
        raise KeyError("Элемент или индекс не найдены!")

    def __setitem__(self, key, value) -> None:
        """
        Переопределяет метод для задания значения элемента словаря по индексу.
        """
        if isinstance(key, int):
            elements = list(map(lambda i: [i[0], i[1]], self.items()))
            if key <= len(elements):
                super().__setitem__(elements[key][0], value)
                return
            raise IndexError("Index out of range")
        super().__setitem__(key, value)

    def remove_by_index(self, index: int = -1) -> None:
        """
        Удаляет элемент словаря по индексу.

        Args:
            index (int): индекс удаляемого элемента (-1 по умолчанию)
        """
        if isinstance(index, int):
            elements = list(map(lambda i: [i[0], i[1]], self.items()))
            if index <= len(elements):
                self.pop(elements[index][0])
                return
            raise IndexError("Index out of range")
        raise KeyError("Index not found")

    def remove_first_by_value(self, value: Any) -> None:
        """
        Удаляет первый элемент словаря с заданным значением.

        Args:
            value (Any): Значение для удаления (удаляет первое вхождение)
        """
        for key, meaning in enumerate(self.values()):
            if meaning == value:
                self.remove_by_index(key)
                return

    def remove_all_by_value(self, value: Any) -> None:
        """
        Удаляет все элементы словаря с заданным значением.

        Args:
            value (Any): Значение для удаления (удаляет все вхождения)
        """
        for key, meaning in enumerate(self.values()):
            if meaning == value:
                self.remove_by_index(key)

    def check_depth(self) -> int:
        """
        Возвращает глубину словаря.
        """
        return self._depth(self)

    @classmethod
    def _depth(cls, _dict) -> int:
        """
        Вспомогательный метод для определения глубины словаря.
        """
        if isinstance(_dict, dict):
            return 1 + (max(map(cls._depth, _dict.values())) if _dict else 0)
        return 0

    def apply_rule(self, rule: Callable) -> IndexDict:
        """
        Применяет заданную функцию ко всем значениям словаря.

        Args:
            rule (Callable): функция для применения
        """
        for k, v in self.items():
            self[k] = rule(v)
        return self

    def apply_rule_depth(self, rule: Callable) -> IndexDict:
        """
        Применяет заданное правило ко всем значениям словаря во всех вложенных уровнях.

        Args:
            rule (Callable): функция для применения
        """
        return self._recursion_rule(self, rule)

    def _recursion_rule(self, _dict, func: Callable) -> IndexDict:
        """
        Вспомогательный метод для применения правила
        ко всем значениям словаря во всех вложенных уровнях.
        """
        for k, v in _dict.items():
            if isinstance(v, dict):
                self[k] = self._recursion_rule(v, func)
            else:
                self[k] = func(v)
        return _dict

    def sort(self, key: Callable = lambda x: x[1], reverse: bool = False) -> IndexDict:
        """
        Сортирует словарь по заданному ключу.

        Args:
            key (Callable): функция для сортировки
            reverse (bool): перевернуть результат
        """
        sorted_data = sorted(self.items(), key=key)
        if reverse:
            sorted_data = sorted_data[::-1]
        self.clear()
        for key, value in sorted_data:
            self[key] = value
        return self.__class__(sorted_data)
