import sys
import json
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QPushButton, QLineEdit, QComboBox,
    QLabel, QListWidgetItem, QDateEdit, QProgressBar
)
from PyQt6.QtCore import Qt, QDate

FILE = "tasks_pro.json"


def load_tasks():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, indent=4)


class TodoPro(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Smart To-Do PRO 🚀")
        self.setGeometry(200, 150, 550, 650)

        self.tasks = load_tasks()

        layout = QVBoxLayout()

        # Title
        title = QLabel("🚀 Smart To-Do PRO")
        title.setStyleSheet("font-size:20px;font-weight:bold;")
        layout.addWidget(title)

        # Input
        self.input = QLineEdit()
        self.input.setPlaceholderText("Task name...")
        layout.addWidget(self.input)

        # Priority
        self.priority = QComboBox()
        self.priority.addItems(["Low", "Medium", "High"])
        layout.addWidget(self.priority)

        # Deadline
        self.date = QDateEdit()
        self.date.setDate(QDate.currentDate())
        self.date.setCalendarPopup(True)
        layout.addWidget(self.date)

        # Add button
        self.add_btn = QPushButton("Add Task")
        self.add_btn.clicked.connect(self.add_task)
        layout.addWidget(self.add_btn)

        # Progress bar
        self.progress = QProgressBar()
        layout.addWidget(self.progress)

        # List
        self.list_widget = QListWidget()
        self.list_widget.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        layout.addWidget(self.list_widget)

        # Buttons
        btns = QHBoxLayout()

        self.done_btn = QPushButton("Toggle Done")
        self.del_btn = QPushButton("Delete")

        self.done_btn.clicked.connect(self.toggle_done)
        self.del_btn.clicked.connect(self.delete_task)

        btns.addWidget(self.done_btn)
        btns.addWidget(self.del_btn)

        layout.addLayout(btns)

        self.setLayout(layout)

        self.refresh()

        self.setStyleSheet("""
            QWidget { background:#0f172a; color:white; }
            QLineEdit, QComboBox, QDateEdit {
                background:#1e293b; padding:8px; border-radius:8px;
            }
            QPushButton {
                background:#3b82f6; padding:8px; border-radius:8px;
            }
            QPushButton:hover { background:#2563eb; }
            QListWidget { background:#111827; border-radius:10px; }
        """)

    # ➕ add task
    def add_task(self):
        text = self.input.text().strip()
        if not text:
            return

        task = {
            "text": text,
            "priority": self.priority.currentText(),
            "deadline": self.date.date().toString("yyyy-MM-dd"),
            "done": False
        }

        self.tasks.append(task)
        save_tasks(self.tasks)

        self.input.clear()
        self.refresh()

    # ✔ toggle done
    def toggle_done(self):
        i = self.list_widget.currentRow()
        if i >= 0:
            self.tasks[i]["done"] = not self.tasks[i]["done"]
            save_tasks(self.tasks)
            self.refresh()

    # 🗑 delete
    def delete_task(self):
        i = self.list_widget.currentRow()
        if i >= 0:
            self.tasks.pop(i)
            save_tasks(self.tasks)
            self.refresh()

    # 📊 progress
    def update_progress(self):
        if not self.tasks:
            self.progress.setValue(0)
            return

        done = len([t for t in self.tasks if t["done"]])
        percent = int((done / len(self.tasks)) * 100)
        self.progress.setValue(percent)

    # 🔄 refresh UI
    def refresh(self):
        self.list_widget.clear()

        for t in self.tasks:
            text = t["text"]
            pr = t["priority"]
            dl = t["deadline"]
            done = t["done"]

            show = f"{text} | {pr} | {dl}"
            if done:
                show = "✔ " + show

            item = QListWidgetItem(show)

            if pr == "High":
                item.setForeground(Qt.GlobalColor.red)
            elif pr == "Medium":
                item.setForeground(Qt.GlobalColor.yellow)
            else:
                item.setForeground(Qt.GlobalColor.green)

            self.list_widget.addItem(item)

        self.update_progress()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TodoPro()
    w.show()
    sys.exit(app.exec())
