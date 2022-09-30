class Contact:
    def __init__(self, id: int = 0, surname: str = "", name: str = "", patronymic: str = "", phone_number: str = "", email: str = "") -> None:
        self.id = id
        self.__surname = surname
        self.__name = name
        self.__patrnm = patronymic
        self.__phone_num = phone_number
        self.__email = email

    def __str__(self) -> str:
        return f"{self.id} {self.__surname} {self.__name} {self.__patrnm} {self.__phone_num} {self.__email}"

    def data(self) -> tuple[str, str, str, str, str, str]:
        return (str(self.id), self.__surname, self.__name, self.__patrnm, self.__phone_num, self.__email)

    def is_correct_data(self, surname: str = "", name: str = "", patronymic: str = "", phone_number: str = "", email: str = "") -> bool:
        ans: bool = True
        if surname: ans &= surname == self.__surname
        if name: ans &= name == self.__name
        if patronymic: ans &= patronymic == self.__patrnm
        if phone_number: ans &= phone_number == self.__phone_num
        if email: ans &= email == self.__email
        return ans

    def is_null_phone_number(self) -> bool:
        return self.__phone_num == ""

    def is_null_email(self) -> bool:
        return self.__email == ""

    def edit_data(self, new_surname: str = "", new_name: str = "", new_patronymic: str = "", new_phone_number: str = "", new_email: str = "") -> tuple[str, str, str, str, str, str]:
        if new_surname == "None":
            self.__surname = ""
        elif new_surname:
            self.__surname = new_surname

        if new_name == "None":
            self.__name = ""
        elif new_name:
            self.__name = new_name

        if new_patronymic == "None":
            self.__patrnm = ""
        elif new_patronymic:
            self.__patrnm = new_patronymic

        if new_phone_number == "None":
            self.__phone_num = ""
        elif new_phone_number:
            self.__phone_num = new_phone_number

        if new_email == "None":
            self.__email = ""
        elif new_email:
            self.__email = new_email

        return self.data()