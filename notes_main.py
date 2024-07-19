import sys
import json
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QListWidget, QPushButton, QLabel, QTextEdit, QMessageBox

initial_notes = {
    "Инструкция": {
        "теги": ["инструкция", "начало"],
        "текст": "Это пример заметки. Используйте это приложение для управления вашими заметками."
    }
}

with open('notes_data.json', 'w', encoding='utf-8') as file:
    json.dump(initial_notes, file, ensure_ascii=False, indent=4)

class SmartNotesApp(QWidget):
    def __init__(self):
        super().__init__()
        self.notes = {}
        self.initUI()
        self.load_notes()

    def initUI(self):
        self.setWindowTitle('Умные заметки')

        self.note_label = QLabel('Название заметки:')
        self.note_input = QLineEdit(self)
        self.notes_list = QListWidget(self)
        self.add_button = QPushButton('Создать заметку', self)
        self.delete_button = QPushButton('Удалить заметку', self)
        self.save_button = QPushButton('Сохранить заметку', self)
        self.search_button = QPushButton('Искать по тегу', self)

        self.tag_label = QLabel('Теги:')
        self.tag_input = QLineEdit(self)
        self.text_label = QLabel('Текст заметки:')
        self.text_edit = QTextEdit(self)

        self.add_button.clicked.connect(self.add_note)
        self.delete_button.clicked.connect(self.del_note)
        self.save_button.clicked.connect(self.save_note)
        self.search_button.clicked.connect(self.search_note)
        self.notes_list.itemClicked.connect(self.show_results)

        main_layout = QVBoxLayout()

        note_layout = QHBoxLayout()
        note_layout.addWidget(self.note_label)
        note_layout.addWidget(self.note_input)
        main_layout.addLayout(note_layout)

        list_button_layout = QHBoxLayout()
        list_button_layout.addWidget(self.notes_list)

        button_layout = QVBoxLayout()
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.save_button)
        button_layout.addWidget(self.search_button)
        list_button_layout.addLayout(button_layout)

        main_layout.addLayout(list_button_layout)

        tag_layout = QHBoxLayout()
        tag_layout.addWidget(self.tag_label)
        tag_layout.addWidget(self.tag_input)
        main_layout.addLayout(tag_layout)

        main_layout.addWidget(self.text_label)
        main_layout.addWidget(self.text_edit)

        self.setLayout(main_layout)
        self.resize(400, 300)

    def load_notes(self):
        try:
            with open('notes_data.json', 'r', encoding='utf-8') as file:
                self.notes = json.load(file)
                self.notes_list.addItems(self.notes.keys())
        except Exception as e:
            QMessageBox.warning(self, "Ошибка", f"Не удалось загрузить заметки: {e}")

    def add_note(self):
        note_title = self.note_input.text()
        if note_title:
            if note_title not in self.notes:
                self.notes[note_title] = {"теги": [], "текст": ""}
                self.notes_list.addItem(note_title)
                self.note_input.clear()
                self.save_to_file()
            else:
                QMessageBox.warning(self, "Предупреждение", "Заметка с таким названием уже существует!")
        else:
            QMessageBox.warning(self, "Предупреждение", "Название заметки не может быть пустым!")

    def del_note(self):
        selected_items = self.notes_list.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "Предупреждение", "Выберите заметку для удаления!")
            return
        for item in selected_items:
            note_title = item.text()
            del self.notes[note_title]
            self.notes_list.takeItem(self.notes_list.row(item))
        self.clear_note_details()
        self.save_to_file()

    def save_note(self):
        current_note = self.notes_list.currentItem()
        if current_note:
            note_title = current_note.text()
            new_note_title = self.note_input.text().strip()
            if new_note_title and new_note_title != note_title:
                if new_note_title not in self.notes:
                    self.notes[new_note_title] = self.notes.pop(note_title)
                    self.notes_list.currentItem().setText(new_note_title)
                    note_title = new_note_title
                else:
                    QMessageBox.warning(self, "Предупреждение", "Заметка с таким названием уже существует!")
                    return
            self.notes[note_title]["теги"] = self.tag_input.text().split(", ")
            self.notes[note_title]["текст"] = self.text_edit.toPlainText()
            self.save_to_file()
            QMessageBox.information(self, "Информация", "Заметка сохранена!")
        else:
            QMessageBox.warning(self, "Предупреждение", "Выберите заметку для сохранения!")

    def show_results(self):
        current_note = self.notes_list.currentItem()
        if current_note:
            note_title = current_note.text()
            note_details = self.notes[note_title]
            self.note_input.setText(note_title)
            self.tag_input.setText(", ".join(note_details["теги"]))
            self.text_edit.setText(note_details["текст"])

    def clear_note_details(self):
        self.note_input.clear()
        self.tag_input.clear()
        self.text_edit.clear()

    def save_to_file(self):
        with open('notes_data.json', 'w', encoding='utf-8') as file:
            json.dump(self.notes, file, ensure_ascii=False, indent=4)

    def search_note(self):
        if self.search_button.text() == "Искать по тегу":
            search_tag = self.tag_input.text().strip()
            if search_tag:
                filtered_notes = {k: v for k, v in self.notes.items() if search_tag in v["теги"]}
                self.notes_list.clear()
                self.notes_list.addItems(filtered_notes.keys())
                self.search_button.setText("Сбросить поиск")
            else:
                QMessageBox.warning(self, "Предупреждение", "Введите тег для поиска!")
        else:
            self.tag_input.clear()
            self.notes_list.clear()
            self.notes_list.addItems(self.notes.keys())
            self.search_button.setText("Искать по тегу")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = SmartNotesApp()
    ex.show()
    sys.exit(app.exec_())
