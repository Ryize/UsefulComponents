class SingletonMixin:
    _singleton_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._singleton_instance:
            cls._singleton_instance = super(SingletonMixin, cls).__new__(cls, *args, **kwargs)
        return cls._singleton_instance
