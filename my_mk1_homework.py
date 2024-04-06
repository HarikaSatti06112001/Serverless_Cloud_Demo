# my_mk1_homework.py
from dispatcher import Dispatcher
from runtimes import RuntimeAlpha, RuntimeBeta

dispatcher = Dispatcher()

class Alpha:
    def __call__(self, user, args):
        """
        Invokes the RuntimeAlpha with the specified user and arguments.
        Returns the result of the runtime execution.
        """
        return dispatcher.dispatch(user=user, runtime=RuntimeAlpha, args=args)

class Beta:
    def __call__(self, user, args):
        """
        Invokes the RuntimeBeta with the specified user and arguments.
        Returns the result of the runtime execution.
        """
        return dispatcher.dispatch(user=user, runtime=RuntimeBeta, args=args)