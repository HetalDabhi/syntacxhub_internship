import json
import os

# ------------------ Book Class ------------------
class Book:
    def __init__(self, book_id, title, author):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.issued = False

    def to_dict(self):
        return {
            "book_id": self.book_id,
            "title": self.title,
            "author": self.author,
            "issued": self.issued
        }

    @staticmethod
    def from_dict(data):
        book = Book(data["book_id"], data["title"], data["author"])
        book.issued = data["issued"]
        return book


# ------------------ Library Class ------------------
class Library:
    def __init__(self, filename="library.json"):
        self.filename = filename
        self.books = {}   # HashMap-like dictionary
        self.load_data()

    # ---------- Add Book ----------
    def add_book(self, book_id, title, author):
        if book_id in self.books:
            print("Book ID already exists!")
            return
        self.books[book_id] = Book(book_id, title, author)
        self.save_data()
        print("Book added successfully.")

    # ---------- Search ----------
    def search(self, keyword):
        print("\nSearch Results:")
        found = False
        for book in self.books.values():
            if keyword.lower() in book.title.lower() or keyword.lower() in book.author.lower():
                self.display_book(book)
                found = True
        if not found:
            print("No matching books found.")

    # ---------- Issue Book ----------
    def issue_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            print("Book not found.")
        elif book.issued:
            print("Book already issued.")
        else:
            book.issued = True
            self.save_data()
            print("Book issued successfully.")

    # ---------- Return Book ----------
    def return_book(self, book_id):
        book = self.books.get(book_id)
        if not book:
            print("Book not found.")
        elif not book.issued:
            print("Book was not issued.")
        else:
            book.issued = False
            self.save_data()
            print("Book returned successfully.")

    # ---------- Reports ----------
    def report(self):
        total_books = len(self.books)
        issued_books = sum(1 for book in self.books.values() if book.issued)
        print("\n--- Library Report ---")
        print("Total Books:", total_books)
        print("Issued Books:", issued_books)

    # ---------- Display ----------
    def display_book(self, book):
        status = "Issued" if book.issued else "Available"
        print(f"ID: {book.book_id} | {book.title} by {book.author} | {status}")

    # ---------- Persistence ----------
    def save_data(self):
        with open(self.filename, "w") as f:
            json.dump({k: v.to_dict() for k, v in self.books.items()}, f, indent=4)

    def load_data(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r") as f:
                data = json.load(f)
                for k, v in data.items():
                    self.books[k] = Book.from_dict(v)


# ------------------ Main Menu ------------------
def main():
    library = Library()

    while True:
        print("\n--- Library Book Inventory Manager ---")
        print("1. Add Book")
        print("2. Search Book")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. Report")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            book_id = input("Book ID: ")
            title = input("Title: ")
            author = input("Author: ")
            library.add_book(book_id, title, author)

        elif choice == "2":
            keyword = input("Enter title or author: ")
            library.search(keyword)

        elif choice == "3":
            book_id = input("Book ID to issue: ")
            library.issue_book(book_id)

        elif choice == "4":
            book_id = input("Book ID to return: ")
            library.return_book(book_id)

        elif choice == "5":
            library.report()

        elif choice == "6":
            print("Exiting Library System...")
            break

        else:
            print("Invalid choice!")


# ------------------ Run Program ------------------
if __name__ == "__main__":
    main()
