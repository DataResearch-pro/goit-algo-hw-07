from functools import wraps
from collections import UserDict
from functools import wraps
from datetime import date, datetime, timedelta
import re


#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

def typevalid(obj):
    ''' Validation arg (type & contains) '''

    def decorator(func):
        @wraps(func)
        def wrapper(self, value):
            if not isinstance(value, obj):
                raise TypeError(f"[ERROR] Аргумент {value} невірного типу.")
            if not value:
                raise ValueError(f"[ERROR] Аргумент не містить символів.")
            return func(self, value)
        return wrapper
    return decorator

#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

#Базовий клас для полів запису
class Field:
    def __init__(self, value: str):
        self.value = self._validate(value)

    def __eq__(self, other):
        return isinstance(other, Field) and self.value == other.value

    def __hash__(self):
        return hash(self.value)
    
    def _validate(self, value):
        return value

    def __str__(self):
        return str(self.value)

#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

#Клас для зберігання імені контакту. Обов'язкове поле.
class Name(Field):
    @typevalid(str)
    def __init__(self, value: str):
        super().__init__(value)

#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

#Клас для зберігання номера телефону. Має валідацію формату (10 цифр).
class Phone(Field):
    @typevalid(str)
    def __init__(self, value: str):
        super().__init__(value)

    def _validate(self, value: str):
        pattern = re.compile(r'\d{10}')
        flag = pattern.fullmatch(value)
        if not flag:
            raise ValueError(f"[ERROR] Аргумент {value} невірного формату.")
        return value
    
#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

#Клас для ДН
class Birthday(Field):
    @typevalid(str)
    def __init__(self, value: str):
        try:
            date_value = datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            print(f"Date '{value}' is incorrect. Use DD.MM.YYYY")
        else:
            super().__init__(date_value)
            self.__birth = value

    #Отримання ДН
    def get_date(self):
        return self.__birth

#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

#Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів
class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def __eq__(self, other):
        return isinstance(other, Record) and self.name.value == other.name.value

    def __hash__(self):
        return hash(self.name.value)

# -----------------------------------------------------------------------------
    
    #Перевірка phone у списку
    def phone_exists(self, obj):
        return obj in self.phones
    
    #Додавання телефонів
    def add_phone(self, num: str):
            self.phones.append(Phone(num))

# -----------------------------------------------------------------------------

    #Додавання ДН
    def add_birthday(self, birth: str):
        self.birthday = Birthday(birth)

# -----------------------------------------------------------------------------

    #Видалення телефонів
    def remove_phone(self, num: str):
        self.phones.remove(Phone(num))

# -----------------------------------------------------------------------------

    #Редагування телефонів
    def edit_phone(self, old_num: str, new_num: str):
        self.phones[self.phones.index(Phone(old_num))] = Phone(new_num)
                                                                                                                                                            
# -----------------------------------------------------------------------------

    #Пошук телефону
    def find_phone(self, num: str) -> Phone | None:  
        if not self.phone_exists(Phone(num)):
            return None
        else:    
            return Phone(num)
             
# -----------------------------------------------------------------------------

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"
    
#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

#Клас для зберігання та управління записами
class AddressBook(UserDict):

# -----------------------------------------------------------------------------
    # Перевірка ключа
    def exists(self, obj):
        return obj in self

    @typevalid(Record)
    #Додавання записів
    def add_record(self, rec: Record):
        self[rec.name.value] = rec

# -----------------------------------------------------------------------------

    @typevalid(str)
    #Пошук записів за іменем
    def find(self, key: str) -> Record:
        if not self.exists(key):
            return None
        else:
            return self[key]

# -----------------------------------------------------------------------------

    @typevalid(str)
    #Видалення записів за іменем
    def delete(self, key: str):
        del self[key]

# -----------------------------------------------------------------------------

    #ДН на тиждень вперед
    def get_upcoming_birthdays(self):
        inform_birth = []

        #Валідація для поточного дня
        def __valid_date(dt: Record) -> bool:
            if dt.birthday is None:
                return False
            
            today = (date.today().day, date.today().month)

            #Ідентифікація ДН, що припадають на вихідний день
            if dt.birthday.value.isoweekday() <= 5:
                offset = dt.birthday.value + timedelta(days=8 - dt.birthday.value.isoweekday())
                valid = (offset.day, offset.month)
            else:
                valid = (dt.birthday.value.day, dt.birthday.value.month)

            return today == valid
        
        #Формуємо словники та додаємо до списку
        for key, obj in self.items():
            if not __valid_date(obj):
                continue
            inform_birth.append({'name': key, 'birthday': obj.birthday.get_date()})

        return inform_birth

# -----------------------------------------------------------------------------

    def __str__(self):
        show_data = ''.join([
            f"\nContact name: {key}\n\n" +
            ''.join(
                f"{idx:^4}|{item.value:^18}|\n"
                for idx, item in enumerate(value.phones, start=1)
            )
            for key, value in self.items()
        ])
        return show_data
    
#⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷⊶⊷

def input_error(func):
    @wraps(func)
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AttributeError:
            return "Data attribute error!"
        except ValueError:
            return "Give me name and phone please."
        except KeyError:
            return "The name is not specified"
        except IndexError:
            return "Input data is incorrect. Try again."
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book: AddressBook) -> str:
    name, phone = args[0], args[1]

    if not book.exists(name):
        book.add_record(Record(name))
        msg = "Contact created."
    else:
        msg = "Contact updated."

    book[name].add_phone(phone)
    return msg

@input_error
def change_contact(args, book: AddressBook):
    name, old_phone, new_phone = args

    record = book.find(name)
    if not record:
        return "Contact not found."

    phone_exists = record.find_phone(old_phone)
    if not phone_exists:
        return f"Phone {old_phone} not found."
    
    record.edit_phone(old_phone, new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook):
    name = args[0]

    record = book.find(name)
    if not record:
        return "Contact not found."

    return str(record)

@input_error
def show_all(book: AddressBook):
    if not book.data:
        return "No contacts."
    return str(book)

@input_error
def add_birthday(args, book: AddressBook):
    name, birth = args

    record = book.find(name)
    if not record:
        return "Contact not found."

    record.add_birthday(birth)
    return "Birthday added."

@input_error
def show_birthday(args, book: AddressBook):
    name = args[0]

    record = book.find(name)
    if not record:
        return "Contact not found."

    if not record.birthday:
        return "Birthday not set."

    return record.birthday.get_date()

@input_error
def birthdays(args, book: AddressBook):
    data = book.get_upcoming_birthdays()

    if not data:
        return "No upcoming birthdays."

    return "\n".join(f"{item['name']}: {item['birthday']}" for item in data)


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
            print(birthdays(args, book))

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()