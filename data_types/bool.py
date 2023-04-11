from __future__ import annotations

import json


class NewBool:
    """
    Класс NewBool представляет собой кастомный тип данных,
    который может быть инициализированю
    значением bool и имеет методы для конвертации в json, int и str.
    """

    def __init__(self, value: bool):
        """
        Инициализация класса со значением bool.
        """
        self._value = bool(value)

    def to_json(self) -> str:
        """
        Метод to_json возвращает строковое представление json с ключом 'value'
        и значением bool типа.
        """
        return json.dumps({'value': self._value})

    def to_int(self) -> int:
        """
        Метод to_int возвращает 1, если self._value равен True,
        и 0 в противном случае.
        """
        return 1 if self._value else 0

    def to_str(self) -> str:
        """
        Метод to_str возвращает 'Yes', если self._value равен True,
        и 'No' в противном случае.
        """
        return "Yes" if self._value else "No"

    def __add__(self, other: NewBool) -> int:
        """
        Перегрузка оператора +.

        Возвращает сумму бул типов (0+1, 1+0 и т.п).
        """
        return int(self._value) + int(other)

    def __int__(self):
        """
        Перегрузка метода __int__.

        Возвращает 1 если True, 0 если False.
        """
        return int(self._value)
