class FormatError(Exception):
    '''formatting is invalid'''
    pass

class ValidationError(Exception):
    '''given input did not meet a certain expectation'''
    pass

class MaxTriesReached(Exception):
    '''max input tries have been reached'''
    pass

class BaseErrorHandler:
    '''base error handler with methods to customise how an error or interupt is dealt with'''
    # objects that cause iterations to stop fully
    stopping_objects = (KeyboardInterrupt, MaxTriesReached)

    def __init__(self, cls, raise_exception=True, **kwargs) -> None:
        self.cls=cls
        self.raise_exception = raise_exception
        self.kwargs = kwargs

    def handle(self, error):
        '''raise error if true'''
        if self.raise_exception or isinstance(error, AssertionError):
            raise error

    def exit(self, error=None):
        '''handle keyboard interupt'''
        if error is None:
            error = KeyboardInterrupt("Cancelling session due to user")
        if self.raise_exception:
            raise error
        self.cls.divider()
        self.cls.tell(error, self.cls.formatting.ERROR)

    @classmethod
    def stop_iterations(cls, error):
        return isinstance(error, cls.stopping_objects)

class DefaultErrorHandler(BaseErrorHandler):
    '''default error handler when handling general errors'''
    def handle(self, error):
        ttype = self.kwargs.get("ttype")
        if isinstance(error, ValueError):
            error = ValidationError("Expected type '%s' could not be casted to given response" % ttype)
        super().handle(error)
        self.cls.divider()
        self.cls.tell(error, self.cls.formatting.ERROR)
        return error

class ChoiceErrorHandler(DefaultErrorHandler):
    '''error handler for dealing with choices'''
    def handle(self, error):
        if isinstance(error, ValueError):
            error = ValidationError("Expected string matching a choice or a number matching a choice's position")
        super().handle(error)