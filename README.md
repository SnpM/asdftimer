# EasyTimer

EasyTimer is a simple Python utility class for measuring elapsed time. It provides an easy-to-use interface for timing code execution, with support for logging and context management.

## Features

- Measure elapsed time.
- Log elapsed time using a custom logger or `print()`.
- Restart the timer at any point.
- Use as a context manager for automatic timing.

## Installation

```bash
pip install easytimer
```

## Usage

### Basic Usage

```python
from easytimer import Timer
from time import sleep

timer = Timer()
time.sleep (2.4)
elapsed_time = timer.end()
# Output: EasyTimer took 2.40 seconds
```

### Using a Custom Logger

```python
from easytimer.timer import Timer
import logging
logger = logging.getLogger(__name__)

timer = Timer(name="LoggedTimer", logger=logger)
# ur code here
timer.end()
# Output: LoggedTimer took X seconds'
```

### Timing a context

```python
from easytimer.timer import Timer
with Timer(name="ContextTimer") as timer:
    pass # ur code here
# Output: ContextTimer took X seconds
```

## API Reference

### `Timer`

#### `__init__(name="EasyTimer", logger=None, disable_print=False, print_digits=2)`
- `name` (str): The name of the timer. Defaults to `"EasyTimer"`.
- `logger` (Logger): A logger instance for logging. Uses `print()` if `None`.
- `disable_print` (bool): Whether to disable logging/printing the elapsed time. Defaults to `False`.
- `print_digits` (int): Number of decimal places to print for elapsed time. Defaults to `2`.

#### `end() -> float`
Outputs and returns the elapsed time in seconds.

#### `restart() -> None`
Restarts the timer.

#### `__enter__()`
Starts the timer when used as a context manager.

#### `__exit__(exc_type, exc_value, traceback)`
Stops the timer and outputs the elapsed time when exiting the context.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve EasyTimer.

## Author

Developed by [Nibs](https://github.com/SnpM).