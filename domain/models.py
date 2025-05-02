from dataclasses import dataclass


@dataclass
class Record:
    def __init__(
        self,
        id_: str,
        date: str,
        type_: str,
        name: str,
        communication: str,
        from_: str,
        who: str,
        description: str,
        note: str,
        author: str,
        status: bool,
    ):
        self.record_id = id_
        self.record_date = date
        self.record_type = type_
        self.record_name = name
        self.record_communication = communication
        self.record_from = from_
        self.record_who = who
        self.record_description = description
        self.record_note = note
        self.record_author = author
        self.record_status = status
