from time import time
from typing import final
import logging
from logging import Logger


@final
class Timer():
    """A simple timer utility class to measure elapsed time.

    Attributes:
        start_time (float): The time when the timer was started.
        name (str): The name of the timer.
        logger (Logger): The custom logger used for logging messages. Defaults to None.
    """

    def __init__(self, name="EasyTimer", logger:logging.Logger=None, disable_print:bool=False):
        """Initialize the Timer instance.

        Args:
            name (str, optional): The name of the timer. Defaults to "EasyTimer".
            logger (Logger, optional): A logger instance for logging. Uses print() if None.
            disable_print (bool, optional): Whether to disable logging/printing the elapsed time. Defaults to False.
        """
        self.start_time = time()
        self.name = name
        self.logger = logger
        assert isinstance(self.logger, (Logger, type(None))), "logger must be a logging.Logger instance or None"
        self.disable_print = disable_print

    def end(self) -> float:
        """Output the elapsed time.

        Returns:
            float: The elapsed time in seconds.
        """
        dif = time() - self.start_time
        message = f'{self.name} took {dif} seconds'
        if not self.disable_print:
            if self.logger:
                self.logger.info(message)  # Use logger if provided
            else:
                print(message)  # Fallback to print
        return dif
    
    def restart(self) -> None:
        """Restart the timer."""
        self.start_time = time()
        
    
    def __enter__(self):
        """Use the Timer instance as a context manager.

        Returns:
            Timer: The Timer instance itself.
        """
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        """Stop the timer when exiting the context. Output the elapsed time."""
        self.end()