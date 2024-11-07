"""
Patrick Leonard
CIS 121 Final Project
"""
import re

from .catalog_object import CatalogObject
from .section import Section


class Course(CatalogObject):
    """Represents a Subject within a Term (e.g. CIS, MATH, ACCT)"""

    #def get_all_sections_without_zero_capacity(self):


    def get_all_open_sections(self):
        return self._filter(lambda section: not section.is_full())

    def get_all_sections(self) -> list:
        """Call this method to get all available Course objects within parent Subject."""
        return self.children

    def get_section(self, section_number):
        """Pass in a string, like "122" or "144W" to retrieve a course within a Subject instance."""
        return self._get_child(section_number)

    def pretty_print(self):
        raise NotImplementedError

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def credits(self):
        return self._credits

    @property
    def session_type(self):
        return self._session_type

    # Internal Components Below This Line - No Touchy
    def _initialize_from_raw_data(self, raw_data):
        self._id = self._strip_subject(raw_data["@num"])
        self._name = raw_data["@title"]
        self._credits = raw_data["@credits"]
        self._session_type = raw_data["@sessiontype"]
        self._instantiate_children(self._ensure_is_list(raw_data["section"]))

    def _create_child(self, raw_data):
        return Section(raw_data, self)

    def _strip_subject(self, raw_course_num):
        return re.sub(r'^\D+', '', raw_course_num)

    def _filter(self, funct):
        output = []
        for obj in self.children:
            if funct(obj):
                output.append(obj)
        return output
