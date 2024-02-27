import inspect


class FriendMixin:
    """
    Добавляет концепцию "дружественного класса"
    (https://www.geeksforgeeks.org/friend-class-function-cpp/).

    В дочернем классе необходимо создать Iterable __friends и указать ссылка на
    дружественные классы.
    """
    def __getattr__(self, name: str):
        """
        Если запрос исходит от дружественного класса, то метод будет вызван,
        даже если он скрытый (private). То же самое и с полями.

        Args:
            name: str (название вызываемого метода/поля)
        """
        stack = inspect.stack()
        frame = stack[1][0]
        caller = frame.f_locals.get('self', None)
        if caller.__class__ in self.__friends:
            name = name.replace(f'_{caller.__class__.__name__}', '')
            return getattr(self, f'_{self.__class__.__name__}{name}')
        return self.__getattribute__(name)


def auto_friend():
    """
    Если необходимо сделать все классы в Python проекте дружественными,
    запустите эту функцию.

    Меняет __getattr__ для всех имеющихся классов (кроме тех, у которых нельзя
    изменить __getattr__)ю
    """
    import inspect

    def __getattr__(self, name):
        stack = inspect.stack()
        frame = stack[1][0]
        caller = frame.f_locals.get('self', None)
        if caller.__class__ in self.__friends:
            name = name.replace(f'_{caller.__class__.__name__}', '')
            return getattr(self, f'_{self.__class__.__name__}{name}')
        return self.__getattribute__(name)

    for i in object.__subclasses__():
        if not getattr(i, '__getattr__', None):
            try:
                i.__getattr__ = __getattr__
                print(i)
            except TypeError:
                pass
