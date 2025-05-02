import tkinter.messagebox as messagebox

from constants.constants import ErrorsParams


class GUIAdapter:
    def __init__(self, parent):
        self.parent = parent

    def show_askyesno(self, title, message) -> bool:
        answer = messagebox.askyesno(title, message)
        return answer

    def show_error(self, title=ErrorsParams.ERROR_WINDOW_NAME, message="Error"):
        messagebox.showerror(title, message)

    def get_fields_data(self):
        record_date = self.parent.frame.dataframe.date_entry.get()
        record_type = self.parent.frame.dataframe.type_combobox.get()
        record_name = "; ".join(
            sorted(self.parent.frame.dataframe.name_text.get("1.0", "end-1c").strip("\n").split("\n"))
        )
        record_communication = "; ".join(
            sorted(self.parent.frame.dataframe.communication_text.get("1.0", "end-1c").strip("\n").split("\n"))
        )
        record_from = self.parent.frame.dataframe.from_entry.get()
        record_who = self.parent.frame.dataframe.who_entry.get()
        record_description = self.parent.frame.dataframe.description_text.get("1.0", "end-1c")
        record_note = self.parent.frame.dataframe.note_text.get("1.0", "end-1c")
        record_author = self.parent.frame.dataframe.author_combobox.get()
        record_status = self.parent.frame.dataframe.record_status.get()

        return (
            record_date,
            record_type,
            record_name,
            record_communication,
            record_from,
            record_who,
            record_description,
            record_note,
            record_author,
            record_status,
        )
