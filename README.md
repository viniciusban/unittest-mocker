# unittest-mocker

Like [pytest-mock](https://github.com/pytest-dev/pytest-mock), but for unittest.

Starring, the `@mocker` decorator:

```
import os

class UnixFS:
    @staticmethod
    def rm(filename):
        os.remove(filename)

class MyTestCase(unittest.TestCase):
    @mocker
    def test_something(self, mocker):
        mocker.patch('os.remove')
        UnixFS.rm('file')
        os.remove.assert_called_once_with('file')
```


You don't need levels of context managers or stacked decorators. Only one `mocker` parameter is enough:

```
import datetime
import os

class MyTestCase(unittest.TestCase):
    @mocker
    def test_something(self, mocker):
        mocker.patch('os.remove')
        mocker.patch('datetime.date')
        mocker.patch('datetime.time')
        mocker.patch('datetime.datetime')
        # do what you need

```


WIP
