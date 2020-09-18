#!/usr/bin/env python3

import unittest

from unittest_mocker import mocker

import func
from func import soma, SomeClass


class InjectMocker(unittest.TestCase):
    @mocker
    def test_mocked(self, mocker):
        mocked = mocker.patch('func.f')
        self.assertIsInstance(mocked, unittest.mock.MagicMock)

    @mocker
    def test_mock_return_value(self, mocker):
        mocker.patch('func.f').return_value = 50
        self.assertEqual(soma(1, 1), 50)

    @mocker
    def test_called(self, mocker):
        mocker.patch('func.f')
        soma(1, 1)
        func.f.assert_called()
        self.assertEqual(func.f.called, True)
        self.assertEqual(func.f.call_count, 1)

    @mocker
    def test_not_called(self, mocker):
        mocker.patch('func.f')
        func.f.assert_not_called()
        self.assertEqual(func.f.called, False)
        self.assertEqual(func.f.call_count, 0)

    @mocker
    def test_not_mocked(self, mocker):
        self.assertEqual(hasattr(func.f, 'assert_not_called'), False)
        self.assertEqual(hasattr(func.f, 'assert_called'), False)
        self.assertEqual(hasattr(func.f, 'called'), False)
        self.assertEqual(hasattr(func.f, 'call_count'), False)


class TestPatchAFunction(unittest.TestCase):
    def test_original(self):
        self.assertEqual(soma(1, 2), 3)

    @mocker
    def test_mocked(self, mocker):
        mocked = mocker.patch('func.f')
        mocked.return_value = 5
        self.assertEqual(soma(1, 1), 5)
        self.assertEqual(mocked.called, True)

    @mocker
    def test_mocked_compact(self, mocker):
        mocker.patch('func.f').return_value = "abc"
        self.assertEqual(soma(1, 1), "abc")


class TestPatchAClass(unittest.TestCase):
    def test_original(self):
        self.assertEqual(SomeClass().show(), 'hi')

    @mocker
    def test_mocked_method(self, mocker):
        mocked = mocker.patch('func.SomeClass')
        mocked.return_value.show.return_value = 'other show'
        # must import after mocking
        from func import SomeClass
        self.assertEqual(SomeClass().show(), 'other show')


class TestPatchObject(unittest.TestCase):
    def test_original(self):
        self.assertEqual(SomeClass().show(), 'hi')

    @mocker
    def test_patch_method(self, mocker):
        mocker.patch.object(SomeClass, 'show').return_value = 'modified'
        self.assertEqual(SomeClass().show(), 'modified')

    @mocker
    def test_patch_class_after_imported(self, mocker):
        self.assertEqual(SomeClass().show(), 'hi')

        mocker.patch.object(SomeClass, 'show').return_value = 'modified'
        self.assertEqual(SomeClass().show(), 'modified')


if __name__ == "__main__":
    unittest.main()
