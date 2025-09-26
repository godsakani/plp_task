# Assignment 1

class Book:
    available_books = 0
    books = {}
    def __init__(self, title, author, isbn, pub_date):
        self.title = title
        self.author = author
        self.isbn = isbn
        self.pub_date = pub_date
        
    @classmethod
    def add_new(clc, title, author, isbn, pub_date):
        clc.books = {"title":title, "author":author, "isbn":isbn, "pub_date":pub_date}
        Book.available_books +=1
        return clc.books
    
    def publish_book(self):
        return "You Publish a new book"
    def __str__(self):
        return f"You just added a new book with title {self.title} and author {self.author}"
    
    
class Library(Book):
    def __init__(self, title, author, isbn, pub_date, borrow_date:str, return_date:str, borrower:str):
        self.borrow_date = borrow_date
        self.return_date = return_date
        self.borrower = borrower
        super().__init__(title, author, isbn, pub_date)
        
    def borrow_book(self, borrow_date, borrower, return_date):
        Book.available_books -=1
        return f"you have borrow book with title {self.title} on {self.borrow_date} to return on {self.return_date}"
        
        
# Testing the class       
books = Book("Time Management","NGodwill","2e#er33","11/02/1988")
library = Library("OOP", "PLP", "2e#er43", "11/02/1908", "11/02/2025", "11/02/2026", "PLP OOP")
new_book = books.add_new("OOP","PLP","2e#er43","11/02/1908")
borrow_book = library.borrow_book("11/02/2025", "PLP OOP", "11/02/2026")

print(new_book)
print(borrow_book)


# Activity 2: Polymorphism Challenge! 🎭
# Create a program that includes animals or vehicles with the same action (like move()). However, make each class define move() differently (for example, Car.move() prints "Driving" 🚗, while Plane.move() prints "Flying" ✈️).
class Plane:
    def move(self):
        return "Flying"
    
class Vehicle:
    def move(self):
        return "Driving"
    
for transport_method in [Plane(), Vehicle()]:
    print(transport_method.move())