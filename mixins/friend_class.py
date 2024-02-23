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