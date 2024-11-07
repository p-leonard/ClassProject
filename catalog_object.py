"""
Patrick Leonard
CIS 121 Final Project
"""

from abc import ABC, abstractmethod

import xmltodict
import requests

class CatalogObject(ABC):
    """An abstract base class that defines MNSU course catalog objects."""

    def __init__(self, raw_data: dict, parent):
        self._children = []
        self._parent = parent
        self._id = None
        self._name = None
        self._initialize_from_raw_data(raw_data)

        assert self.obj_id is not None
        self._name = self.obj_id if self.name is None else self.name

    def __len__(self):
        return len(self._children)

    def _get_child(self, obj_id) -> "CatalogObject":
        obj = next((c for c in self._children if c.id == obj_id), None)
        if obj is None:
            raise ValueError(f"Invalid ID: {obj_id}")
        return obj


    def _instantiate_children(self, raw_data_list: list) -> None:
        for entry in raw_data_list:
            self.children.append(self._create_child(entry))

    @abstractmethod
    def _create_child(self, raw_data: dict) -> 'CatalogObject':
        raise NotImplementedError("This method should be implemented in child class.")

    @abstractmethod
    def _initialize_from_raw_data(self, raw_data: dict) -> None:
        raise NotImplementedError("This method should be implemented in child class.")

    @staticmethod
    def _fetch_raw_data(args: dict) -> dict:
        """
        Sends a request to the MNSU API with specified arguments.
        The API response is formatted as XML which is converted
        to a dict and passed to the caller.

        :param args: dictionary of HTML query parameters
        :return: parsed XML response in dictionary format
        """
        url = "https://secure2.mnsu.edu/coursescheduledata/direct.ashx"

        for idx, arg in enumerate(args):
            prefix = "?" if idx == 0 else "&"
            url += prefix + arg + '=' + str(args[arg])

        response = requests.get(url, timeout=5)
        response.raise_for_status()

        return xmltodict.parse(response.text)

    @staticmethod
    def _ensure_is_list(obj) -> list:
        if isinstance(obj, list):
            return obj
        return [obj, ]

    @property
    def obj_id(self) -> str:
        """Returns the object id."""
        return self._id

    @property
    def name(self) -> str:
        """Returns the object name. If no name is provided during creation, is equal to id."""
        return self._name

    @property
    def parent(self) -> 'CatalogObject':
        """Returns the parent object."""
        return self._parent

    @property
    def children(self) -> list['CatalogObject']:
        """Returns a list of child objects."""
        return self._children

    def get_name(self):
        return self.name

    def get_id(self):
        return self.obj_id

    def get_parent(self):
        return self.parent

    def get_children(self):
        return self.children