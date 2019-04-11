class BaseResponse():
    def __init__(self, code=200, data=None, error=None, *args, **kwargs):
        self.code = code
        self.data = data
        self.error = error

    @property
    def dict(self):
        return self.__dict__