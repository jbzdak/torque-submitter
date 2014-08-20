# -*- coding: utf-8 -*-
from functools import partial
import shutil
import unittest
from nose.tools.nontrivial import nottest, istest
import os
from uuid import uuid4
import random
import string
import tempfile
from codecs import open
import six
import time
from torqsubmit import Submitter
from torqsubmit._test import TestTask
from torqsubmit.store import FileBasedStore, EnvStore


DEFAULT_TEST_DIR = os.path.join(os.path.dirname(__file__), '__test_scrath')

TEST_DIR = os.environ.get('__PY_T_TEST_DIR', DEFAULT_TEST_DIR)

if not os.path.exists(TEST_DIR):
    os.makedirs(TEST_DIR)


FileBasedStore.set_tepmdir(TEST_DIR)


class BaseTest(object):

    @classmethod
    def setUpClass(cls):
        assert os.path.exists(TEST_DIR)
        cls.dir = os.path.join(TEST_DIR, "".join([random.choice(string.ascii_letters) for __ in range(15)]))
        os.makedirs(cls.dir)


    @classmethod
    def tearDownClass(cls):
        pass
        shutil.rmtree(cls.dir)


class TestSanity(BaseTest, unittest.TestCase):

    def test_sanity(self):
        tt = TestTask(self.dir)
        tt('foo')
        tt.validate('foo')

    def test_invalid(self):
        tt = TestTask(self.dir)
        tt('foo')
        with self.assertRaises(AssertionError):
            tt.validate('bar')

    def test_no_file(self):
        tt = TestTask(self.dir)
        with self.assertRaises(AssertionError):
            tt.validate('bar')


@nottest
class TestSubmiSingle(BaseTest, unittest.TestCase):

    STORE = None

    def test_submit_single_task(self):

        s = Submitter()
        s.guess_virtualenv()
        print(self.dir)
        ttt = TestTask(self.dir)
        s.tasks = [partial(ttt, 'foo')]
        s.StoreClass = self.STORE
        s.submit()
        time.sleep(15)
        ttt.validate('foo')


@istest
class SubmitSingleFile(TestSubmiSingle):

    STORE = FileBasedStore


@istest
class SubmitSingleEnv(TestSubmiSingle):

    STORE = EnvStore

@nottest
class TestSubmitMany(BaseTest, unittest.TestCase):

    STORE = None

    def setUp(self):
        self.tasks = [TestTask(self.dir) for __ in range(10)]
        self.args = [
             "".join([random.choice(string.ascii_letters) for __ in range(15)])
             for __ in range(10)
        ]

    def test_submit_many_tasks(self):

        s = Submitter()
        s.guess_virtualenv()
        s.tasks = [partial(t, a) for t, a in zip(self.tasks, self.args)]
        s.StoreClass = self.STORE
        s.submit()
        time.sleep(15)
        for t, a in zip(self.tasks, self.args):
            t.validate(a)

    def test_submit_many_array(self):

        s = Submitter()
        s.use_pbs_array=True
        s.array_tasks_to_run_in_paralel=5
        s.guess_virtualenv()
        s.tasks = [partial(t, a) for t, a in zip(self.tasks, self.args)]
        s.StoreClass = self.STORE
        s.submit()
        time.sleep(15)
        for t, a in zip(self.tasks, self.args):
            t.validate(a)


@istest
class TestSubmitManyFile(TestSubmitMany):

    STORE = FileBasedStore


@istest
class TestSubmitManyEnv(TestSubmitMany):

    STORE = EnvStore