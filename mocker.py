import functools
import unittest.mock


class Mocker:
    """Controls the patches to clean everything up after leaving the test method."""
    def __init__(self):
        self._patchers = []
        self.patch = Patcher(self)

    def append_patcher(self, patcher):
        self._patchers.append(patcher)

    def stop(self):
        for patcher in reversed(self._patchers):
            patcher.stop()


class Patcher:
    """Class responsible to replicate the `patch` API"""
    def __init__(self, mocker):
        self._mocker = mocker

    def __call__(self, object_name):
        patcher = unittest.mock.patch(object_name)
        patched = patcher.start()
        self._mocker.append_patcher(patcher)
        return patched

    def object(self, target, attribute):
        patcher = unittest.mock.patch.object(target, attribute)
        patched = patcher.start()
        self._mocker.append_patcher(patcher)
        return patched


def mocker(func):
    """Decorator to inject `mocker` into a test method.

    Inspired by https://github.com/pytest-dev/pytest-mock

    Usage:

    >>> class MyTestCase(unittest.TestCase):
    ...     @mocker
    ...     def test_something(self, mocker):
    ...         mocked = mocker.patch('package.module.ClassName')
    ...         mocked.method.return_value = 3
    ...         # ...
    ...
    """
    @functools.wraps(func)
    def wrapper_mocker(*args, **kwargs):
        try:
            mocker_ = Mocker()
            result = func(*args, mocker_, **kwargs)
        except:
            raise
        finally:
            mocker_.stop()
        return result

    return wrapper_mocker

