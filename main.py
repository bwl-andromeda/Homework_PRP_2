import csv
import re

def correct_data(contacts_list):
    pattern_fio = r'^([а-яёА-ЯЁ]+)(\s*)(,?)([а-яёА-ЯЁ]+)(\s?)(,?)([а-яёА-ЯЁ]*)(,?){1,6}([а-яёА-ЯЁ]*)'
    new_pattern_fio = r'\1,\4,\7,\9,' 
    pattern_number = r'(\+7|8)?\s*\(?(\d{3})\)?\s*[-]?(\d{3})\s*[-]?(\d{2})\s*[-]?(\d{2})(\s*)\(?(доб.)?\)?(\s*)(\d{0,4})\)?'
    new_pattern_number = r'+7(\2)\3-\4-\5\6\7\9'
    new_contacts_list = []

    for page in contacts_list:
        page_string = ','.join(page)
        format_page = re.sub(pattern_fio, new_pattern_fio, page_string)
        format_page_number = re.sub(pattern_number, new_pattern_number, format_page)
        page_list = format_page_number.split(',')
        new_contacts_list.append(page_list)
    
    return new_contacts_list


def delete_duplicate_data(new_contacts_list):
    surnames = {}
    fixed_list = [new_contacts_list[0]]

    for index, row in enumerate(new_contacts_list[1:]):
        if row[0] not in surnames.keys():
            surnames[row[0]] = index + 1
        else:
            fix_row = new_contacts_list[surnames[row[0]]]
            for i in range(1, 6):
                fix_row[i] = fix_row[i] or row[i-1]

    for index in surnames.values():
        fixed_list.append(new_contacts_list[index])
    
    return fixed_list


if __name__ == '__main__':
    with open("phonebook_raw.csv", encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=",")
        contacts_list = list(rows)
    
    contacts_new = delete_duplicate_data(correct_data(contacts_list))

    with open("phonebook_new.csv", 'w', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=",")
        datawriter.writerows(contacts_new)