from time import time
from typing import final
import logging
from logging import Logger
from warnings import warn
@final
class Timer():
    """A simple timer utility class to measure elapsed time.
    This class provides methods to start, stop, resume, and restart a timer.
    It can also be used as a context manager to automatically stop the timer
    when exiting the context.
    
    Attributes:
        name (str): The name of the timer.
        logger (Logger): A logger instance for logging. If None, uses print().
        disable_print (bool): Whether to disable logging/printing the elapsed time.
        print_digits (int): Number of decimal places to print for elapsed time.
    """

    def __init__(self, name="AsdfTimer", logger:logging.Logger=None, disable_print:bool=False, print_digits:int=2) -> None:
        """Initialize the Timer instance.

        Args:
            name (str, optional): The name of the timer. Defaults to "AsdfTimer".
            logger (Logger, optional): A logger instance for logging. Uses print() if None.
            disable_print (bool, optional): Whether to disable logging/printing the elapsed time. Defaults to False.
            print_digits (int, optional): Number of decimal places to print for elapsed time. Defaults to 2.
        """        
        self.name = name
        self.logger = logger
        assert isinstance(self.logger, (Logger, type(None))), "logger must be a logging.Logger instance or None"
        self.disable_print = disable_print
        self.print_digits = print_digits
        
        # Start the timer
        self.restart()
        
    def check(self) -> float:
        """Output the elapsed time.
        
        Returns:
            float: The elapsed time in seconds.
        """
        check_time = self._stop_time or time()
        dif = check_time - self._start_time
        # If the timer was stopped, add the accumulated elapsed time
        dif += self._elapsed_acc
        if not self.disable_print:
            message = f'{self.name} took {dif:.{self.print_digits}f} seconds'
            if self.logger:
                self.logger.info(message)
            else:
                print(message)
        return dif

    def stop(self) -> float:
        """Pause the timer and output the elapsed time.

        Returns:
            float: The elapsed time in seconds.
        """
        if self._stop_time is not None:
            warn(RuntimeWarning("Timer is already stopped. Doing nothing."))
            return self.check()
        self._stop_time = time()
        return self.check()
    
    def resume(self) -> None:
        """Unstop the timer."""
        if self._stop_time is None:
            warn(RuntimeWarning("Timer is already running. Doing nothing."))
            return
        
        self._elapsed_acc += self._stop_time - self._start_time
        self._stop_time = None
        self._start_time = time()
        
    
    def restart(self) -> None:
        """Restart the timer."""
        self._elapsed_acc = 0
        self._stop_time = None
        self._start_time = time()
        
    
    def __enter__(self):
        """Use the Timer instance as a context manager.

        Returns:
            Timer: The Timer instance itself.
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the timer when exiting the context. Output the elapsed time."""
        self.stop()
        
    
    def __repr__(self) -> str:
        """String representation of the Timer instance."""
        return f"Timer(name={self.name}, disable_print={self.disable_print}, print_digits={self.print_digits})"
    
    def __str__(self) -> str:
        """String representation of the Timer instance."""
        return f"Timer: {self.name}, disable_print={self.disable_print}, print_digits={self.print_digits}"