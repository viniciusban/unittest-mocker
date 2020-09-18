# unittest-mock

Like [pytest-mock](https://github.com/pytest-dev/pytest-mock), but for unittest. Introduces the `@mocker` decorator:

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


You don't need a context manager or stacked decorators. With the `mocker` parameter you mock everything.


WIP
