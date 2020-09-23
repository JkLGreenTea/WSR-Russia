import datetime
import re
import os


class Cmd:
    def __init__(self, cmd, func) -> None:
        """Иницаилазиция команды"""

        self.args_inline: list = get_args_inline(cmd)  # Аргументы которые будут вводится с новой строки
        self.args: list = get_args(cmd)  # Аргументы
        self.name: str = func.__name__  # Имя команды
        self.doc: str = func.__doc__  # Документация к команде
        self.re: str = get_re(cmd)  # Регулярка команды
        self.func: object = func  # Функция команды
        self.cmd: str = cmd  # Сама команда


class Cli:
    def __init__(self) -> None:
        """Иницаилазиция CLI"""
        self.__last_cmd: tuple = ()  # Предыдущая команда
        self.__list_cmd: list = []  # Список команд
        self.Logger: Logger = Logger()  # Инициализация логгера
        self.copy: str = "Самара Гальцев, Дорогавцев 2020"  # Разработчики

    def cmd(self, command: str):
        """Декоратор который связывает переданную команду и функцией"""

        def wrapper(func):
            cmd: Cmd = Cmd(command, func)
            self.__list_cmd.append(cmd)
        return wrapper

    def run(self) -> None:
        """Запуск интерфейса"""

        self.__create_cmd()
        self.clear()
        print(f'\n{self.copy}\n')
        while True:
            msg: str = '$'
            cmd: str = input(msg)

            if cmd:
                self.__last_cmd = self.__handler(cmd)

    def __handler(self, command) -> None:
        """Обработчик команд"""

        __found_cmd: Cmd = self.__found(command)
        if __found_cmd:
            kwargs: dict = {}
            command_split: list = command.split()
            for arg in __found_cmd.args:
                kwargs.update({arg[0]: self.__type_(arg[1], command_split[arg[2]])})

            if __found_cmd.args_inline:
                for arg in __found_cmd.args_inline:
                    date: str = datetime.datetime.now().strftime('%H:%M:%S')
                    msg: str = f'[{date}] INPUT: {arg[0]} - '
                    kwargs.update({arg[0]: self.__type_(arg[1], input(msg))})

            ret = __found_cmd.func(**kwargs)

            if ret:
                self.Logger.info(ret, prefix='RETURN')

            return __found_cmd, kwargs

    def __found(self, command) -> Cmd:
        """Поиск команды в списке"""

        for cmd in self.__list_cmd:
            res: list = re.findall(cmd.re, command)

            if res:
                if len(command.split()) == len(cmd.re.split()):
                    return cmd

        self.Logger.warn('Команда не найдена')

    def __type_(self, type_: str, arg: str):
        """Преведение типов"""

        return eval(f'{type_}({arg})') if type_ != 'str' else arg

    def clear(self) -> None:
        """Очистка терминала"""

        os.system('cls||clear')

    def exit(self) -> None:
        """Выход из терминала"""

        exit()

    def help(self) -> None:
        """Список команд"""

        msg: str = f'"function"{14*" "}|{60*" "}"cmd"{60*" "}| "doc"'
        self.Logger.info(msg, prefix='HELP')

        for cmd in self.__list_cmd:
            msg: str = f'{cmd.name}{(24-len(cmd.name)) * " "}| {cmd.cmd}{(124-len(cmd.cmd)) * " "}| {cmd.doc}'
            self.Logger.info(msg, prefix='HELP')

    def __create_cmd(self) -> None:
        """Создание стдантартных комманд"""

        commands: list = [{'cmd': 'help',
                      'func': self.help},
                     {'cmd': 'exit',
                      'func': self.exit},
                     {'cmd': 'clear',
                      'func': self.clear}
                     ]
        for cmd in commands:
            cmd_: Cmd = Cmd(cmd['cmd'], cmd['func'])
            self.__list_cmd.append(cmd_)


class Logger:
    def info(self, msg: str, prefix: str = 'INFO') -> None:
        """Вывод info"""
        date = datetime.datetime.now().strftime('%H:%M:%S')
        msg = f'[{date}] {prefix}: {msg}'
        print(msg)

    def warn(self, msg: str) -> None:
        """Вывод warn"""

        date = datetime.datetime.now().strftime('%H:%M:%S')
        msg = f'[{date}] WARN: {msg}'
        print(msg)


def get_args_inline(command: str) -> list:
    args_inline = re.findall('<\\w+:\\w+:\\w+>', command)
    result = [(re.findall('<\\w+:', arg)[0][1:-1],
               re.findall(':\\w+:', arg)[0][1:-1],
               'inline') for arg in args_inline]

    return result


def get_args(command: str) -> list:
    args = re.findall('<\\w+:\\w+>', command)
    split_command = command.split()
    result = [(re.findall('<\\w+:', arg)[0][1:-1],
               re.findall(':\\w+>', arg)[0][1:-1],
               split_command.index(arg)) for arg in args]

    return result


def get_re(command: str) -> str:
    args_inline = re.findall('<\\w+:\\w+:\\w+>', command)
    args = re.findall('<\\w+:\\w+>', command)

    for arg in args_inline:
        command = command.replace(f' {arg}', '')

    for arg in args:
        command = command.replace(f'{arg}', '\\w+')

    return command