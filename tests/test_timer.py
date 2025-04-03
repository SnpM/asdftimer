import pytest
from time import sleep
from easytimer.timer import Timer

def test_timer_end():
    """Test the `end` method for accurate elapsed time."""
    timer = Timer(name="Test Timer", disable_print=False)
    sleep(1)
    elapsed_time = timer.end()
    assert pytest.approx(elapsed_time, rel=0.1) == 1

def test_timer_restart():
    """Test the `restart` method resets the timer."""
    timer = Timer(name="Test Timer", disable_print=False)
    sleep(1)
    timer.restart()
    sleep(0.5)
    elapsed_time = timer.end()
    assert pytest.approx(elapsed_time, rel=0.1) == 0.5

def test_context_manager():
    """Test the Timer as a context manager."""
    with Timer(name="Context Timer", disable_print=False) as timer:
        sleep(1)
    elapsed_time = timer.end()
    assert pytest.approx(elapsed_time, rel=0.1) == 1

def test_timer_disable_print(capfd):
    """Test the `disable_print` functionality."""
    timer = Timer(name="No Print Timer", disable_print=True)
    sleep(1)
    timer.end()
    captured = capfd.readouterr()
    assert captured.out == ""

def test_timer_enable_print(capfd):
    """Test that output is printed when `disable_print` is False."""
    timer = Timer(name="Print Timer", disable_print=False)
    sleep(1)
    timer.end()
    captured = capfd.readouterr()
    assert "Print Timer took" in captured.out

def test_timer_with_logger(caplog):
    """Test the Timer with a custom logger."""
    import logging
    logger = logging.getLogger("test_logger")
    with caplog.at_level(logging.INFO):
        timer = Timer(name="Logger Timer", logger=logger)
        sleep(1)
        timer.end()
    assert "Logger Timer took" in caplog.text

def test_timer_print_digits(capfd):
    """Test the `print_digits` parameter for controlling decimal places."""
    timer = Timer(name="Digits Timer", disable_print=False, print_digits=4)
    sleep(1)
    timer.end()
    captured = capfd.readouterr()
    assert "Digits Timer took" in captured.out
    assert "1.0000 seconds" in captured.out

