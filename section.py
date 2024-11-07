"""
Patrick Leonard
CIS 121 Final Project
"""

from .catalog_object import CatalogObject
from .meeting import Meeting

class Section(CatalogObject):
    """Represents a Subject within a Term (e.g. CIS, MATH, ACCT)"""

    def get_all_meetings(self) -> list:
        """Call this method to get all available Course objects within parent Subject."""
        return self.children

    def get_section(self, section_number):
        """Pass in a string, like "122" or "144W" to retrieve a course within a Subject instance."""
        return self._get_child(section_number)

    def pretty_print(self):
        return str(self)

    def is_weird(self) -> bool:
        return any([m.is_weird() for m in self.children])

    def is_full(self) -> bool:
        raise NotImplementedError

    def is_online(self) -> bool:
        raise NotImplementedError

    def is_permission_required(self) -> bool:
        raise NotImplementedError

    @property
    def id(self):
        """The lookup for this section. The "02" in CIS334-02."""
        return self._id

    @property
    def registration_id(self):
        """The unique ID assigned to every section by the University. Used for registration."""
        return self._registration_id

    @property
    def grading_method(self):
        """The grading method used for the section. Of dubious use, but here it is."""
        return self._grading_method

    @property
    def capacity(self):
        """The maximum capacity of the section."""
        return self._capacity

    @property
    def seated(self):
        """The number of registered students."""
        return self._seated

    # @property
    # def online(self):
    #     """Useless. """
    #     return self._online

    @property
    def notes(self):
        """If any notes are attached to a section, they're stored here."""
        return self._notes

    # Internal Components Below This Line - No Touchy
    def __str__(self):
        return (f"({self.registration_id}) Section {self.id} of {self.parent.parent.id}{self.parent.id}" +
              f" - {self.seated}/{self.capacity} students.")

    def _initialize_from_raw_data(self, raw_data):
        self._id = raw_data["@section"]
        self._registration_id = raw_data["@courseid"]
        self._grading_method = raw_data["@gradingmethod"]
        self._capacity = raw_data["@capacity"]
        self._seated = raw_data["@seated"]
        # self._online = raw_data["@online"]
        self._notes = []

        self._parse_note_data(raw_data)
        raw_meeting_data_list = self._ensure_is_list(raw_data["meeting"])
        self._instantiate_children(raw_meeting_data_list)

    def _create_child(self, raw_data):
        return Meeting(raw_data, self)

    def _parse_note_data(self, raw_data):
        if "note" in raw_data:
            raw_note_data = self._ensure_is_list(raw_data["note"])
            self._notes = [note["#text"] for note in raw_note_data]
