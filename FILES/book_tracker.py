
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QListWidget, QMessageBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QIcon
from database_functions import load_data, add_book, delete_book, update_books, create_table

class BookTrackerApp(QWidget):
    def __init__(self):
        super().__init__()
        create_table()
        self.title = 'Book Tracker'
        self.left = 100
        self.top = 100
        self.width = 400
        self.height = 300
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowIcon(QIcon('books.png'))

        # Title
        title_label = QLabel('Title', self)
        title_label.move(20, 20)
        self.title_entry = QLineEdit(self)
        self.title_entry.move(100, 20)

        # Author
        author_label = QLabel('Author', self)
        author_label.move(20, 60)
        self.author_entry = QLineEdit(self)
        self.author_entry.move(100, 60)

        # Year
        year_label = QLabel('Year', self)
        year_label.move(20, 100)
        self.year_entry = QLineEdit(self)
        self.year_entry.move(100, 100)

        # Last page read
        last_page_label = QLabel('Last Page Read', self)
        last_page_label.move(20, 140)
        self.last_page_entry = QLineEdit(self)
        self.last_page_entry.move(150, 140)

        # Buttons
        add_button = QPushButton('Add Book', self)
        add_button.clicked.connect(self.add_book)
        add_button.move(20, 140)

        delete_button = QPushButton('Delete Book', self)
        delete_button.clicked.connect(self.delete_book)
        delete_button.move(120, 140)

        update_button = QPushButton('Update Book', self)
        update_button.clicked.connect(self.update_book)
        update_button.move(220, 140)
        
        # Books list
        books_label = QLabel('Books', self)
        books_label.move(20, 220)
        self.books_list = QListWidget(self)
        self.books_list.move(20, 240)
        self.load_books()

        # Layout
        vbox = QVBoxLayout()
        vbox.addWidget(title_label)
        vbox.addWidget(self.title_entry)
        vbox.addWidget(author_label)
        vbox.addWidget(self.author_entry)
        vbox.addWidget(year_label)
        vbox.addWidget(self.year_entry)
        vbox.addWidget(last_page_label)
        vbox.addWidget(self.last_page_entry)
        vbox.addWidget(add_button)
        vbox.addWidget(delete_button)
        vbox.addWidget(update_button)

        hbox = QHBoxLayout()
        hbox.addLayout(vbox)
        hbox.addWidget(books_label)
        hbox.addWidget(self.books_list)

        self.setLayout(hbox)
        self.show()

    def load_books(self):
        self.books_list.clear()
        data = load_data()
        for book in data:
            self.books_list.addItem(f"{book['title']} by {book['author']} ({book['year']}) - Last page read: {book['last_page']}")

    def add_book(self):
        title = self.title_entry.text()
        author = self.author_entry.text()
        year = self.year_entry.text()
        last_page = self.last_page_entry.text()

        if not title or not author:
            QMessageBox.critical(self, 'Error', 'Please fill in title and author fields')
            return

        success = add_book(title, author, year,last_page)

        if success:
            self.load_books()
            QMessageBox.information(self, 'Success', 'Book added successfully')
            self.title_entry.clear()
            self.author_entry.clear()
            self.year_entry.clear()
            self.last_page_entry.clear()
        else:
            QMessageBox.critical(self, 'Error', 'Failed to add book')

    def delete_book(self):
        selected_items = self.books_list.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, 'Error', 'Please select a book')
        else:
            for item in selected_items:
                title = item.text().split(' by ')[0]
                delete_book(title)
        self.load_books()

    def update_book(self):
        selected_items = self.books_list.selectedItems()
        if not selected_items:
            QMessageBox.critical(self, 'Error', 'Please select a book')
        else:
            title = selected_items[0].text().split(' by ')[0]
            author = self.author_entry.text()
            year = self.year_entry.text()
            last_page = self.last_page_entry.text()
            if not author or not year or not last_page:
                QMessageBox.critical(self, 'Error', 'Please fill in the author and year fields')
            else:
                update_books(title, author, year,last_page)
                self.load_books()
                self.title_entry.clear()
                self.author_entry.clear()
                self.year_entry.clear()
                self.last_page_entry.clear()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = BookTrackerApp()
    sys.exit(app.exec_())




