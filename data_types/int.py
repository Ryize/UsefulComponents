from __future__ import annotations

import math
from typing import Any


class _FunctionalNumbers:
    __base = 10  # Стандартная система счисления

    def __add__(self, other: Any) -> _FunctionalNumbers:
        """
        Добавляет возможность прибавить к числу строку
        (строка преобразуется в число).
        """
        if isinstance(other, str) and other.isdigit():
            return self._create_class(
                super().__add__(self._create_class(other))
            )
        return self._create_class(super().__add__(other))

    def sqrt(self, n: int = 2) -> _FunctionalNumbers:
        """
        Возвращает квадратный корень числа.
        Параметр n позволяет вычислить корень степени n.
        """
        return self._create_class((self ** (1 / n)))

    def pow(self, n: int = 2) -> _FunctionalNumbers:
        """
        Возводит число в степень n.
        """
        return self._create_class(self ** n)

    def reverse(self) -> _FunctionalNumbers:
        """
        Возвращает число в обратном порядке.
        """
        return self._create_class(str(self)[::-1])

    def log(self, base: int = 2) -> _FunctionalNumbers:
        """
        Возвращает логарифм числа по основанию base.

        Args:
            base (int): основание алгоритма
        """
        return self._create_class(math.log(self, base))

    def sin(self) -> _FunctionalNumbers:
        """
        Возвращает синус числа, заданного в градусах.
        """
        return self._create_class(math.sin(self * math.pi / 180))

    def cos(self) -> _FunctionalNumbers:
        """
        Возвращает косинус числа, заданного в градусах.
        """
        return self._create_class(math.cos(self * math.pi / 180))

    def tan(self) -> _FunctionalNumbers:
        """
        Возвращает тангенс числа, заданного в градусах.
        """
        return self._create_class(math.tan(self * math.pi / 180))

    def gcd(self, *args) -> int:
        """
        Возвращает НОД (Наибольший общий делитель)
        для данного числа и переданных аргументов.
        """
        return math.gcd(self, *args)

    def lcm(self, *args) -> int:
        """
        Возвращает НОК (Наименьшее общее кратное)
        для данного числа и переданных аргументов.
        """
        return math.lcm(self, *args)

    def to_base(self, new_base) -> _FunctionalNumbers:
        """
        Преобразует число в систему счисления с основанием new_base.
        """
        if new_base == self.__base:
            return self._create_class(int(str(self)))
        elif new_base == 10:
            return self._create_class(int(str(self), new_base))
        digits = []
        value = self
        while value > 0:
            value, remainder = divmod(value, new_base)
            digits.append(str(remainder))
        digits.reverse()
        return self._create_class(''.join(digits))

    def is_prime(self) -> bool:
        """
        Возвращает True, если число простое, и False в противном случае.
        """
        if self < 2:
            return False
        for i in range(2, int(self.sqrt()) + 1):
            if self % i == 0:
                return False
        return True

    def _create_class(self, *args, **kwargs) -> _FunctionalNumbers:
        return self.__class__(*args, **kwargs)


class WeakInt(int, _FunctionalNumbers):
    pass
