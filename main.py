import re
from pprint import pprint
import csv

def fix_name(name_str):
    # разбиваем строку с ФИО на отдельные части
    name_parts = re.split(r'\s+', name_str.strip())
    # предполагаем, что в name_parts записаны: Ф И О (возможно неполное)
    if len(name_parts)==3:
        return name_parts
    # неполное ФИО, попробуем восстановить
    # если возможно, значение пустых полей заполним из следующих записей
    new_name_parts = [name_parts[0], '', '']
    if len(name_parts)>=2:
      new_name_parts[1] = name_parts[1]
    if len(name_parts)>=3:
      new_name_parts[2] = name_parts[2]
    return new_name_parts

def fix_phone(phone_str):
    # убираем все символы, кроме цифр и знака +
    phone_digits = re.sub(r'\D', '', phone_str)
    # если номер начинается с 8, заменяем на +7
    if phone_digits.startswith('8'):
        phone_digits = '7' + phone_digits[1:]
    # добавляем форматирование
    if len(phone_digits) >= 11:
        phone_formatted = '+7({}){}-{}-{}'.format(phone_digits[1:4], phone_digits[4:7], \
                                                   phone_digits[7:9], phone_digits[9:11])
        if len(phone_digits) > 11:
            phone_formatted += ' доб.{}'.format(phone_digits[11:])
    else:
        phone_formatted = phone_str
    return phone_formatted

def fix_contact(contact):
    new_contact = contact[:6]
    # исправляем ФИО
    new_contact[:3] = fix_name(contact[0])
    # исправляем телефон и e-mail
    new_contact.append(fix_phone(contact[5]))
    new_contact.append(contact[6].lower())
    return new_contact

with open("phonebook_raw.csv",encoding='utf-8') as f:
    rows = csv.reader(f, delimiter=",")
    contacts_list = list(rows)

# Собираем все записи, использовавшие одинаковые номера телефонов/адреса эл. почты
contacts_dict = {}
for contact in contacts_list:
    # пропускаем первую строчку с заголовками
    if contact[0] == 'lastname':
        continue
    # подготавливаем данный контакт
    new_contact = fix_contact(contact)
    # проверяем, существует ли у нас контакт с таким же телефоном или адресом эл. почты
    key = (new_contact[5], new_contact[6])
    if key in contacts_dict:
        # если да, обновляем этот контакт с наиболее полной информацией
        existing_contact = contacts_dict[key]
        for i in range(6):
            if existing_contact[i] == '' and new_contact[i] != '':
                existing_contact[i] = new_contact[i]
    else:
        # если нет, сохраняем этот контакт
        contacts_dict[key] = new_contact

# формируем список уникальных контактов
unique_contacts = list(contacts_dict.values())

# записываем данные в новый файл
with open("phonebook.csv", "w", newline='',encoding='utf-8') as f:
    datawriter = csv.writer(f, delimiter=',')
    datawriter.writerow(['lastname', 'firstname', 'surname', 'organization', \
                         'position', 'phone', 'email'])
    datawriter.writerows(unique_contacts)