from __future__ import annotations

from typing import Any, Union

from data_types.int import _FunctionalNumbers


class CorrectFloat(float, _FunctionalNumbers):
    """
    Класс исправляющий некорректное складывание дробных чисел.
    """

    def __add__(self, other: Any) -> CorrectFloat:
        """
        Складывает два числа, при этом убирая нюанс бесконечного float,
        пример: 0.1 + 0.2 = 0.3000000004,
        на этом классе: 0.1 + 0.2 = 0.3.

        Работает с помощью округления.

        Args:
            other (Any): значение с которым складываем

        Returns:
            CorrectFloat
        """
        if isinstance(other, str) and other.isdigit():
            return self.__class__(super().__add__(self._create_class(other)))

        if isinstance(other, int):
            return self.__class__(super().__add__(other))

        len_number = self._get_len_number(self, 1)
        len_part = self._get_len_number(other, 1)
        return self._create_class(
            round(super().__add__(other), len_number + len_part)
        )

    def _get_len_number(self, number: Union[int, float], index: int = 0):
        """
        Возвращает кол-во цифр до или после запятой (зависит от индекса).
        """
        return len(str(number).split('.')[index])
