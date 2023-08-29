import threading
from functools import wraps
from typing import Callable


class ThreadMixin:
    """
    Делает все методы класса многопоточными.
    """

    def __init__(self):
        for func_name in reversed(dir(self)):
            if func_name == '_to_thread':
                break
            method = getattr(self, func_name)
            thread_method = self._to_thread(method)
            setattr(self, func_name, thread_method)

    def _to_thread(self, func: Callable):
        @wraps(func)
        def inner(*args, **kwargs):
            thread = threading.Thread(target=func, args=args, kwargs=kwargs)
            thread.start()

        return inner
