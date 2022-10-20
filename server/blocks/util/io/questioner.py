from collections import OrderedDict
from typing import Any, Iterable

from .exceptions import ChoiceErrorHandler, FormatError, MaxTriesReached, ValidationError, DefaultErrorHandler

class Formatting:
    '''Object with attributes and methods to help format output'''
    default_output_format = "%s : "
    default_expec_format = str

    ERROR = "error"
    INFO = "info"
    QUESTION = "question"
    CHOICE = "choice"
    EXIT = "exit"

    default_frmt_type = INFO

    FORMATS = {
        ERROR: "| ! %s",
        INFO:"| # %s",
        QUESTION:"| ? %s",
        CHOICE:"=> %s",
        EXIT:"| EXITING : %s"
    }

    ACCEPT_INPUT = "y"

    DEFAULT_DIVIDER_LENGTH = 30

    @classmethod
    def normalise(cls, msg:str, frmt_type:Any):
        frmt = cls.FORMATS.get(frmt_type, None)
        if frmt is None:
            raise FormatError(
                "invalid format type '%s'" % frmt_type)
        return frmt % msg

    @classmethod
    def build_final(cls, msg:str):
        return cls.default_output_format % msg.capitalize()

    @staticmethod
    def build_default_message(msg:str, default:Any):
        return "%s (default : %s)" % (msg, default)

    @classmethod
    def build_output(cls, msg:str, frmt_type:Any):
        return cls.default_output_format % cls.normalise(msg, frmt_type)

    @staticmethod
    def add_opts(msg:str, opts:Iterable):
        return "%s (%s)" % (msg, "/".join(opts))

class Questionair:
    '''Modules with methods when outputting and asking for inputs'''
    formatting = Formatting
    error_handler = DefaultErrorHandler
    choice_error_handler = ChoiceErrorHandler

    @classmethod
    def ask(cls, message:str, ttype=None, default=None, **opts) -> Any:
        '''get an input from the cli with given formatting'''
        
        if default:
            message = cls.formatting.build_default_message(message, default)

        if ttype is bool:
            message = cls.formatting.add_opts(message, ("y","n"))
        # handle persists and type
        persists = opts.get("persists", None) 
        if ttype is None:
            ttype = cls.formatting.default_expec_format
        # settings persists to true means exceptions cannot be raised as we rely on errors
        # being raised to check if the iteration can go on
        raise_exceptions = opts.get("raise_exceptions", False)
        if raise_exceptions is True and persists:
            raise AssertionError("cannot persist the input and also raise exceptions")

        err_handler = cls.error_handler(cls, raise_exception=raise_exceptions)

        stop = False
        tries = 0
        while stop is False:
            # we need to try and get a valid response from the user. If an error
            # occurs, we'll need to catch it and handle it.
            try:
                # handle persist if any
                if persists is None:
                    stop = True
                elif type(persists) is int and tries > persists:
                    raise MaxTriesReached("Cancelling due to max tries reached")
                # get an input
                result = input(
                    cls.formatting.build_output(message, opts.get("input_format", cls.formatting.QUESTION))
                    )
                # deal with no responses
                if not result.strip():
                    if default is not None:
                        return default
                    elif not opts.get("blank", False):
                        raise ValidationError("You cannot leave this question unanswered")
                    return None
                # try and cast the value and handle if it is a boolean
                if ttype is bool:
                    if result == cls.formatting.ACCEPT_INPUT:
                        return True
                    return False
                return ttype(result)
            except err_handler.stopping_objects:
                err_handler.exit()
                break
            # handle error using error handler
            except Exception as error:
                error = err_handler.handle(error)
                if err_handler.stop_iterations(error):
                    break
            tries += 1
            
    @classmethod
    def tell(cls, message:str, frmt_type=None):
        '''output to cli in a given format'''
        if frmt_type is None:
            frmt_type = cls.formatting.default_frmt_type 
        print(cls.formatting.normalise(message, frmt_type))

    @classmethod
    def choice(cls, message:str, choices:dict, default=None, **opts):
        '''output a set of choices that requires an input. The given key that is choosen will be given'''
        # users can either choose a string matching a key out of the choices, or 
        # choose an integer matching the given choice
        orederd_choices = OrderedDict()
        orederd_choices.update(choices)
    
        # output a message
        cls.divider(cls.formatting.DEFAULT_DIVIDER_LENGTH)
        cls.tell(message, cls.formatting.INFO)

        persists = opts.get("persists", None) 
        raise_exceptions = opts.get("raise_exceptions", False)
        if raise_exceptions is True and persists:
            raise AssertionError("cannot persist the input and also raise exceptions")
        choices = orederd_choices.keys()
        # validate default value is valid
        if default is not None:
            if type(default) is str:
                assert default in choices, "default value is not in choices"
            elif type(default) is int:
                assert default < len(orederd_choices.keys()) and default > 0, "default value is out of range"
        err_handler = cls.choice_error_handler(cls, raise_exception=raise_exceptions)

        # display choices
        stop = False
        tries = 0
        while stop is False:
            try:
                if persists is None:
                    stop = True
                elif type(persists) is int and tries >= persists:
                    raise MaxTriesReached("Cancelling due to max tries reached")

                # get a choice
                for pos, choice in enumerate(choices):
                    print("%s %s" % (pos+1, cls.formatting.normalise(choice, cls.formatting.CHOICE)))
                choice = cls.ask("choice", default=default, raise_exceptions=True)
                if choice is None:
                    raise ValidationError("You cannot leave this question unanswered")
                value = orederd_choices.get(choice, None)
                if value is None:
                    pos = int(choice)
                    choices = tuple(orederd_choices.values())
                    if pos > len(orederd_choices.keys()) or pos <= 0:
                        raise ValidationError("Choice was not in range. Please pick an option (1-%s)" % len(orederd_choices.keys()))
                    value = choices[pos-1]
                
                return value
            except err_handler.stopping_objects as err:
                err_handler.exit(err)
                break
            except Exception as error:
                error = err_handler.handle(error)
            tries += 1

    @staticmethod
    def divider(divider_length:int=None):
        '''provide a line break'''
        # if no divider length is given, just display a break
        if divider_length is not None:
            return print("- "*divider_length)
        print("")

    