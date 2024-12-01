import logging


class LoggingMixin(object):
    def __init__(self):
        self._logger = logging.getLogger(self.__class__.__name__)

    def log_debug(self, message):
        self._logger.debug(message)

    def log_info(self, message):
        self._logger.info(message)

    def log_warning(self, message):
        self._logger.warning(message)

    def log_error(self, message):
        self._logger.error(message)

    def log_critical(self, message):
        self._logger.critical(message)


class LoggingToFileMixin:
    """
    Записывает название функции, args, kwargs и результат работы в файл.

    Конструкция __name__ == '__main__' обязательна
    """

    def __init__(self, log_file='log.txt'):
        self._log_file = log_file

    def __getattribute__(self, name):
        """
        Этот метод вызывается каждый раз, когда экземпляр класса пытается
        получить доступ к атрибуту.

        Он принимает один аргумент - name,
        который является именем атрибута. Метод пытается получить доступ
        к атрибуту с именем name с помощью super().__getattribute__(name).
        Если атрибут является вызываемым объектом, метод возвращает
        функцию wrapped, которая записывает информацию о вызове метода
        в файл и вызывает оригинальный метод с переданными аргументами.
        Если атрибут не является вызываемым объектом, метод возвращает
        оригинальный.
        """
        attr = super().__getattribute__(name)
        if callable(attr):
            def wrapped(*args, **kwargs):
                with open(self._log_file, 'a') as f:
                    f.write(f'{name}({args}, {kwargs})')
                return attr(*args, **kwargs)

            return wrapped
        return attr
