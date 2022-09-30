from io import TextIOWrapper
from Contact import Contact
# глобальные переменные
TABLE_HEADERS = ["id", "фамилия", "имя", "отчество", "номер телефона", "email"]
CONSOLE_REPORT = "Доступные действия (введите номер):\
                \n1 - вывести все контакты\
                \n2 - произвести поиск по номеру телефона\
                \n3 - произвести поиск по адресу электронной почты\
                \n4 - произвести поиск по фамилии, имени, и/или отчеству\
                \n5 - вывести все контакты с незаполненным номером телефона\
                \n6 - вывести все контакты с незаполненной почтой\
                \n7 - вывести все контакты с незаполненными номером телефона и электронной почтой\
                \n8 - изменить данные контактов человека\
                \n9 - завершить работу программы\
                \n> "



def print_table(max_length: int, users_data: list[tuple[str, str, str, str, str, str]]) -> None:
   output = []
   l = max(len(str(len(users_data))), 3) # ширина столбца id
   for data in users_data:
      output.append(f"# {data[0].center(l)} # " + " # ".join(field.center(max_length, " ") for field in data[1:]) + " #")
   separator = "#" * ((max_length + 2) * 5 + 9 + l)
   print(f"Пользователей, соответствующих заданным параметрам: {len(users_data)}")
   print(separator)
   print(f"# {TABLE_HEADERS[0].center(l)} # " + " # ".join(field.center(max_length, " ") for field in TABLE_HEADERS[1:]) + " #")
   print(separator)
   print("\n".join(output))
   print(separator, end="\n\n")

def fetch_users() -> list[Contact]:
   file = request_file()
   users = []
   counter = 1
   for line in file:
      surname, name, patronymic, phone_number, email = parse_data(raw_data=line)
      if surname == "":
         # если формат строки в файле неверный
         continue
      user = Contact(id=counter, surname=surname, name=name, patronymic=patronymic, phone_number=phone_number, email=email)
      users.append(user)
      counter += 1
   if not file.closed: file.close()
   return users

def request_file() -> TextIOWrapper:
   while True:
      try:
         filename = input("Пожалуйста, введите имя файла\n> ").strip()
         if not filename.endswith(".txt"):
            filename += ".txt"
         f = open(file=filename, mode="r", encoding="utf-8")
      except FileNotFoundError:
         print("Такой текстовый файл не найден")
      except PermissionError:
         print("Недостаточно прав для чтения этого файла")
      except OSError:
         print("Такой текстовый файл не найден")
      except:
         print("Такой текстовый файл не найден")
      else:
         break
   return f

def parse_data(raw_data: str) -> tuple[str, str, str, str, str]:
   user_info = raw_data.strip().split(",")
   if len(user_info) != 3:
      return ("", "", "", "", "")
   snp, phone_number, email = user_info[0].strip().split(), user_info[1].strip(), user_info[2].strip()
   snp += ["", ""] # если нет имени или отчества
   surname, name, patronymic = snp[0], snp[1], snp[2]
   return (surname, name, patronymic, phone_number, email)

def print_users(users: list[Contact]) -> None:
   users_data = []
   # наиболшая длина какого-либо параметра пользователя для корректного формата таблицы (выравнивание столбцов)
   # по умолчанию 14 - для заголовка 'номер телефона'
   max_length = 14
   for user in users:
      data = user.data()
      max_length = max(max_length, len(max(data, key=len)))
      users_data.append(data)
   print_table(max_length=max_length, users_data=users_data)

def find_by_number(users: list[Contact]) -> None:
   ph_number = request_number()
   if not ph_number:
      print("Вы ничего не ввели")
      return
   found_users = []
   max_length = 14
   for user in users:
      if user.is_correct_data(phone_number=ph_number):
         data = user.data()
         max_length = max(max_length, len(max(data, key=len)))
         found_users.append(data)
   if not len(found_users):
      print("В базе данных нет человека с таким номером")
   else:
      print_table(max_length=max_length, users_data=found_users)

def request_number(additional_info: str = "") -> str:
   report = f"Введите {additional_info}номер телефона в формате +Х, где X - от 9 до 11 цифр. Например, +74957713242\n> "
   while True:
      user_input = input(report).strip()
      if not user_input:
         return ""
      if not user_input.startswith("+"):
         print("Указанный Вами номер не начинается с \"+\"")
         continue
      if not user_input[1:].isdigit():
         print("Указанный Вами номер содержит не только цифры")
         continue
      if not (10 <= len(user_input) <= 12):
         print("Указанный Вами номер имеет некорретную длину")
         continue
      return user_input

def find_by_email(users: list[Contact]) -> None:
   email = request_email()
   if not email:
      print("Вы ничего не ввели")
      return
   found_users = []
   max_length = 14
   for user in users:
      if user.is_correct_data(email=email):
         data = user.data()
         max_length = max(max_length, len(max(data, key=len)))
         found_users.append(data)
   if not len(found_users):
      print("В базе данных данных нет человека с таким адресом электронной почты")
   else:
      print_table(max_length=max_length, users_data=found_users)

def request_email(additional_info: str = "") -> str:
   report = f"Введите {additional_info}адрес электронной почты в формате X@Y.Z, например, X@hse.ru\n> "
   while True:
      user_input = input(report).strip()
      if not user_input:
         return ""
      if not "@" in user_input:
         print("Указанный Вами адрес электронной почты не содержит \"@\"")
         continue
      domen_path = user_input.split("@")[1].split(".")
      if len(domen_path) != 2 or not len(domen_path[0]) or not len(domen_path[1]):
         print("Указанный Вами адрес электронной почты имеет неправильный формат домена")
         continue
      return user_input

def find_by_snp(users: list[Contact]) -> None:
   surname, name, patrnm = request_info()
   if not surname and not name and not patrnm:
      print("Вы ничего не ввели")
      return
   found_users = []
   max_length = 14
   for user in users:
      if user.is_correct_data(surname=surname, name=name, patronymic=patrnm):
         data = user.data()
         found_users.append(data)
         max_length = max(max_length, len(max(data, key=len)))
   if not found_users:
      report = form_report(surname=surname, name=name, patrnm=patrnm)
      print(report)
      return
   print_table(max_length=max_length, users_data=found_users)

def request_info() -> tuple[str, str, str]:
   surname = input("Введите фамилию человека (если поиск без фамилии, нажмите Enter)\n> ").strip()
   name = input("Введите имя человека (если поиск без имени, нажмите Enter)\n> ").strip()
   patronymic = input("Введите отчество человека (если поиск без отчества, нажмите Enter)\n> ").strip()
   return (surname, name, patronymic)

def form_report(surname: str, name: str, patrnm: str) -> str:
   user_info = []
   if surname: user_info.append(f"фамилией {surname}")
   if name: user_info.append(f"именем {name}")
   if patrnm: user_info.append(f"отчеством {patrnm}")
   report = f"В базе данных нет человека с {user_info[0]}"
   if len(user_info) == 2:
      report += f" и {user_info[1]}"
   elif len(user_info) == 3:
      report += f", {user_info[1]} и {user_info[2]}"
   return report

def print_null_ph_num(users: list[Contact]) -> None:
   found_users = []
   max_length = 14
   for user in users:
      if user.is_null_phone_number():
         data = user.data()
         found_users.append(data)
         max_length = max(max_length, len(max(data, key=len)))
   if not found_users:
      print("Не найдено пользователей с незаполненным номером")
      return
   print_table(max_length=max_length, users_data=found_users)

def print_null_email(users: list[Contact]) -> None:
   found_users = []
   max_length = 14
   for user in users:
      if user.is_null_email():
         data = user.data()
         found_users.append(data)
         max_length = max(max_length, len(max(data, key=len)))
   if not found_users:
      print("Не найдено пользователей с незаполненным адресом электронной почты")
      return
   print_table(max_length=max_length, users_data=found_users)

def print_null_ph_n_and_eml(users: list[Contact]) -> None:
   found_users = []
   max_length = 14
   for user in users:
      if user.is_null_phone_number() and user.is_null_email():
         data = user.data()
         found_users.append(data)
         max_length = max(max_length, len(max(data, key=len)))
   if not found_users:
      print("Не найдено пользователей с незаполненными номером телефона и адресом электронной почты")
      return
   print_table(max_length=max_length, users_data=found_users)

def edit_user(users: list[Contact]) -> None:
   user = request_user(users)
   if user.id == 0:
      print("Вы ничего не ввели")
      return
   new_surname, new_name, new_patronymic, new_ph_num, new_email = request_new_info()
   if not new_surname and not new_name and not new_patronymic and not new_ph_num and not new_email:
      print("Вы ничего не ввели")
      return
   new_data = user.edit_data(new_surname=new_surname, new_name=new_name, new_patronymic=new_patronymic, new_phone_number=new_ph_num, new_email=new_email)
   max_length = max(14, len(max(new_data, key=len)))
   print("Контакты человека успешно обновлены:")
   print_table(max_length=max_length, users_data=[new_data])

def request_user(users: list[Contact]) -> Contact:
   max_id = len(users)
   while True:
      user_input = input("Введите id пользователя из таблицы\n> ")
      if not user_input:
         return Contact()
      if not user_input.isdigit():
         print("Вы ввели не id")
         continue
      user_id = int(user_input)
      if not (1 <= user_id <= max_id):
         print("Введённого Вами id нет в таблице")
         continue
      break
   return fetch_user_by_id(user_id=user_id, users=users)

def fetch_user_by_id(user_id: int, users: list[Contact]) -> Contact:
   found_user = Contact()
   for user in users:
      if user.id == user_id:
         found_user = user
         break
   return found_user

def request_new_info() -> tuple[str, str, str, str, str]:
   print("Если какой-то из параметров надо сбросить, введите None. Если менять не надо, нажмите Enter")
   new_surname = input("Введите новую фамилию человека\n> ").strip()
   new_name = input("Введите новое имя человека\n> ").strip()
   new_patronymic = input("Введите новое отчество человека\n> ").strip()
   new_ph_num = request_number(additional_info="новый ")
   new_email = request_email(additional_info="новый ")
   return (new_surname, new_name, new_patronymic, new_ph_num, new_email)

def exit_program(*args):
   input("Благодраим за использование программы. Нажмите Enter для выхода в командную строку консоли\n")
   exit()

def main():
   commands = {
      "1": print_users,
      "2": find_by_number,
      "3": find_by_email,
      "4": find_by_snp,
      "5": print_null_ph_num,
      "6": print_null_email,
      "7": print_null_ph_n_and_eml,
      "8": edit_user,
      "9": exit_program
   }
   users: list[Contact] = fetch_users()
   while True:
      user_input = input(CONSOLE_REPORT)
      if user_input not in commands:
         print("Такая команда не найдена")
         continue
      commands[user_input](users)

if __name__ == "__main__":
   main()