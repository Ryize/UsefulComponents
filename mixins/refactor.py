import inspect
import re


class PEP8NamingMixin:
    @classmethod
    def __init_subclass__(cls):
        class_name = cls.__name__
        if not re.match(r'^[A-Z][a-zA-Z0-9]+$', class_name):
            raise ValueError(
                f'Неверное имя класса {class_name}, нарушение соглашения PEP8'
            )
        for name, value in cls.__dict__.items():
            if callable(value):
                if not re.match(r'^[a-z][a-zA-Z0-9_]+$', name):
                    raise ValueError(
                        f'Неверное имя метода {name}, '
                        f'Нарушение соглашения PEP8'
                    )
                arg_spec = inspect.getfullargspec(value)
                for arg in arg_spec.args:
                    if not re.match(r'^[a-z][a-zA-Z0-9_]+$', arg):
                        raise ValueError(
                            f'Неверное имя аргумента {arg}'
                            f' в методе {name}, нарушение соглашения PEP8'
                        )
        super().__init_subclass__()


class MethodLengthMixin:
    max_length = 50

    @classmethod
    def __init_subclass__(cls):
        for name, value in cls.__dict__.items():
            if callable(value):
                source_code = inspect.getsource(value)
                lines = source_code.split("\n")
                docstring = inspect.getdoc(value)
                docstring_lines = 0 if docstring is None else len(
                    docstring.splitlines()
                )
                if len(lines) - docstring_lines > cls.max_length:
                    raise ValueError(
                        f'Метод {name} содержит более {cls.max_length}'
                        f' строк кода'
                    )
        super().__init_subclass__()


class LineLengthMixin:
    @classmethod
    def __init_subclass__(cls):
        max_length = 79
        for name, value in cls.__dict__.items():
            if callable(value):
                source_code = inspect.getsource(value)
                lines = source_code.split("\n")
                for i, line in enumerate(lines):
                    if len(line) > max_length:
                        raise ValueError(
                            f'Строка {i + 1} в методе {name} содержит более'
                            f' {max_length} символов'
                        )
        super().__init_subclass__()
