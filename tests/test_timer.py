import pytest
from time import sleep
from asdftimer.timer import Timer

def test_timer_stop():
    """Test the `end` method for accurate elapsed time."""
    timer = Timer(name="Test Timer", disable_print=False)
    sleep(1)
    elapsed_time = timer.stop()
    assert pytest.approx(elapsed_time, rel=0.1) == 1

def test_timer_restart():
    """Test the `restart` method resets the timer."""
    timer = Timer(name="Test Timer", disable_print=False)
    sleep(1)
    timer.restart()
    sleep(0.5)
    elapsed_time = timer.stop()
    assert pytest.approx(elapsed_time, rel=0.1) == 0.5

def test_context_manager():
    """Test the Timer as a context manager."""
    with Timer(name="Context Timer", disable_print=False) as timer:
        sleep(1)
    elapsed_time = timer.stop()
    assert pytest.approx(elapsed_time, rel=0.1) == 1

def test_timer_disable_print(capfd):
    """Test the `disable_print` functionality."""
    timer = Timer(name="No Print Timer", disable_print=True)
    sleep(1)
    timer.stop()
    captured = capfd.readouterr()
    assert captured.out == ""

def test_timer_enable_print(capfd):
    """Test that output is printed when `disable_print` is False."""
    timer = Timer(name="Print Timer", disable_print=False)
    sleep(1)
    timer.stop()
    captured = capfd.readouterr()
    assert "Print Timer took" in captured.out

def test_timer_with_logger(caplog):
    """Test the Timer with a custom logger."""
    import logging
    logger = logging.getLogger("test_logger")
    with caplog.at_level(logging.INFO):
        timer = Timer(name="Logger Timer", logger=logger)
        sleep(1)
        timer.stop()
    assert "Logger Timer took" in caplog.text

def test_timer_print_digits(capfd):
    """Test the `print_digits` parameter for controlling decimal places."""
    timer = Timer(name="Digits Timer", disable_print=False, print_digits=1)
    sleep(1)
    timer.stop()
    captured = capfd.readouterr()
    assert "Digits Timer took" in captured.out
    assert "1.0 seconds" in captured.out

def test_timer_start_resumes():
    """Test that `start` resumes the timer after a stop."""
    timer = Timer(name="Resume Timer", disable_print=True)
    sleep(1)
    timer.stop()
    timer.resume()  # resume after stopping
    sleep(0.5)
    elapsed_time = timer.stop()
    # The total elapsed should be close to 1 + 0.5 seconds.
    assert pytest.approx(elapsed_time, rel=0.1) == 1.5

def test_timer_start_warn():
    """Test that calling `start` on a running timer warns."""
    timer = Timer(name="Warn Timer", disable_print=True)
    with pytest.warns(RuntimeWarning):
        timer.resume()

