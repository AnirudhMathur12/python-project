from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Static, ListView, ListItem, Label, Input, Button
from textual.containers import Container, Vertical, Horizontal, VerticalScroll
from textual.screen import Screen
from textual import events

import mysql.connector
import pandas
import pickle
import os

DATABASE_NAME = "USEMP_DB"
STUDENT_TABLE_NAME = "STUDENT_USEMP_TBL"
EXAM_TABLE_NAME = "EXAMINATION_USEMP_TBL"
FILENAME = "login-cred.usemp"


class login:
    def __init__(self, uname, password):
        self.uname = uname
        self.password = password


def SQL_INIT():
    global con, cur
    if FILENAME in os.listdir('.'):
        with open(FILENAME, 'rb') as fb:
            login_cred = pickle.load(fb)
    else:
        user = input("Enter username: ")
        pw = input("Enter password: ")
        login_cred = login(user, pw)
        with open(FILENAME, 'wb') as fb:
            pickle.dump(login_cred, fb)

    con = mysql.connector.connect(user=login_cred.uname, password=login_cred.password, host="localhost")
    cur = con.cursor()

    cur.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE_NAME}")
    cur.execute(f"USE {DATABASE_NAME}")
    cur.execute(f"CREATE TABLE IF NOT EXISTS `{STUDENT_TABLE_NAME}` (Student_ID INT PRIMARY KEY, Name VARCHAR(30) NOT NULL, SLOT ENUM('MORNING', 'EVENING') NOT NULL)")
    cur.execute(f"CREATE TABLE IF NOT EXISTS `{EXAM_TABLE_NAME}` (EXAM_ID INT PRIMARY KEY, Student_ID INT, FOREIGN KEY (Student_ID) REFERENCES `{STUDENT_TABLE_NAME}`(Student_ID), PHYSICS INT, CHEMISTRY INT, MATH INT, PYTHON INT, EXAM ENUM('CAT1', 'CAT2', 'FAT'))")
    con.commit()


# ------------------- Input Screens -------------------

class AddStudentScreen(Screen):
    CSS = """
    AddStudentScreen {
        align: center middle;
    }
    
    #dialog {
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    
    Input {
        margin: 1 0;
    }
    
    Button {
        margin: 1 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Add Student", classes="centered")
            yield Label("Student ID:")
            yield Input(placeholder="Enter Student ID", id="student_id")
            yield Label("Name:")
            yield Input(placeholder="Enter Name", id="name")
            yield Label("Slot (MORNING/EVENING):")
            yield Input(placeholder="Enter Slot", id="slot")
            with Horizontal():
                yield Button("Submit", variant="primary", id="submit")
                yield Button("Cancel", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            try:
                sid = int(self.query_one("#student_id", Input).value)
                name = self.query_one("#name", Input).value
                slot = self.query_one("#slot", Input).value.upper()
                
                cur.execute(f"INSERT INTO {STUDENT_TABLE_NAME} VALUES (%s, %s, %s)", (sid, name, slot))
                con.commit()
                self.app.pop_screen()
                self.app.notify("Student added successfully!")
            except Exception as e:
                self.app.notify(f"Error: {str(e)}", severity="error")
        else:
            self.app.pop_screen()


class DeleteStudentScreen(Screen):
    CSS = """
    DeleteStudentScreen {
        align: center middle;
    }
    
    #dialog {
        width: 50;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Delete Student", classes="centered")
            yield Label("Student ID:")
            yield Input(placeholder="Enter Student ID to delete", id="student_id")
            with Horizontal():
                yield Button("Delete", variant="error", id="submit")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            try:
                sid = int(self.query_one("#student_id", Input).value)
                cur.execute(f"DELETE FROM {STUDENT_TABLE_NAME} WHERE Student_ID=%s", (sid,))
                con.commit()
                self.app.pop_screen()
                self.app.notify("Student deleted successfully!")
            except Exception as e:
                self.app.notify(f"Error: {str(e)}", severity="error")
        else:
            self.app.pop_screen()


class AddExamScreen(Screen):
    CSS = """
    AddExamScreen {
        align: center middle;
    }
    
    #dialog {
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Add Exam Record", classes="centered")
            yield Label("Exam ID:")
            yield Input(placeholder="Enter Exam ID", id="exam_id")
            yield Label("Student ID:")
            yield Input(placeholder="Enter Student ID", id="student_id")
            yield Label("Exam Type (CAT1/CAT2/FAT):")
            yield Input(placeholder="Enter Exam Type", id="exam_type")
            yield Label("Physics Marks:")
            yield Input(placeholder="Enter Physics marks", id="physics")
            yield Label("Chemistry Marks:")
            yield Input(placeholder="Enter Chemistry marks", id="chemistry")
            yield Label("Math Marks:")
            yield Input(placeholder="Enter Math marks", id="math")
            yield Label("Python Marks:")
            yield Input(placeholder="Enter Python marks", id="python")
            with Horizontal():
                yield Button("Submit", variant="primary", id="submit")
                yield Button("Cancel", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            try:
                eid = int(self.query_one("#exam_id", Input).value)
                sid = int(self.query_one("#student_id", Input).value)
                exam_type = self.query_one("#exam_type", Input).value.upper()
                phy = int(self.query_one("#physics", Input).value)
                chem = int(self.query_one("#chemistry", Input).value)
                math = int(self.query_one("#math", Input).value)
                py = int(self.query_one("#python", Input).value)
                
                cur.execute(f"INSERT INTO {EXAM_TABLE_NAME} VALUES (%s,%s,%s,%s,%s,%s,%s)",
                           (eid, sid, phy, chem, math, py, exam_type))
                con.commit()
                self.app.pop_screen()
                self.app.notify("Exam record added successfully!")
            except Exception as e:
                self.app.notify(f"Error: {str(e)}", severity="error")
        else:
            self.app.pop_screen()


class UpdateExamScreen(Screen):
    CSS = """
    UpdateExamScreen {
        align: center middle;
    }
    
    #dialog {
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Update Exam Marks", classes="centered")
            yield Label("Exam ID:")
            yield Input(placeholder="Enter Exam ID", id="exam_id")
            yield Label("Subject (PHYSICS/CHEMISTRY/MATH/PYTHON):")
            yield Input(placeholder="Enter Subject", id="subject")
            yield Label("New Mark:")
            yield Input(placeholder="Enter new mark", id="new_mark")
            with Horizontal():
                yield Button("Update", variant="primary", id="submit")
                yield Button("Cancel", variant="error", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            try:
                eid = int(self.query_one("#exam_id", Input).value)
                sub = self.query_one("#subject", Input).value.upper()
                new_mark = int(self.query_one("#new_mark", Input).value)
                
                cur.execute(f"UPDATE {EXAM_TABLE_NAME} SET {sub}=%s WHERE EXAM_ID=%s", (new_mark, eid))
                con.commit()
                self.app.pop_screen()
                self.app.notify("Exam marks updated successfully!")
            except Exception as e:
                self.app.notify(f"Error: {str(e)}", severity="error")
        else:
            self.app.pop_screen()


class DeleteExamScreen(Screen):
    CSS = """
    DeleteExamScreen {
        align: center middle;
    }
    
    #dialog {
        width: 50;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Delete Exam Record", classes="centered")
            yield Label("Exam ID:")
            yield Input(placeholder="Enter Exam ID to delete", id="exam_id")
            with Horizontal():
                yield Button("Delete", variant="error", id="submit")
                yield Button("Cancel", id="cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "submit":
            try:
                eid = int(self.query_one("#exam_id", Input).value)
                cur.execute(f"DELETE FROM {EXAM_TABLE_NAME} WHERE EXAM_ID=%s", (eid,))
                con.commit()
                self.app.pop_screen()
                self.app.notify("Exam record deleted successfully!")
            except Exception as e:
                self.app.notify(f"Error: {str(e)}", severity="error")
        else:
            self.app.pop_screen()


class ViewStudentsScreen(Screen):
    BINDINGS = [
        ("escape", "dismiss", "Close"),
        ("q", "dismiss", "Close")
    ]
    
    CSS = """
    ViewStudentsScreen {
        align: center middle;
    }
    
    #dialog {
        width: 80;
        height: 80%;
        border: thick $background 80%;
        background: $surface;
    }
    
    #content {
        height: 1fr;
        border: solid $primary;
        margin: 1;
    }
    
    #header {
        background: $boost;
        padding: 1;
    }
    
    #button-container {
        height: auto;
        align: center middle;
        padding: 1;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Students List - Press ESC or Q to close", id="header")
            with VerticalScroll(id="content"):
                cur.execute(f"SELECT * FROM {STUDENT_TABLE_NAME}")
                data = cur.fetchall()
                
                if not data:
                    yield Static("No students found.")
                else:
                    yield Static(f"{'ID':<20}{'Name':<20}{'Slot':<20}")
                    yield Static("-" * 60)
                    for s in data:
                        yield Static(f"{s[0]:<20}{s[1]:<20}{s[2]:<20}")
            with Horizontal(id="button-container"):
                yield Button("Close", id="close", variant="primary")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss()
        
    def action_dismiss(self) -> None:
        self.dismiss()


class SearchStudentScreen(Screen):
    CSS = """
    SearchStudentScreen {
        align: center middle;
    }

    #dialog {
        width: 60;
        height: auto;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    """

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Search Student", classes="centered")
            yield Label("Search by ID or partial Name:")
            yield Input(id="query", placeholder="Enter ID or name")
            with Horizontal():
                yield Button("Search", id="search", variant="primary")
                yield Button("Cancel", id="cancel", variant="error")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "search":
            q = self.query_one("#query", Input).value.strip()

            try:
                # If digits, treat as exact ID search
                if q.isdigit():
                    cur.execute(f"SELECT * FROM {STUDENT_TABLE_NAME} WHERE Student_ID=%s", (int(q),))
                else:
                    cur.execute(f"SELECT * FROM {STUDENT_TABLE_NAME} WHERE Name LIKE %s", (f"%{q}%",))

                rows = cur.fetchall()
                self.app.push_screen(SearchStudentResultScreen(rows))
            except Exception as e:
                self.app.notify(f"Error: {str(e)}", severity="error")
        else:
            self.app.pop_screen()


class SearchStudentResultScreen(Screen):
    CSS = """
    SearchStudentResultScreen {
        align: center middle;
    }

    #dialog {
        width: 80%;
        height: 80%;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }

    #content {
        height: 1fr;
        overflow-y: auto;
        border: solid $primary;
    }
    """

    def __init__(self, rows):
        super().__init__()
        self.rows = rows

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Static("Search Results", classes="centered")
            with VerticalScroll(id="content"):
                if not self.rows:
                    yield Static("No matching students found.")
                else:
                    yield Static(f"{'ID':<20}{'Name':<20}{'Slot':<20}")
                    yield Static("-" * 60)
                    for s in self.rows:
                        yield Static(f"{s[0]:<20}{s[1]:<20}{s[2]:<20}")
            yield Button("Close", id="close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()


class ViewExamsScreen(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Close")]
    
    CSS = """
    ViewExamsScreen {
        align: center middle;
    }
    
    #dialog {
        width: 90%;
        height: 80%;
        border: thick $background 80%;
        background: $surface;
        padding: 1 2;
    }
    
    #content {
        height: 1fr;
        overflow-y: auto;
        border: solid $primary;
    }
    """

    def compose(self) -> ComposeResult:
        cur.execute(f"""SELECT e.EXAM_ID, s.Name, e.Student_ID, e.EXAM, e.PHYSICS, e.CHEMISTRY, e.MATH, e.PYTHON
                        FROM {EXAM_TABLE_NAME} e
                        JOIN {STUDENT_TABLE_NAME} s ON e.Student_ID = s.Student_ID""")
        data = cur.fetchall()
        
        with Vertical(id="dialog"):
            yield Static("Exam Records", classes="centered")
            with Vertical(id="content"):
                if not data:
                    yield Static("No exam records found.")
                else:
                    for row in data:
                        yield Static(f"Exam ID: {row[0]}, Name: {row[1]}, Student ID: {row[2]}, Exam: {row[3]}")
                        yield Static(f"  Physics: {row[4]}, Chemistry: {row[5]}, Math: {row[6]}, Python: {row[7]}")
            yield Button("Close", id="close")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.app.pop_screen()


# ------------------- Database functions (for CSV operations) -------------------

def write_to_csv():
    cur.execute(f"SELECT * FROM {STUDENT_TABLE_NAME}")
    students = cur.fetchall()
    df = pandas.DataFrame(students, columns=[desc[0] for desc in cur.description])
    df.to_csv("students.csv", index=False)

    cur.execute(f"SELECT * FROM {EXAM_TABLE_NAME}")
    exams = cur.fetchall()
    df = pandas.DataFrame(exams, columns=[desc[0] for desc in cur.description])
    df.to_csv("exams.csv", index=False)


def import_from_csv():
    df = pandas.read_csv("students.csv")
    for _, row in df.iterrows():
        cur.execute(
            f"INSERT INTO `{STUDENT_TABLE_NAME}` (Student_ID, Name, SLOT) VALUES (%s, %s, %s)",
            (int(row['Student_ID']), row['Name'], row['SLOT'])
        )
    con.commit()


class MenuApp(App):
    CSS = """
    .centered {
        text-align: center;
        width: 100%;
        content-align: center middle;
    }
    
    #menu {
        width: 80%;
        height: 80%;
        margin: 2 4;
    }
    """

    def compose(self) -> ComposeResult:
        yield Header()
        yield Container(
            Static("VIT STUDENT EXAMINATION MANAGEMENT PORTAL", classes="centered"),
            ListView(
                ListItem(Label("1. Add Student")),
                ListItem(Label("2. View Students")),
                ListItem(Label("3. Delete Student")),
                ListItem(Label("4. Add Exam Record")),
                ListItem(Label("5. View Exam Records")),
                ListItem(Label("6. Update Exam Marks")),
                ListItem(Label("7. Delete Exam Record")),
                ListItem(Label("8. Export Data to CSV")),
                ListItem(Label("9. Import Data from CSV")),
                ListItem(Label("10. Search Student")),
                ListItem(Label("11. Exit")),
                id="menu"
            )
        )
        yield Footer()

    async def on_list_view_selected(self, event: ListView.Selected) -> None:
        index = event.list_view.index
        if index == 0:
            self.push_screen(AddStudentScreen())
        elif index == 1:
            self.push_screen(ViewStudentsScreen())
        elif index == 2:
            self.push_screen(DeleteStudentScreen())
        elif index == 3:
            self.push_screen(AddExamScreen())
        elif index == 4:
            self.push_screen(ViewExamsScreen())
        elif index == 5:
            self.push_screen(UpdateExamScreen())
        elif index == 6:
            self.push_screen(DeleteExamScreen())
        elif index == 7:
            try:
                write_to_csv()
                self.notify("Data exported to CSV successfully!")
            except Exception as e:
                self.notify(f"Error: {str(e)}", severity="error")
        elif index == 8:
            try:
                import_from_csv()
                self.notify("Data imported from CSV successfully!")
            except Exception as e:
                self.notify(f"Error: {str(e)}", severity="error")
        elif index == 9:
            self.push_screen(SearchStudentScreen())
        elif index == 10:
            await self.action_quit()


def main():
    SQL_INIT()
    MenuApp().run()
    cur.close()
    con.close()


if __name__ == "__main__":
    main()
