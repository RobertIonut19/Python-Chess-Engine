import datetime
class LibraryItem():

    def __init__(self, name):
        self.item = name
        self.no_pages = None
        self.date_of_borrow = None
        self.date_of_return = None

    def check_out(self, borrow_date):
        self.date_of_borrow = borrow_date

        current_date = datetime.date.today()
        self.date_of_return = current_date + datetime.timedelta(days=14)

    def return_item(self, current_date):
        if current_date > self.date_of_return:
            print(f"Trebuia sa aduci cartea pana pe {self.date_of_return}...")
        else:
            print("Return completed")


class Book(LibraryItem):

    def __init__(self, name, no_pages, author, is_rented, check_out_date = 0):

        super().__init__(name)
        self.no_pages = no_pages
        self.author = author
        self.is_rented = is_rented
        if(is_rented == True):
            self.date_of_borrow = check_out_date
            self.date_of_return = check_out_date + datetime.timedelta(days=14)

    def get_info(self):
        print(f"Name: {self.item}, number of pages: {self.no_pages}, author: {self.author}, is rented: {self.is_rented}")

    def rent_book(self, current_date):
        if(self.is_rented == False):
            self.is_rented = True
            self.check_out(current_date)
        else:
            print("Book already rented")

    def return_book(self, current_date):
        if(self.is_rented == True):
            self.is_rented = False
            self.return_item(current_date)
        else:
            print("Book already returned")

class Magazine(LibraryItem):

    def __init__(self, name, no_pages, issue, is_rented, check_out_date = 0):
        super().__init__(name)
        self.no_pages = no_pages
        self.issue = issue
        self.is_rented = is_rented
        if(is_rented == True):
            self.date_of_borrow = check_out_date
            self.date_of_return = check_out_date + datetime.timedelta(days=14)

    def get_info(self):
        print(f"Name: {self.item}, number of pages: {self.no_pages}, issue: {self.issue}, is rented: {self.is_rented}")

    def rent_magazine(self, current_date):
        if(self.is_rented == False):
            self.is_rented = True
            self.check_out(current_date)
        else:
            print("Magazine already rented")

    def return_magazine(self, current_date):
        if(self.is_rented == True):
            self.is_rented = False
            self.return_item(current_date)
        else:
            print("Magazine already returned")

class DVD(LibraryItem):

    def __init__(self, name, no_pages, director, is_rented, check_out_date = 0):
        super().__init__(name)
        self.no_pages = no_pages
        self.director = director
        self.is_rented = is_rented
        if(is_rented == True):
            self.date_of_borrow = check_out_date
            self.date_of_return = check_out_date + datetime.timedelta(days=14)

    def get_info(self):
        print(f"Name: {self.item}, number of pages: {self.no_pages}, director: {self.director}, is rented: {self.is_rented}")

    def rent_dvd(self, current_date):
        if(self.is_rented == False):
            self.is_rented = True
            self.check_out(current_date)
        else:
            print("DVD already rented")

    def return_dvd(self, current_date):
        if(self.is_rented == True):
            self.is_rented = False
            self.return_item(current_date)
        else:
            print("DVD already returned")

def library_exercise():
    book = Book("Book", 100, "James Goodwill", False)
    book.get_info()
    book.rent_book(datetime.date.today())
    book.get_info()
    book.return_book(datetime.date.today())
    book.get_info()

    magazine = Magazine("Magazine", 50, 1, False)
    magazine.get_info()
    magazine.rent_magazine(datetime.date.today())
    magazine.get_info()
    magazine.return_magazine(datetime.date.today())
    magazine.get_info()

    dvd = DVD("DVD", 2, "Director", False)
    dvd.get_info()
    dvd.rent_dvd(datetime.date.today())
    dvd.get_info()
    dvd.return_dvd(datetime.date.today())
    dvd.get_info()


library_exercise()


