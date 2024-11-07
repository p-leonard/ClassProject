"""
Patrick Leonard
CIS 121 Final Project
"""

from .catalog_object import CatalogObject
from .subject import Subject

class Term(CatalogObject):
    """Represents a Term at MNSU (e.g. Spring 2025)"""

    @staticmethod
    def get_all_terms() -> list:
        """Call this method to get all available Term objects."""
        output = []
        list_of_terms = Term._fetch_term_raw_data()
        for term_data in list_of_terms:
            output.append(Term(term_data, None))
        return output

    def get_subject(self, subject_code:str) -> Subject:
        """Pass in a string, like 'ACCT' or 'CIS' to get the corresponding Subject object."""
        child = self._get_child(subject_code)
        return child

    def pretty_print(self):
        raise NotImplementedError

    def get_all_subjects(self) -> list:
        return self.children

    # Internal Components Below This Line - No Touchy
    _EXCLUDED_SUBJECT_CODES = ["AOS", "MACC"]

    def _initialize_from_raw_data(self, raw_data):
        self._id = raw_data["@yrtr"]
        self._name = raw_data["#text"]
        self._instantiate_children(self._fetch_subject_list())

    @staticmethod
    def _fetch_term_raw_data() -> list[dict]:
        """
        If data is cached, returns term data.
        Otherwise, downloads, caches, then returns term data.
        """
        args = {"action": "terms"}
        response = Term._fetch_raw_data(args)["termlist"]["term"]
        Term._CACHED_AVAILABLE_TERM_DATA = Term._ensure_is_list(response)
        return Term._CACHED_AVAILABLE_TERM_DATA

    def _fetch_subject_list(self) -> list[dict]:
        """Downloads and stores all subject codes available from API, excluding given subjects"""
        args = {"action": "subjects", "term": self.obj_id}
        response = Term._fetch_raw_data(args)["subjectlist"]["subject"]
        return [out for out in response if out["@symbol"] not in self._EXCLUDED_SUBJECT_CODES]

    def _create_child(self, raw_data) -> "Subject":
        return Subject(raw_data, self)
