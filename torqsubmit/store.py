# -*- coding: utf-8 -*-

import abc
import base64
from functools import total_ordering
from tempfile import gettempdir, mkstemp
import six
import pickle
import os

from enum import Enum

class Mode(object):

    SINGLE_TASK = "SINGLE_TASK"
    MANY_TASKS = "MANY_TASKS"

    @classmethod
    def fromstring(cls, str):
        return getattr(cls, str.upper(), None)

class StoreProperty(object):

    MODE = "MODE"
    TASK = "TASK"
    ENVIORMENT = "ENVIORMENT"
    DIRNAME = "DIRNAME"
    TASK_COUNT = "TASK_COUNT"

    @classmethod
    def TASK_NO(self, no):
        return "TASK_{}".format(no)


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

    @classmethod
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
    def map_kwargs(self):
        self.__assert_many()
        return self.store[StoreProperty.MAP_KWARGS]

    def cpus_per_task(self):
        return self.store[StoreProperty]

    @property
    def task(self):
        self.__assert_single()
        return self._load_task(self.store[StoreProperty.TASK])

    @property
    def task_count(self):
        self.__assert_many()
        return self.store[StoreProperty.TASK_COUNT]

    def get_task(self, no):
        return self._load_task(self.store[StoreProperty.TASK_NO(no)])

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
        return pickle.loads(base64.b64decode(v))


class EnvStore(TorqeSubmitStore):
    @classmethod
    def save_store(self, store):
        result = {}
        for k, v in store.items():
            result["__PY_T_{}".format(k)] = base64.b64encode(pickle.dumps(v))
        result["__PY_T_{}".format("STORE")] = "ENV"
        return result

    def load(self):
        if os.environ.get("__PY_T_{}".format("STORE")) != "ENV":
            raise StoreNotUsed()

    @property
    def store(self):
        return _EnvDict()


class FileBasedStore(TorqeSubmitStore):

    def load(self):
        if os.environ.get("__PY_T_{}".format("STORE")) != "FILE":
            raise StoreNotUsed()
        import pickle
        with open(os.environ['__PY_T_FILE']) as f:
            self.__store = pickle.load(f)

    @property
    def store(self):
        return self.__store

    @classmethod
    def get_tempdir(self):
        return os.environ.get("__PY_T_TEMPDIR", gettempdir())

    @classmethod
    def save_store(self, store):
        import pickle
        opened, file = mkstemp(dir=self.get_tempdir())
        with open(file, 'w') as f:
            pickle.dump(store, f)
            f.close()
        return {"__PY_T_FILE": file, "__PY_T_STORE": "FILE"}
