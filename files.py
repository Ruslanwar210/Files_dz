'''
Дополнить справочник возможностью копирования данных из одного файла в другой.
Пользователь вводит номер строки, которую необходимо перенести из одного файла в другой.
'''
from csv import DictWriter, DictReader
from os.path import exists


class NameError:
    def __init__(self, txt):
        self.txt = txt


class PhoneError:
    def __init__(self, txt):
        self.txt = txt


class RowError:
    def __init__(self, txt):
        self.txt = txt


def get_user_data():
    flag = False
    while not flag:
        try:
            first_name = input('Введите имя пользователя: ')
            if len(first_name) < 2:
                raise NameError('Невалидная длина!')
            last_name = input('Введите фамилию пользователя: ')
            if len(last_name) < 2:
                raise NameError('Невалидная длина!')
            phone_number = int(input('Введите номер телефона пользователя: '))
            if len(str(phone_number)) < 11:
                raise PhoneError('Неверная длина номера!')
            validation = input(f'Введите "y" для подтверждения.\n'
                               f'Имя: {first_name}; Фамилия: {last_name}; Телефон: {phone_number}\n')
            if validation == "y":
                flag = True
        except ValueError:
            print('Вы вводите символы вместо цифр!')
            continue
        except NameError as err:
            print(err)
            continue
        except PhoneError as err:
            print(err)
            continue
    return first_name, last_name, phone_number


def create_file(file_name):
    with open(file_name, 'w', encoding='UTF-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()


file_name = 'phone.csv'
copy_file = 'copy_phone.csv'


def read_file(file_name):
    with open(file_name, encoding='UTF-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)


def write_file(file_name):
    user_data = get_user_data()
    res = read_file(file_name)
    for el in res:
        if el['Телефон'] == str(user_data[2]):
            print('Такой пользователь уже существует!')
            return
    obj = {'Имя': user_data[0], 'Фамилия': user_data[1], 'Телефон': user_data[2]}
    res.append(obj)
    with open(file_name, 'w', encoding='UTF-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)


def copy_data(file_name, copy_file):  # функция копирования
    row = 0
    source = read_file(file_name)
    result = read_file(copy_file)
    flag = False
    while not flag:
        try:
            row = int(input(f'Введите номер строки для копии от 1 до {len(source)}\n')) - 1
            if 0 < row > len(source) - 1:
                raise RowError('Строка вне диапазона!')
            validation = input('Введите "y" для подтверждения.\n')
            if validation == "y":
                flag = True
        except ValueError:
            print('Вы вводите символы вместо цифр!')
            continue

    for el in result:
        if source[row] == el:
            print('Такой пользователь уже существует!')
            return
    result.append(source[row])
    with open(copy_file, 'w', encoding='UTF-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(result)
        print('Данные успешно записаны')


def main():
    while True:
        command = input('Введите команду: ')
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                create_file(file_name)
            write_file(file_name)
            print('Данные успешно записаны')
        elif command == 'r':
            if not exists(file_name):
                print('Файл не создан! Создайте его')
                continue
            print(read_file(file_name))
        elif command == 'c':  # Команда копирования
            if not exists(copy_file):  # Если целевой файл не создан, создаем
                create_file(copy_file)
            copy_data(file_name, copy_file)  # Передаем в функцию строку, исходный и целевой файл


main()