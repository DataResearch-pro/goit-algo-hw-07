from collections import UserDict
from datetime import datetime, timedelta


def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return str(e)
        except KeyError:
            return "Contact not found."
        except IndexError:
            return "Invalid input."
    return wrapper


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    pass


class Phone(Field):
    def __init__(self, value):
        if not (value.isdigit() and len(value) == 10):
            raise ValueError("Phone must be 10 digits.")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            self.date = datetime.strptime(value, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        p = self.find_phone(phone)
        if p:
            self.phones.remove(p)
        else:
            raise ValueError("Phone not found.")

    def edit_phone(self, old_phone, new_phone):
        p = self.find_phone(old_phone)
        if p:
            num = Phone(new_phone)
            self.phones.remove(p)
            self.phones.append(num)
        else:
            raise ValueError("Phone not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def __str__(self):
        phones      = "; ".join(p.value for p in self.phones)
        brth_day    = f", birthday: {self.birthday.value}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{brth_day}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
        else:
            raise KeyError

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        result = []

        for record in self.data.values():
            if not record.birthday:
                continue

            brth_day = record.birthday.date.replace(year=today.year)
            if brth_day < today:
                brth_day = brth_day.replace(year=today.year + 1)

            delta = (brth_day - today).days
            
            if 0 <= delta <= 7:
                congrat_date = brth_day
                if congrat_date.weekday() >= 5:
                    congrat_date += timedelta(days=(7 - congrat_date.weekday()))
                result.append({
                    "Contact": record.name.value,
                    "Date of the greeting": congrat_date.strftime("%d.%m.%Y")
                })

        return result

    def __str__(self):
        return "\n".join(str(record) for record in self.data.values())


def parse_input(user_input):
    cmd, *args = user_input.split()
    return cmd.strip().lower(), *args


@input_error
def add_contact(args, book):
    name, phone, *_ = args
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    else:
        message = "Contact updated."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book):
    name, old_phone, new_phone = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."


@input_error
def show_phone(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    return "; ".join(p.value for p in record.phones)


@input_error
def show_all(book):
    return str(book)


@input_error
def add_birthday(args, book):
    name, brth_day = args
    record = book.find(name)
    if record is None:
        raise KeyError
    record.add_birthday(brth_day)
    return "Birthday added."


@input_error
def show_birthday(args, book):
    name, *_ = args
    record = book.find(name)
    if record is None:
        raise KeyError
    if not record.birthday:
        return "Birthday not set."
    return record.birthday.value


@input_error
def birthdays(book):
    brth_dataset = book.get_upcoming_birthdays()
    if not brth_dataset:
        return "No upcoming birthdays."
    return "\n".join(f"{item['name']}: {item['birthday']}" for item in brth_dataset)


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

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


if __name__ == "__main__":
    main()