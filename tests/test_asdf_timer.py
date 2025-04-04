import pytest
from time import sleep
from asdftimer.asdf_timer import AsdfTimer

def test_timer_stop():
    """Test the `end` method for accurate elapsed time."""
    timer = AsdfTimer(name="Test Timer", disable_print=False)
    sleep(0.1)
    elapsed_time = timer.stop()
    assert pytest.approx(elapsed_time, rel=0.1) == 0.1

def test_timer_restart():
    """Test the `restart` method resets the timer."""
    timer = AsdfTimer(name="Test Timer", disable_print=False)
    sleep(0.1)
    timer.restart()
    sleep(0.05)
    elapsed_time = timer.stop()
    assert pytest.approx(0.05, rel=0.1) == elapsed_time

def test_context_manager():
    """Test the Timer as a context manager."""
    with AsdfTimer(name="Context Timer", disable_print=False) as timer:
        sleep(0.1)
    elapsed_time = timer.check()
    assert pytest.approx(elapsed_time, rel=0.1) == 0.1

def test_timer_disable_print(capfd):
    """Test the `disable_print` functionality."""
    timer = AsdfTimer(name="No Print Timer", disable_print=True)
    sleep(0.1)
    timer.stop()
    captured = capfd.readouterr()
    assert captured.out == ""

def test_timer_enable_print(capfd):
    """Test that output is printed when `disable_print` is False."""
    timer = AsdfTimer(name="Print Timer", disable_print=False)
    sleep(0.1)
    timer.stop()
    captured = capfd.readouterr()
    assert "Print Timer took" in captured.out

def test_timer_with_logger(caplog):
    """Test the Timer with a custom logger."""
    import logging
    logger = logging.getLogger("test_logger")
    with caplog.at_level(logging.INFO):
        timer = AsdfTimer(name="Logger Timer", logger=logger)
        sleep(0.1)
        timer.stop()
    assert "Logger Timer took" in caplog.text

def test_timer_print_digits(capfd):
    """Test the `print_digits` parameter for controlling decimal places."""
    timer = AsdfTimer(name="Digits Timer", disable_print=False, print_digits=1)
    sleep(0.1)
    timer.stop()
    captured = capfd.readouterr()
    assert "Digits Timer took" in captured.out
    assert "0.1 seconds" in captured.out

def test_timer_start_resumes():
    """Test that `start` resumes the timer after a stop."""
    timer = AsdfTimer(name="Resume Timer", disable_print=True)
    sleep(0.1)
    timer.stop()
    timer.resume()  # resume after stopping
    sleep(0.05)
    elapsed_time = timer.stop()
    # The total elapsed should be close to 0.1 + 0.05 seconds.
    assert pytest.approx(elapsed_time, rel=0.1) == 0.15

def test_timer_start_warn():
    """Test that calling `start` on a running timer warns."""
    timer = AsdfTimer(name="Warn Timer", disable_print=True)
    with pytest.warns(RuntimeWarning):
        timer.resume()

def test_timer_repr_str():
    """Test __repr__ and __str__ methods of AsdfTimer."""
    timer = AsdfTimer(name="ReprStr Timer", disable_print=True)
    repr_value = repr(timer)
    str_value = str(timer)
    assert "ReprStr Timer" in repr_value
    assert "ReprStr Timer" in str_value

def test_timer_stop_twice_warn(capfd):
    """Test that calling stop() twice warns and returns consistent elapsed time."""
    timer = AsdfTimer(name="Double Stop Timer", disable_print=True)
    sleep(0.05)
    first_time = timer.stop()
    with pytest.warns(RuntimeWarning):
        second_time = timer.stop()
    assert pytest.approx(second_time, rel=0.1) == first_time

def test_elapsed_property():
    """Test that the elapsed property accumulates time correctly."""
    timer = AsdfTimer(name="Elapsed Timer", disable_print=True)
    sleep(0.05)
    running_elapsed = timer.elapsed
    sleep(0.05)
    stopped_elapsed = timer.stop()
    # Verify that elapsed time increased as expected
    assert stopped_elapsed > running_elapsed

def test_exit_already_stopped():
    """Test __exit__ when timer is already stopped."""
    from asdftimer.asdf_timer import AsdfTimer
    from time import sleep
    timer = AsdfTimer(name="Already Stopped Timer", disable_print=True)
    sleep(0.05)
    first_elapsed = timer.stop()  # timer is now stopped
    ret = timer.__exit__(None, None, None)  # should go through the already-stopped branch
    assert ret is None
    # Verify that elapsed time remains at least first_elapsed.
    assert timer.elapsed >= first_elapsed