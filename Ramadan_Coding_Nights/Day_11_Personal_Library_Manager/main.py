import json

class BookCollection:
    """A class to manage a collection of books, allowing user to store and organize their books."""
    
    def __init__(self):
        """initialize a new book collection with an empty list and set up file storage."""
        self.books =[]
        self.storage_file = "books_data.json"
        self.read_from_file()
        
    def read_from_file(self):
        """Load saved books from a JSON file into memory.
        if the file does not exist, initiatize an empty list.
        """
        try:
            with open(self.storage_file, "r")as file:
                self.books_list = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.books_list = []
            
    def save_to_file(self):
        """Save the current collection of books to a JSON file."""
        with open(self.storage_file, "w") as file:
            json.dump(self.books_list, file, indent=4)
            
    def create_new_book(self):
        """Add a new book to the collection by gathering information from the user"""
        book_title = input("Enter book title")
        book_author = input("Enter book author")
        publication_year = input("Enter publication year")
        book_genre = input("Enter book genre")
        is_book_read = (
            input("Have you read this book? (yes/no)").strip().lower() == "yes"
        )
        new_book = {
            "title": book_title,
            "author": book_author,
            "year": publication_year,
            "genre": book_genre,
            "read": is_book_read,
        }
        
        self.books_list.append(new_book)
        self.save_to_file() 
        print(f"Book added successfully! \n")
        
    
    def delete_book(self):
        """Remove a book from the collection by title."""
        book_title = input("Enter the title of the book you want to delete:")
        
        for book in self.books_list:
            if book["title"].lower() == book_title.lower():
                self.books_list.remove(book)
                self.save_to_file()
                print(f"{book_title} has been removed from the collection")
                return
        print(f"Book with title {book_title} not found in the collection.")
        
        
    def find_book(self):
        """Search for a book in the collection by title."""
        search_title = input("Enter the title of the book you are looking for:")
        search_text = search_title.lower()
        found_books = [
            book
            for book in self.books_list
            if search_text in book["title"].lower()
            or search_text in book["author"].lower()
        ]
        
        if found_books:
            print("Matching books:")
            for index, book in enumerate(found_books, 1):
                reading_status ="Read" if book["read"] else "Unread"
                print(
                    f"{index}. {book['title']} by {book['author']} ({book['year']}), {reading_status}"
                )
            else:
                print("No books found matching that title.")
                
        
    def update_book(self):
        """Modify the details of an existing book in the collection."""
        book_title = input("Enter the title of the book you want to edit: ")
        for book in self.book_list:
            if book["title"].lower() == book_title.lower():
                print("Leave blank to keep existing value.")
                book["title"] = input(f"New title ({book['title']}): ") or book["title"]
                book["author"] = (
                    input(f"New author ({book['author']}): ") or book["author"]
                )
                book["year"] = input(f"New year ({book['year']}): ") or book["year"]
                book["genre"] = input(f"New genre ({book['genre']}): ") or book["genre"]
                book["read"] = (
                    input("Have you read this book? (yes/no): ").strip().lower()
                    == "yes"
                )
                self.save_to_file()
                print("Book updated successfully!\n")
                return
        print("Book not found!\n")

    def show_all_books(self):
        """Display all books in the collection with their details."""
        if not self.book_list:
            print("Your collection is empty.\n")
            return

        print("Your Book Collection:")
        for index, book in enumerate(self.book_list, 1):
            reading_status = "Read" if book["read"] else "Unread"
            print(
                f"{index}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}"
            )
        print()
        
    def show_reading_progress(self):
        """Calculate and display statistics about your reading progress."""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])
        completion_rate = (
            (completed_books / total_books * 100) if total_books > 0 else 0
        )
        print(f"Total books in collection: {total_books}")
        print(f"Reading progress: {completion_rate:.2f}%\n")
        
    def start_application(self):
        """Run the main application loop with a user-friendly menu interface."""
        while True:
            print("📚 Welcome to Your Book Collection Manager! 📚")
            print("1. Add a new book")
            print("2. Remove a book")
            print("3. Search for books")
            print("4. Update book details")
            print("5. View all books")
            print("6. View reading progress")
            print("7. Exit")
            user_choice = input("Please choose an option (1-7): ")

            if user_choice == "1":
                self.create_new_book()
            elif user_choice == "2":
                self.delete_book()
            elif user_choice == "3":
                self.find_book()
            elif user_choice == "4":
                self.update_book()
            elif user_choice == "5":
                self.show_all_books()
            elif user_choice == "6":
                self.show_reading_progress()
            elif user_choice == "7":
                self.save_to_file()
                print("Thank you for using Book Collection Manager. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.\n")


if __name__ == "__main__":
    book_manager = BookCollection()
    book_manager.start_application()

        