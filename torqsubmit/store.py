# -*- coding: utf-8 -*-

import abc
import base64
from tempfile import gettempdir, mkstemp
import six

import os

from enum import Enum

class Mode(Enum):

    SINGLE_TASK = 1
    MANY_TASKS = 2

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)


class StoreProperty(Enum, six.text_type):

    MODE = "MODE"
    TASK = "TASK"
    ENVIORMENT = "ENVIORMENT"
    DIRNAME = "DIRNAME"
    TASK_COUNT = "TASK_COUNT"

class StoreNotUsed(Exception): pass

class TorqeSubmitStore(six.with_metaclass(abc.ABCMeta, object)):

    @property
    @abc.abstractmethod
    def store(self):
        """
        Returns dictionary storing tasks to be submitted
        :return:
        """
        return {}

    @abc.abstractmethod
    def load(self):
        raise StoreNotUsed()

    @abc.abstractmethod
    def save_store(self, store):
        """
        Saves store to some object
        :param dict store:
        :return: Object representing the store
        """
        pass

    @property
    def mode(self):
        return Mode.fromstring(self.store[StoreProperty.MODE])


    @property
    def task(self):
        self.__assert_single()
        return self.__load_task(self.store[StoreProperty.TASK])

    @property
    def enviorment(self):
        return self.store[StoreProperty.ENVIORMENT]

    @property
    def task_count(self):
        self.__assert_many()
        return self.store[StoreProperty.TASK_COUNT]

    def get_task(self, no):
        return self.store["TASK_{}".format(no)]

    def __assert_single(self):
        assert self.mode == Mode.SINGLE_TASK

    def __assert_many(self):
        assert self.mode == Mode.MANY_TASKS

    @property
    def _pickle(self):
        try:
            import dill as pickle
        except ImportError:
            import pickle
        return pickle

    def _load_task(self, serialized):
        try:
            import dill as pickle
        except ImportError:
            import pickle
        return pickle.loads(serialized)

    @classmethod
    def pickle_task(cls, task):
        try:
            import dill as pickle
        except ImportError:
            import pickle
        return pickle.dumps(task)


class _EnvDict(dict):
    def __missing__(self, key):
        key = "__PY_T_{}".format(key)
        v = os.environ[key]
        return base64.b64decode(v)


class EnvStore(TorqeSubmitStore):
    def save_store(self, store):
        result = {}
        for k, v in store:
            result["__PY_T_{}".format(k)] = base64.b64encode(v)
        result["__PY_T_{}".format("STORE")] = "ENV"
        return result

    def load(self):
        if os.environ.get("__PY_T_{}".format("STORE")) != "ENV":
            raise StoreNotUsed()

    def store(self):
        return _EnvDict()


class FileBasedStore(TorqeSubmitStore):

    def load(self):
        if os.environ.get("__PY_T_{}".format("STORE")) != "FILE":
            raise StoreNotUsed()
        import pickle
        with open(os.environ['__PY_T_FILE']) as f:
            self.__store = pickle.load(f)

    def store(self):
        return self.__store

    def get_tempdir(self):
        return os.environ.get("__PY_T_TEMPDIR", gettempdir())

    def save_store(self, store):
        import pickle
        opened, file = mkstemp(dir=self.get_tempdir())
        pickle.dump(store, opened)
        opened.close()
        return {"__PY_T_FILE": file, "__PY_T_STORE": "FILE"}
