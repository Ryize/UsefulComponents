from __future__ import annotations

import hashlib
import re
from typing import Callable, List, Optional

from errors.error import IntervalError


class WeakStr(str):
    def __add__(self, other):
        if type(other) in (list, tuple, set,):
            other = ' '.join(map(str, other))
            return '{iter} {string}'.format(iter=other, string=self)
        return super().__add__(other)

    def get_after_rule(self, rule: Callable) -> WeakStr:
        """
        Возвращает новый объект класса WeakStr,
        созданный из строки, в которой каждый символ заменен
        результатом вызова функции 'rule' с этим символом.

        Args:
            rule (Callable): функция, в которую будут передаеы все символы.

        Returns:
            WeakStr: WeakStr, с новой строкой.
        """
        return self._create_class(''.join([rule(i) for i in self]))

    def find_substring(self, substring: str):
        """
        Находит все вхождения подстроки в строке.

        Используется re.search.

        Args:
            substring (str): строка, которую будем искать.

        Returns:
            Результат вызова re.search
        """
        return re.search(substring, self)

    def get_close_matches(self, possibilities: List[str], n: int = 3,
                          cutoff: float = 0.6) -> List[str]:
        """
        Находит ближайшие совпадения для слова в списке возможностей с
        использованием расстояния Левенштейна.

        В качестве слова, использует значение текущей строки (self).

        Args:
            possibilities (List[str]): Список строк, в котором нужно искать
             близкие совпадения.
            n (int): Максимальное число близких совпадений,
             которые нужно вернуть.
            cutoff (float): Число с плавающей точкой в диапазоне [0.0, 1.0],
             которое указывает максимальное расстояние Левенштейна
             между 'word' и близким совпадением.
             Совпадения с расстоянием большим, чем 'cutoff',
             не будут возвращены.

        Returns:
            List[str]: Список ближайших совпадений, отсортированный
             по расстоянию Левенштейна в количестве n.
        """

        if not n > 0:
            raise IntervalError("n должно быть > 0: %d" % n)
        if not 0.0 <= cutoff <= 1.0:
            raise IntervalError("cutoff в промежутке [0.0, 1.0]: %r" % cutoff)

        result = []
        max_distance = len(self) * cutoff
        for possibility in possibilities:
            distance = self._calculate_distance(self, possibility)
            if distance <= max_distance:
                result.append((distance, possibility))
        result.sort()
        return [x[1] for x in result][:n]

    def _calculate_distance(self, a: str, b: str) -> int:
        """
        Вычислить расстояние Левенштейна между a и b.
        """
        if not a:
            return len(b)
        if not b:
            return len(a)
        if a[0] == b[0]:
            return self._calculate_distance(a[1:], b[1:])
        l1 = self._calculate_distance(a, b[1:])
        l2 = self._calculate_distance(a[1:], b)
        l3 = self._calculate_distance(a[1:], b[1:])
        return min(l1, l2, l3) + 1

    def reverse(self) -> WeakStr:
        """
        Переворачивает строку.

        Returns:
            WeakStr: перевёрнутая строка.
        """
        return self._create_class(self[::-1])

    def is_palindrome(self) -> bool:
        """
        Возвращает True, если строка 'string' является палиндромом,
        иначе False.

        Returns:
            bool: True, если строка является палиндромом. Иначе False.
        """
        return self == self[::-1]

    def longest_common_prefix(self, s2: str) -> WeakStr:
        """
        Возвращает наибольший общий префикс текущей строки и 's2'.

        Args:
            s2 (str): вторая строка для поиска префикса.

        Returns:
            WeakStr: наибольший общий префикс.
        """
        i = 0
        while i < len(self) and i < len(s2) and self[i] == s2[i]:
            i += 1
        return self._create_class(self[:i])

    def longest_common_suffix(self, s2: str) -> WeakStr:
        """
        Возвращает наибольший общий суффикс текущей строки и 's2'.

        Args:
            s2 (str): вторая строка для поиска суффикса.

        Returns:
            WeakStr: наибольший общий суффикс.
        """
        i = 0
        while i < len(self) and i < len(s2) and self[-i - 1] == s2[-i - 1]:
            i += 1
        return self._create_class(self[-i:])

    def longest_common_substring(self, s2: str) -> WeakStr:
        """
        Возвращает самую длинную общую подстроку.

        Args:
            s2 (str): вторая строка.

        Returns:
            WeakStr: самая длинная общая подстрока.
        """
        m = [[0] * (1 + len(s2)) for _ in range(1 + len(self))]
        longest, x_longest = 0, 0
        for x in range(1, 1 + len(self)):
            for y in range(1, 1 + len(s2)):
                if self[x - 1] == s2[y - 1]:
                    m[x][y] = m[x - 1][y - 1] + 1
                    if m[x][y] > longest:
                        longest = m[x][y]
                        x_longest = x
                else:
                    m[x][y] = 0
        return self._create_class(self[x_longest - longest: x_longest])

    def remove_repeated_chars(self,
                              exclude:
                              Optional[list, tuple, set] = None
                              ) -> WeakStr:
        """
        Удаляет повторяющиеся символы из строки.

        Args:
            exclude (list): список символов, которые не должны удаляться.

        Returns:
            WeakStr: строка состоящая из неповторяющихся символов.
        """
        exclude = exclude if exclude is not None else []
        result_str = []
        for i in self:
            if i not in result_str or i in exclude:
                result_str.append(i)
        return self._create_class(''.join(result_str))

    def remove_duplicate_words(self,
                               exclude:
                               Optional[list, tuple, set] = None
                               ) -> WeakStr:
        """
        Удаляет дублирующиеся слова из строки 's'.

        Args:
            exclude (list): список слов, которые не должны удаляться.

        Returns:
            WeakStr: строка состоящая из неповторяющихся слов.
        """
        exclude = exclude if exclude is not None else []
        result_str = []
        for i in self.split(' '):
            if i not in result_str or i in exclude:
                result_str.append(i)
        return self._create_class(' '.join(result_str))

    def extract_numbers(self) -> List[int]:
        """
        Извлекает числа из строки и возвращает их в виде списка.

        Returns:
            List[int]: список с полученными числами.
        """
        return [int(x) for x in re.findall(r'\d+', self)]

    def is_valid_email(self) -> bool:
        """
        Возвращает True, если строка является корректным адресом
        электронной почты, иначе False.

        Returns:
            bool: True, если строка является корректным email, иначе False.
         """
        return re.match(r'^[\w.-]+@[\w.-]+\.[a-z]{2,6}$', self) is not None

    def mask_credit_card(self) -> WeakStr:
        """
        Заменяет цифры в строке, соответствующей номеру кредитной карты,
        на 'X', кроме последних четырех цифр.

        Returns:
            WeakStr: строка с заменёнными символами.
         """
        result_string = re.sub(r'(\d{4})\d+(\d{4})', r'\1XXXXXXXXX\2', self)
        return self._create_class(result_string)

    def hash_string(self, algorithm: str = 'sha256') -> WeakStr:
        """
        Возвращает хеш-сумму строки 's' по указанному алгоритму 'algorithm'.

        Returns:
            WeakStr: зашифрованная строка.
        """
        h = hashlib.new(algorithm)
        h.update(self.encode())
        return self._create_class(h.hexdigest())

    def compare_hashes(self, hash2: str) -> bool:
        """
        Сравнивает две хеш-суммы.

        Returns:
            bool: True, если они равны, иначе False.
        """
        return self == hash2

    def replace_first_occurrence(self,
                                 old_substr: str,
                                 new_substr: str,
                                 ) -> WeakStr:
        """
        Заменяет в строке первое вхождение подстроки 'old_substr'
        на подстроку 'new_substr'.

        Args:
            old_substr (str): подстрока, которую нужно заменить.
            new_substr (str): новая подстрока.

        Returns:
            WeakStr: полученная строка.
        """
        index = self.find(old_substr)
        if index == -1:  # подстрока не найдена
            return self
        return self._create_class(self[:index] + new_substr + self[index + len(old_substr):])

    def _create_class(self, *args, **kwargs) -> WeakStr:
        return self.__class__(*args, **kwargs)
