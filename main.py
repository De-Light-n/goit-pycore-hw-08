from address_book import AddressBook, Record
import pickle


# Мені вже цікаво, чи то я щось не доробив, чи то пожаліли і просто Ctrl+C/V
def save_data(book, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


# Декоратор
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except IndexError:
            return "Not enough arguments was gained."
        except Exception as e:
            return  f"{e}"
    return inner

# Функції 
def show_all(book: AddressBook):
    return book

@input_error       
def show_phone(args, book: AddressBook):
    record = book.find(args[0])
    if record:
        return record
    else:
        return "Contact not founded"

@input_error     
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
        return "Contact changed"
    else:
        return "Contact not founded"
    

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message

@input_error
def add_birthday(args, book: AddressBook):
    name, birthday, *_ = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return "Birthday added."
    else:
        return "Contact not founded"

@input_error
def show_birthday(args, book: AddressBook):
    record = book.find(args[0])
    if record:
        return record.birthday
    else:
        return "Contact not founded"
@input_error
def birthdays(book: AddressBook):
    bds = book.get_upcoming_birthdays()
    if bds:
        string = ""
        for contact in bds:
            string += f"{contact["name"]}: {contact["congratulation_date"]}\n"
        return string
    else:
        return "There is not upcoming birthdays"


def main():
    book = load_data()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?\nComands:\nadd [name] [phone]\nchahge [name] [old phone] [new phone] \
                    \nphone [name] \nall\nadd-birthday [name] [date in format 'DD.MM.YYYY']\nshow-birthday [name]\
                    \nbirthdays\nexit\nclose")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")
            
    save_data(book)


if __name__ == "__main__":
    main()