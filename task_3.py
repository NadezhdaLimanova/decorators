import os
import datetime
import re
from pprint import pprint
import csv

def logger(path):
    def __logger(old_function):
        def new_function(*args, **kwargs):
            with open(path, 'a', encoding='utf-8') as file:
                current_time = datetime.datetime.now()
                result = old_function(*args, **kwargs)
                file.write(f'Дата и время вызова функции {current_time.strftime("%Y-%m-%d|%H-%M-%S")}\n')
                file.write(f"Функция {old_function.__name__} возвращает {result}\n")
                file.write(f'Args: {args}\n')
                file.write(f'Kwrgs: {kwargs}\n')
            return result

        return new_function

    return __logger


def test_2():
    path = 'log_4.log'

    if os.path.exists(path):
        os.remove(path)

    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        new_list = list(rows)

    @logger(path)
    def regular_sent(new_list):
        for person in new_list[1:]:
            first_field = person[0].split()
            second_field = person[1].split()
            if len(second_field) == 2:
                person[1], person[2] = second_field
            if len(first_field) == 2:
                person[0], person[1] = first_field
            elif len(first_field) == 3:
                person[0], person[1], person[2] = first_field

        pattern = r"(8|\+7)[\s]?[\(]?(\d{3})?[\)]?[\s-]?(\d{3})?[\s-]?(\d{2})?[\s-]?(\d{2})?([\s])?[\(]?(\w{3}\.\s\d{4})?[\s)]?"
        pattern_repl = r"+7(\2)\3-\4-\5\6\7"
        list_2 = []
        for i in new_list:
            i[5] = re.sub(pattern, pattern_repl, i[5])

        data_list = []
        for i in range(1):
            data_list = new_list[i]
        num_elements = len(new_list[0])
        dict_data = {}
        for person in new_list[1:]:
            key = ' '.join(person[:2])
            if key in dict_data.keys():
                for index in range(2, len(person)):
                    if len(person[index]) > 0:
                        dict_data[key][index] = person[index]
            else:
                dict_data[key] = person
        contacts_list = [person_data for person_data in dict_data.values()]
        contacts_list.insert(0, data_list)
        return contacts_list

    @logger(path)
    def write_reg_sent_to_file(contacts_list):
        with open("phonebook.csv", "w", encoding='utf-8') as f:
            datawriter = csv.writer(f, delimiter=',', lineterminator='\n')
            datawriter.writerows(contacts_list)
        return 'Файл сохранен'


    result = regular_sent(new_list)
    result_2 = write_reg_sent_to_file(result)




if __name__ == '__main__':
    test_2()
