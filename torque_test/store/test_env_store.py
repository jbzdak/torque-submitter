# -*- coding: utf-8 -*-
import os
import unittest

from torqsubmit.store import StoreProperty, Mode, EnvStore, FileBasedStore, \
    load_store

import dill


class TestStore(object):

    STORE_TYPE = None

    @classmethod
    def setUpClass(cls):
        super(TestStore, cls).setUpClass()

        cls.env = dict(os.environ)

        cls.store_data = {}
        cls.store_data[StoreProperty.MODE] = Mode.MANY_TASKS
        cls.store_data[StoreProperty.TASK_COUNT] = 10
        cls.store_data[StoreProperty.TASK_NO(0)] = dill.dumps(lambda: 0)
        cls.store_data[StoreProperty.TASK_NO(1)] = dill.dumps(lambda: 1)

        os.environ.update(cls.STORE_TYPE.save_store(cls.store_data))

    def setUp(self):
        self.store = load_store()
        self.store.load()

    def test_type(self):
        self.assertEqual(self.STORE_TYPE, type(self.store))

    def test_mode(self):
        self.assertEqual(self.store.mode, Mode.MANY_TASKS)

    def test_count(self):
        self.assertEqual(self.store.task_count, 10)

    def test_task_no(self):
        self.assertEqual(self.store.get_task(0)(), 0)
        self.assertEqual(self.store.get_task(1)(), 1)

    @classmethod
    def tearDownClass(cls):
        os.environ.clear()
        os.environ.update(cls.env)


class TestEnvStore(TestStore, unittest.TestCase):

    STORE_TYPE = EnvStore


class TestFileStore(TestStore, unittest.TestCase):

    STORE_TYPE = FileBasedStore