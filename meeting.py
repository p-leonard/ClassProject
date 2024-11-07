"""
Patrick Leonard
CIS 121 Final Project
"""

from .catalog_object import CatalogObject


class Meeting(CatalogObject):
    """Represents a Meeting within a Section"""

    def pretty_print(self):
        return f"Meeting: Days={self.days}, Start={self.start_time}, End={self.end_time}, Location={self.location}, Instructor={self.instructor}"

    def conflicts_with(self, meeting) -> bool:
        if not self._do_dates_overlap(meeting): return False
        if not self._do_days_overlap(meeting): return False
        if not self._do_times_overlap(meeting):return False
        return True

    def is_weird(self) -> bool:
        """Returns true if not useful for automatic schedule generation."""
        return all([self.days == "", self.start_time == "", self.end_time == ""]) or self.instructor == "Staff Unassigned"

    @property
    def days(self):
        return self._days

    @property
    def start_time(self):
        return self._start_time

    @property
    def end_time(self):
        return self._end_time

    @property
    def start_date(self):
        return self._start_date

    @property
    def end_date(self):
        return self._end_date

    @property
    def location(self):
        return self._location

    @property
    def instructor(self):
        return self._instructor

    # Internal Components Below This Line - No Touchy
    def _initialize_from_raw_data(self, raw_data):
        self._id = "blank"
        self._days = raw_data["@days"].replace(" ","")
        self._start_time = raw_data["@starttime"]
        self._end_time = raw_data["@endtime"]
        self._start_date = raw_data["@startdate"]
        self._end_date = raw_data["@enddate"]
        self._location = raw_data["@location"]
        self._instructor = raw_data["@instructor"]

    def _create_child(self, raw_data):
        raise NotImplementedError("Cannot get children of Meeting")

    def _do_days_overlap(self, meeting):
        if self._parse_days(self.days).isdisjoint(self._parse_days(meeting.days)):
            return False
        return True

    def _do_times_overlap(self, meeting):
        if not all([self.start_time, self.end_time, meeting.start_time, meeting.end_time]):
            return False
        return ((int(self.start_time) <= int(meeting.end_time)) and (
                int(self.end_time) >= int(meeting.start_time)))

    def _do_dates_overlap(self, meeting):
        if self.start_date == "" or meeting.start_date == "":
            return False
        a_start = self._parse_date(self.start_date)
        a_end = self._parse_date(self.end_date)
        b_start = self._parse_date(meeting.start_date)
        b_end = self._parse_date(meeting.end_date)
        return (a_start <= b_end) and (a_end >= b_start)

    @staticmethod
    def _parse_days(day_string):
        day_string = day_string.replace(" ", "")
        output = set()
        for char in day_string:
            match char:
                case 'M':
                    output.add("Monday")
                case 'T':
                    output.add("Tuesday")
                case 'W':
                    output.add("Wednesday")
                case 'H':
                    output.add("Thursday")
                case 'F':
                    output.add("Friday")
                case 'S':
                    output.add("Saturday")
        return output