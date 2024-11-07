"""
Patrick Leonard
CIS 121 Final Project
"""

from .catalog_object import CatalogObject
from .course import Course

class Subject(CatalogObject):
    """Represents a Subject within a Term (e.g. CIS, MATH, ACCT)"""

    def get_all_courses(self) -> list[CatalogObject]:
        self._download_and_populate_data()
        return self.children

    def get_course(self, course_number):
        """Pass in a string, like "122" or "144W" to retrieve a course within a Subject instance."""
        self._download_and_populate_data()
        return self._get_child(course_number)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    # Internal Components Below This Line - No Touchy
    def __len__(self):
        self._download_and_populate_data()
        super().__len__()

    def _initialize_from_raw_data(self, raw_data):
        self.is_data_downloaded = False
        self._id = raw_data["@symbol"]
        self._name = raw_data["#text"] if "#text" in raw_data else self.obj_id

    def _create_child(self, raw_data):
        return Course(raw_data, self)

    def _download_and_populate_data(self):
        if not self.is_data_downloaded:
            fetched_data = self._fetch_raw_subject_data()
            self._instantiate_children(fetched_data[0]["course"])
            self.is_data_downloaded = True

    def _fetch_raw_subject_data(self):
        args = {"action": "courses", "term": self.parent.obj_id, "subject": self.obj_id}
        return self._ensure_is_list(self._fetch_raw_data(args)["courselists"]["courselist"])
