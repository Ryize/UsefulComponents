import logging
import sys
import threading
import time
from typing import Optional, Callable, Union

from errors.error import MismatchType, CallFrequencyHigh
from functools import wraps

try:
    import thread
except ImportError:
    import _thread as thread


def check_types(func: Callable):
    """
    Используется для проверки передаваемых типов данных.

    Например:
        Функция get_sum принимает 2 аргумента, оба должны быть целыми числами
        (int), если мы передадим два целых числа (int), то программа корректно
        отработает. Если мы попробуем передать любой другой тип данных,
        то декоратор вернёт ошибку,
        о не совпадении ожидаемых типов данных с пришедшими.

    Args:
        func: Callable (декорируемаая функция)

    Returns:
        Any (результат работы функции)
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        arguments_types = list(func.__annotations__.values())
        for index in range(len(args)):
            type_arg = arguments_types[index]
            if not isinstance(args[index], type_arg):
                raise MismatchType("Передаваемые/ожидаемые типы не совпадают")
        for param_type in kwargs.items():
            type_kwarg = func.__annotations__[param_type[0]]
            if not isinstance(param_type[1], type_kwarg):
                raise MismatchType("Передаваемые/ожидаемые типы не совпадают")
        return func(*args, **kwargs)

    return wrapper


def repeat(_func: Optional[Callable] = None, *, num_times: int = 2):
    """
    Используется для повторения функции.

    Повторяет декорируемую функцию num_times раз.
    Возвращает последний результат.

    Args:
        _func: Optional[Callable] (декорируемаая функция)
        num_times: int (число раз в период повтора)

    Returns:
        Any (последний результат функции)
    """

    def decorator_repeat(func):
        @wraps(func)
        def wrapper_repeat(*args, **kwargs):
            func_result = None
            for tries in range(num_times):
                func_result = func(*args, **kwargs)
                print(f"Retrying ({func.__name__}): {tries}")
            return func_result

        return wrapper_repeat

    if _func is None:
        return decorator_repeat
    return decorator_repeat(_func)


def debug(func: Callable):
    """
    Используется для упрощения дебага.

    Возвращает передаваемые параметры и результат работы функции.

    Args:
        func: Callable (декорируемаая функция)

    Returns:
        Any (результат функции)
    """

    @wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        print(f"Calling: {func.__name__}({signature})")
        value = func(*args, **kwargs)
        print(f"{func.__name__!r} returned {value!r}")
        return value

    return wrapper_debug


def timeit(func: Callable):
    """
    Используется для проверки времени исполнения функции.

    Печатает сигнатуру и время выполнения функции.

    Args:
        func: Callable (декорируемаая функция)

    Returns:
        Any (результат функции)
    """

    @wraps(func)
    def timed(*args, **kw):
        ts = time.monotonic()
        result = func(*args, **kw)
        te = time.monotonic()
        ms = (te - ts) * 1000
        all_args = ', '.join(tuple(f'{a!r}' for a in args)
                             + tuple(f'{k}={v!r}' for k, v in kw.items()))
        print(f'{func.__name__}({all_args}): {ms:2.2f} ms')
        return result

    return timed


def deprecated(func):
    """
    При вызове метода или функции, помеченной декоратором @deprecated
    будет выдано предупреждение, что метод или функция является устаревшими.

    Можно использовать, как замена TO DO:

    Args:
        func: Callable (декорируемаая функция)

    Returns:
        Any (результат функции)
    """

    @wraps(func)
    def new_func(*args, **kwargs):
        logging.warning("Call to deprecated function {}.".format(func.__name__))
        return func(*args, **kwargs)

    return new_func


class CachedProperty:
    """
    Свойство класса, которое реально вычисляется один раз,
    а потом запоминается на ttl секунд.

    Применение:
        cached_property = CachedProperty
        # применение
        class Foo:
            @cached_property()
            def some_long_running_property(self):
                time.sleep(1)
                return 42
        f = Foo()
        for _ in range(10):
            print(f.some_long_running_property)
    """

    def __init__(self, ttl=300):
        self.ttl = ttl

    def __call__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        return self

    def __get__(self, inst, owner):
        now = time.monotonic()
        try:
            value, last_update = inst._cache[self.__name__]
            if 0 < self.ttl < now - last_update:
                raise AttributeError
        except (KeyError, AttributeError):
            value = self.fget(inst)
            try:
                cache = inst._cache
            except AttributeError:
                cache = inst._cache = {}
            cache[self.__name__] = (value, now)
        return value


from typing import Union
from functools import wraps
import time

def restrict_execution(max_per_second: int, second: Union[int, float] = 1):
    """
    Ограничивает количество вызовов функции.

    Ограничивает вызовы декорируемой функции.
    Счётчик сбрасывается каждые `second` секунд (по умолчанию 1 секунда).

    Args:
        max_per_second: int (максимальное количество вызовов за установленное время).
        second: int (время, за которое ограничивается количество вызовов в секундах).

    Returns:
        Any (результат функции)
    """

    def decorate(func):
        class CallCounter:
            def __init__(self):
                self.last_time_call = 0
                self.count_call = 0

        counter = CallCounter()

        @wraps(func)
        def restricted_func(*args, **kwargs):
            current_time = time.perf_counter()
            if current_time - counter.last_time_call > second:
                counter.last_time_call = current_time
                counter.count_call = 0
            if counter.count_call >= max_per_second:
                name = func.__name__
                raise CallFrequencyHigh(f'Превышена частота вызова {name}')
            counter.count_call += 1
            return func(*args, **kwargs)

        return restricted_func

    return decorate


def _quit_function(func_name):
    logging.error('{name} выполняется слишком долго!'.format(name=func_name))
    sys.stderr.flush()
    thread.interrupt_main()


def exit_after(max_time: Union[int, float]):
    """
    Ограничивает время работы функции.

    Если функция работает дольше установленного лимита,
    вызывается исключение KeyboardInterrupt и функция останавливается.

    Args:
        max_time: int (максимальное время работы функции).

    Returns:
        Any (результат функции)
    """

    def outer(func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            timer_args = [func.__name__]
            timer = threading.Timer(max_time, _quit_function, args=timer_args)
            timer.start()
            try:
                result = func(*args, **kwargs)
            finally:
                timer.cancel()
            return result

        return inner

    return outer

