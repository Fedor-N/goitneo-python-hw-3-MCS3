from datetime import datetime, timedelta
from collections import defaultdict, UserDict

# - main classes


class Field:
    # - Base class for record fields.
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Birthday(Field):
    def __init__(self, birthday):
        try:
            date = datetime.strptime(birthday, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Date of birth must be in DD.MM.YYYY format")

        super().__init__(date)


class Name(Field):
    # - A class for storing a contact name. Mandatory field.
    def __init__(self, name):
        super().__init__(name)


class Phone(Field):
    # - A class for storing a phone number. Has format validation (10 digits).
    def __init__(self, phone):
        if not (len(phone) == 10 and phone.isdigit()):
            raise ValueError("Phone number must be 10 digits long")
        super().__init__(phone)


class Record:
    # - A class for storing information about a contact, including name and phone list.
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.birthday = Birthday(birthday) if birthday else None
        self.phones = []

    def add_phone(self, phone_number):
        # - Adding phone
        phone = Phone(phone_number)
        self.phones.append(phone)

    def edit_phone(self, old_number, new_number):
        # - Editing phone
        phone = self.find_phone(old_number)
        if phone:
            phone.value = new_number
            return True
        return False

    def find_phone(self, phone_number):
        # - Phone search
        for phone in self.phones:
            if phone.value == phone_number:
                return phone
        return None

    def add_birthday(self, birthday):
        # - Add birthday
        self.birthday = Birthday(birthday)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        # - Adding records
        if isinstance(record, Record):
            self.data[record.name.value] = record

    def find(self, name):
        # - Search records by name
        return self.data.get(name)

    def delete(self, name):
        # - Deleting records by name
        if name in self.data:
            del self.data[name]

    def get_birthdays_per_week(self):
        birthday_dict = defaultdict(list)
        today = datetime.today().date()
        start = today - timedelta(days=today.weekday())
        end = start + timedelta(days=6)
        for name, record in self.data.items():
            birthday = record.birthday.value.date()
            birthday_this_year = birthday.replace(year=today.year)
            delta_days = (birthday_this_year - end).days
            if delta_days <= 5 and delta_days > -2:
                day_of_week = (birthday_this_year).strftime('%A')
                if day_of_week == "Saturday" or day_of_week == "Sunday":
                    day_of_week = "Monday"
                birthday_dict[day_of_week].append(name)

        return birthday_dict


def input_error(func):
    # - Exception handling
    VErrorPhone = "The phone number must consist of 10 digits"
    VErrorBirthday = "Date of birth must be in DD.MM.YYYY format"

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Can't find the contact."
        except ValueError as VError:
            if str(VError) in VErrorPhone or VErrorBirthday:
                return "Give the correct data, please"
        except IndexError:
            return "No arguments."
    return inner


@input_error
def add_contact(args, book):
    # - Create contact
    name, phone = args
    record = Record(name)
    record.add_phone(phone)
    book.add_record(record)

    return "Contact added."


@input_error
def change_contact(args, book):
    # - Update contact
    name, phone = args
    record = book.find(name)
    if record:
        record.edit_phone(record.phones[0].value, phone)
        return "Contact updated."
    else:
        return "Not found."


@input_error
def show_phone(args, book):
    # - Show phone
    [name] = args
    record = book.find(name)
    if record:
        return ', '.join(map(str, record.phones))
    else:
        return "Not found."


@input_error
def show_all(book):
    # - Show all contatcs
    if not book.data:
        return "No contacts stored."
    return '\n'.join([f"{record.name}: {', '.join(map(str, record.phones))}" for record in book.data.values()])


@input_error
def add_birthday(args, book):
    # - Add a birthday to a contact
    name, birthday = args
    record = book.find(name)
    if record:
        record.add_birthday(birthday)
        return f"Birthday added."
    else:
        return "Contact not found."


@input_error
def show_birthday(args, book):
    # - show the contact birthday
    [name] = args
    record = book.find(name)
    if record and record.birthday:
        return str(record.birthday)
    else:
        return "No birthday found for this contact."


@input_error
def show_birthdays_next_week(book):
    # - show birthdays for the next week
    birthdays_next_week = book.get_birthdays_per_week()
    if not birthdays_next_week:
        return "No birthdays next week."
    response = []
    for day, names in birthdays_next_week.items():
        response.append(f"{day}: {', '.join(names)}")

    return "\n".join(response)


def hello_command():
    return "How can I help you?"


def parse_input(user_input):
    # - Processes the input by splitting the string into command and arguments
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        # Enter a command
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)  # Parse_input
        if command in ["close", "exit"]:
            print("Good bye!")
            break  # Exit
        elif command == "hello":
            print(hello_command())
        elif command == "add":
            print(add_contact(args, book))  # Add Contact
        elif command == "change":
            print(change_contact(args, book))  # Update Contac
        elif command == "phone":
            print(show_phone(args, book))  # Show phone Contact
        elif command == "all":
            print(show_all(book))  # Show All Contacts
        elif command == "add-birthday":
            print(add_birthday(args, book))  # Add birthday
        elif command == "show-birthday":
            print(show_birthday(args, book))  # Show birthday
        elif command == "birthdays":
            print(show_birthdays_next_week(book))  # Show birthday next week
        elif command in ["close", "exit"]:
            print("Good bye!")
            break  # Вихід
        else:
            print(f"Not a valid command '{command}'")


# Input point
if __name__ == "__main__":
    main()
