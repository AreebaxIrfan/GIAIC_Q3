class Book:
    total_books = 0
    
    def __init__ (self, title):
        self.title = title
        Book.increment_book_count()
        
    @classmethod
    def increment_book_count(cls):
        cls.total_books += 1
    
    @classmethod
    def display_total_books(cls):
        print(f"Total books: {cls.total_books}")
        
        
book1 = Book("Python Programming")
book2 = Book("Data Science")    
Book.display_total_books()  # Output: Total books: 2