from datetime import datetime as dt
import functools

from handler import Cli
from contract import User, Admin, Wallet, DPS, Bank, Insurance, w3
from settings import settings

cli = Cli()


def access(list_role: list):
    def wrapper(func):
        @functools.wraps(func)
        def foo(*args, **kwargs):
            if functional.role in list_role:
                return func(*args, **kwargs)
            else:
                msg = 'Нет доступа'
                cli.Logger.warn(msg)
        return foo
    return wrapper


class Functional:
    logIn: bool = False
    wallet: str = ''
    role: int = 0
    session_role: int = 0
    
    @staticmethod
    @cli.cmd('session dps <private_key:str>')
    def dps(private_key: str) -> None:
        """Зайти в роль сотрудника ДПС"""

        if w3.isConnected():
            if functional.session_role == 2:
                if functional.role == 2:
                    msg = 'Вы уже в роли сотрудника ДПС'
                    cli.Logger.warn(msg)
                elif functional.role == 1:
                    try:
                        w3.geth.personal.unlock_account(functional.wallet, private_key, 10)
                        functional.role: int = 2
                        w3.geth.personal.lock_account(functional.wallet)
                        cli.Logger.info('Сессия изменена')
                    except:
                        cli.Logger.warn('Ошибка изменения сессия')
            else:
                msg = 'Нет доступа'
                cli.Logger.warn(msg)

        else:
            msg = 'Нет соединения с контрактом'
            cli.Logger.warn(msg)

    @staticmethod
    @cli.cmd('session user <private_key:str>')
    def user(private_key: str) -> None:
        """Зайти в роль водителя"""

        if w3.isConnected():
            if functional.session_role == 2:
                if functional.role == 1:
                    msg = 'Вы уже в роли водителя'
                    cli.Logger.warn(msg)
                elif functional.role == 2:
                    try:
                        w3.geth.personal.unlock_account(functional.wallet, private_key, 10)
                        functional.role: int = 1
                        w3.geth.personal.lock_account(functional.wallet)
                        cli.Logger.info('Сессия изменена')
                    except:
                        cli.Logger.warn('Ошибка изменения сессия')
            else:
                msg = 'Нет доступа'
                cli.Logger.warn(msg)
        else:
            msg = 'Нет соединения с контрактом'
            cli.Logger.warn(msg)

    @staticmethod
    @cli.cmd('login <wallet:str:inline> <private_key:str:inline>')
    @access([0])
    def logIn(wallet: str, private_key: str) -> None:
        """Авторизация"""
    
        response: dict = User.logIn(wallet, private_key)
    
        if response['status']:
            functional.logIn: bool = True
            functional.wallet: str = wallet
            functional.role: int = response['role']
            functional.session_role: int = response['role']
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('register wallet <private_key:str>')
    @access([0])
    def registerWallet(private_key: str) -> None:
        """Регистрация нового кошелька"""
    
        response: dict = Wallet.register(private_key)
    
        if response['status']:
            msg = f'Кошелёк - {response["wallet"]}'
            cli.Logger.info(msg)
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('register <wallet:str:inline> <private_key:str:inline> <surname:str:inline> <name:str:inline> <middlename:str:inline>')
    @access([0])
    def register(wallet: str, private_key: str, surname: str, name: str, middlename: str) -> None:
        """Регистрация"""
    
        fio: str = f'{surname} {name} {middlename}'
        response: dict = User.register(wallet, private_key, fio)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get info')
    @access([1, 2, 3, 4, 5])
    def getUserInfo() -> None:
        """Информация о пользователе"""
    
        response: dict = User.getUserInfo(functional.wallet)
        if response['status']:
            cli.Logger.info(response['msg'])
    
            if functional.role == 1:
                cli.Logger.info(f'Роль - Водитель', prefix='LK')
                cli.Logger.info(f'ФИО - {response["info"]["fio"]}', prefix='LK')
                cli.Logger.info(f'Кошелёк - {response["info"]["wallet"]}', prefix='LK')
                cli.Logger.info(f'Баланс - {response["info"]["balance"]}', prefix='LK')
                if response["info"]["driver_licence"][0]:
                    cli.Logger.info(f'Вод.удост - {response["info"]["driver_licence"][0]} | {dt.strftime(dt.fromtimestamp(response["info"]["driver_licence"][1]), "%d.%m.%Y %H:%M:%S")} | '
                                    f'{"A" if response["info"]["driver_licence"][2] else ""} {"B" if response["info"]["driver_licence"][3] else ""} {"C" if response["info"]["driver_licence"][4] else ""}', prefix='LK')
                else:
                    cli.Logger.info(f'Вод.удост - нет', prefix='LK')
                    cli.Logger.info(f'Опыт вождения - {response["info"]["exp"]}', prefix='LK')
                    cli.Logger.info(f'Кол-во ДТП - {response["info"]["dtp_value"]}', prefix='LK')
                    cli.Logger.info(f'Кол-во неоплаченных штрафов - {response["info"]["not_fines"]}', prefix='LK')
            elif functional.role == 2:
                cli.Logger.info(f'Роль - сотрудник ДПС', prefix='LK')
                cli.Logger.info(f'ФИО - {response["info"]["fio"]}', prefix='LK')
                cli.Logger.info(f'Кошелёк - {response["info"]["wallet"]}', prefix='LK')
            elif functional.role == 3:
                cli.Logger.info(f'Роль - Админ', prefix='LK')
                cli.Logger.info(f'Кошелёк - {response["info"]["wallet"]}', prefix='LK')
                cli.Logger.info(f'Баланс - {response["info"]["balance"]}', prefix='LK')
            elif functional.role == 4:
                balance_contract: int = Bank.getBalanceETH(functional.wallet)['balance_contract']
                balance: int = w3.eth.getBalance(functional.wallet)

                cli.Logger.info(f'Роль - Банк', prefix='LK')
                cli.Logger.info(f'Кошелёк - {response["info"]["wallet"]}', prefix='LK')
                cli.Logger.info(f'Баланс - {balance}', prefix='LK')
                cli.Logger.info(f'Баланс контракта - {balance_contract}', prefix='LK')
            elif functional.role == 5:
                balance: int = w3.eth.getBalance(functional.wallet)
                debt: int = Insurance.getInsuranceDebt(functional.wallet)['debt']
                balance_contract: int = Insurance.getBalanceETH(functional.wallet)['balance_contract']

                cli.Logger.info(f'Роль - Страховая', prefix='LK')
                cli.Logger.info(f'Кошелёк - {response["info"]["wallet"]}', prefix='LK')
                cli.Logger.info(f'Баланс - {balance}', prefix='LK')
                cli.Logger.info(f'Баланс контракта - {balance_contract}', prefix='LK')
                cli.Logger.info(f'Долг - {debt}', prefix='LK')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('add new category <catA:bool> <catB:bool> <catC:bool> <private_key:str>')
    @access([1])
    def addNewCategory(private_key: str, catA: bool, catB: bool, catC: bool) -> None:
        """Добавить новую категорию ТС в права"""
    
        response: dict = User.addNewCategory(functional.wallet, private_key, catA, catB, catC)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get fines')
    @access([1])  # unix
    def getFines() -> None:
        """Мои штрафы"""
    
        response: dict = User.getFines(functional.wallet)
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
    
            msg: str = f'"ID"{6 * " "}|{8 * " "}"Time"{17 * " "}| "Status"'
            cli.Logger.info(msg, prefix='FINE')
    
            for fine in response['fines']:
                msg: str = f'{fine[0]}{(10 - len(str(fine[0]))) * " "}| {dt.strftime(dt.fromtimestamp(fine[1]), "%d.%m.%Y %H:%M:%S")}{(30 - len(str(dt.strftime(dt.fromtimestamp(fine[1]), "%d.%m.%Y %H:%M:%S")))) * " "}| {"Оплачено" if fine[2] else "Не оплачено"}'
                cli.Logger.info(msg, prefix='FINE')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get insurance')
    @access([1])   # unix
    def getInsuranceHistory() -> None:
        """История страховок"""
    
        response: dict = User.getInsuranceHistory(functional.wallet)
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
            msg: str = f'"ID"{6 * " "}|{3 * " "}"Car ID"{3 * " "} | {8 * " "}"Time"{7 * " "} | "Price"'
            cli.Logger.info(msg, prefix='INS')
    
            for insurance in response['insurance_history']:
                msg: str = f'{insurance[0]}{(9 - len(str(insurance[0]))) * " "} | {insurance[1]}{(14 - len(str(insurance[1]))) * " "}| {insurance[2]}{(21 - len(str(dt.strftime(dt.fromtimestamp(insurance[2]), "%d.%m.%Y %H:%M:%S")))) * " "} | {insurance[3]}'
                cli.Logger.info(msg, prefix='INS')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get insurance car <id_car:int>')
    @access([1])  # unix
    def getInsurance(id_car: int) -> None:
        """Информация о страховке конкретного ТС"""
    
        response: dict = User.getInsurance(functional.wallet, id_car)
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
            msg: str = f'"ID"{6 * " "}|{3 * " "}"Car ID"{3 * " "} | {8 * " "}"Time"{7 * " "} | "Price"'
            cli.Logger.info(msg, prefix='FINE')
    
            insurance: dict = response['insurance_history']
            msg: str = f'{insurance["id"]}{(9 - len(str(insurance["id"]))) * " "} | {insurance["id_car"]}{(14 - len(str(insurance["id_car"]))) * " "}| {insurance["validity"]}{(21 - len(str(dt.strftime(dt.fromtimestamp(insurance["validity"]), "%d.%m.%Y %H:%M:%S")))) * " "} | {insurance["price_insurance"]}'
            cli.Logger.info(msg, prefix='FINE')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get car <id_car:int>')
    @access([1])
    def getCar(id_car: int) -> None:
        """Информация о конкретном ТС"""
    
        response: dict = User.getCar(functional.wallet, id_car)
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
            msg: str = f'"ID"{6 * " "}|{20 * " "}"Model"{20 * " "}| {3 * " "}"Category"{3 * " "} | {7 * " "}"Market price"{7 * " "} |  {7 * " "}"Insurance price"{7 * " "} | Use time'
            cli.Logger.info(msg, prefix='CAR')
    
            info_car: dict = response['info_car']
            msg: str = f'{info_car["id"]}{(10-len(str(info_car["id"]))) * " "}| {info_car["model"]}{(45 - len(info_car["model"])) * " "} | {info_car["category"]}{(17 - len(info_car["category"])) * " "}| {info_car["market_price"]}{(28 - len(str(info_car["market_price"]))) * " "} | {info_car["insurance_price"]}{(32 - len(str(info_car["insurance_price"]))) * " "} | {info_car["validity"]}'
            cli.Logger.info(msg, prefix='CAR')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get cars')
    @access([1])
    def getCars() -> None:
        """Список всех ТС пользователя"""
    
        response: dict = User.getCars(functional.wallet)
        cat = ''
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
            msg: str = f'"ID"{6 * " "}|{20 * " "}"Model"{20 * " "}| {3 * " "}"Category"{3 * " "} | {7 * " "}"Market price"{7 * " "} |  {7 * " "}"Insurance price"{7 * " "} | Use time'
            cli.Logger.info(msg, prefix='CARS')
    
            for car in response['cars']:
                if car[2] == 0:
                    cat = 'A'
                elif car[2] == 1:
                    cat = 'B'
                elif car[2] == 2:
                    cat = 'C'
                msg: str = f'{car[0]}{(10-len(str(car[0]))) * " "}| {car[2]}{(45 - len(str(car[2]))) * " "} | {cat}{(17 - len(str(cat))) * " "}| {car[3]}{(28 - len(str(car[3]))) * " "} | {car[4]}{(32 - len(str(car[4]))) * " "} | {car[5]}'
                cli.Logger.info(msg, prefix='CARS')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get dtp')  # unix
    @access([1])
    def getDTP() -> None:
        """Список всех ДТП пользователя"""
    
        response: dict = User.getDTP(functional.wallet)
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
            msg: str = f'"ID"{6 * " "}|{10 * " "}"ID Car"{10 * " "}| Time'
            cli.Logger.info(msg, prefix='DTP')
            for dtp in response['dtp']:
                msg: str = f'{dtp[0]}{(10-len(str(dtp[0]))) * " "}| {dtp[1]}{(26 - len(str(dtp[1]))) * " "} | {dt.strftime(dt.fromtimestamp(dtp[2]), "%d.%m.%Y %H:%M:%S")}'
                cli.Logger.info(msg, prefix='DTP')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('add dl <experience:int> <number:int>'
             ' <validity:str> <catA:bool> <catB:bool> <catC:bool> <private_key:str:inline>')
    @access([1])  # unix (validity)
    def addDL(private_key: str, experience: int, number: int, validity: str, catA: bool, catB: bool, catC: bool) -> None:
        """Добавить вод.удост  формат даты - (ДД.ММ.ГГГГ)"""
        validity = dt.strptime(validity, "%d.%m.%Y")
        validity = int(validity.timestamp())
        response: dict = User.addDL(functional.wallet, private_key, experience, number, validity, catA, catB, catC)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('add new dl <catA:bool> <catB:bool> <catC:bool> <private_key:str:inline>')
    @access([1])
    def addNewDL(private_key: str, catA: bool, catB: bool, catC: bool) -> None:
        """Зарегистрировать новое вод.удост"""
    
        response: dict = User.addNewDL(functional.wallet, private_key, catA, catB, catC)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('buy insurance <id_car:int> <private_key:str>')
    @access([1])
    def buyInsurance(private_key: str, id_car: int) -> None:
        """Регистрация страховки"""
    
        response: dict = User.buyInsurance(functional.wallet, private_key, id_car)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('info price insurance <id_car:int>')
    @access([1])
    def requestInsurance(id_car: int) -> None:
        """Узнать стоимость страховки"""
    
        response: dict = User.requestInsurance(functional.wallet, id_car)
    
        if response['status']:
            cli.Logger.info(f'Стоимость страховки {response["price"]}')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('pay fine <id_fine:int> <private_key:str>')
    @access([1])
    def payFine(private_key: str, id_fine: int) -> None:
        """Оплатить штраф"""
    
        response: dict = User.payFine(functional.wallet, private_key, id_fine)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('add car <model:str> <category:str> <market_price:int> <year:int> <private_key:str:inline>')
    @access([1])
    def addCar(private_key: str, model: str, category: str, market_price: int,
                   year: int) -> None:
        """Добавить ТС"""
    
        response: dict = User.addCar(functional.wallet, private_key, model, category, market_price, year)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('change info <surname:str> <name:str> <middlename:str> <private_key:str:inline> ')
    @access([1, 2, 3])
    def changeUserInfo(private_key: str, surname: str, name: str, middlename: str) -> None:
        """Изменить информация о пользователе"""
    
        fio: str = f'{surname} {name} {middlename}'
        response: dict = User.changeUserInfo(functional.wallet, private_key, fio)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('give fine <number_dl:int> <private_key:str>')
    @access([2])
    def giveFine(private_key: str, number_dl: int) -> None:
        """Выдать штраф пользователю"""
    
        response: dict = DPS.giveFine(functional.wallet, private_key, number_dl)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('confirm dtp <id_car:int> <number_dl:int> <private_key:str>')
    @access([2])
    def confirmDTP(private_key: str, number_dl: int, id_car: int) -> None:
        """Подтвердить ДТП"""
    
        response: dict = DPS.confirmDTP(functional.wallet, private_key, number_dl, id_car)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('accept new dl <number_dl:int> <private_key:str>')
    @access([2])
    def acceptNewDL(private_key: str, number_dl: int) -> None:
        """Принять новое вод.удост"""
    
        response: dict = DPS.acceptNewDL(functional.wallet, private_key, number_dl)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get dl')
    @access([2])
    def getRequestsDL() -> None:
        """Список новых вод.удост"""
    
        response: dict = DPS.getRequestsDL(functional.wallet)
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
            msg: str = f'"ID"{6 * " "}|{20 * " "}"Wallet"{20 * " "}| Category'
            cli.Logger.info(msg, prefix='DL')
    
            for driver_licence in response['driver_licences']:
                msg: str = f'{driver_licence[0]}{(10 - len(str(driver_licence[0]))) * " "}| {driver_licence[2]}{(46 - len(driver_licence[2])) * " "} | {"A" if driver_licence[1][2] else ""} {"B" if driver_licence[1][3] else ""} {"C" if driver_licence[1][4] else ""}'
                cli.Logger.info(msg, prefix='DL')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('accept new category <id_category:int> <private_key:str>')
    @access([2])
    def acceptNewCategory(private_key: str, id_category: int) -> None:
        """Принять новую категорию для вод.удост """
    
        response: dict = DPS.acceptNewCategory(functional.wallet, private_key, id_category)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('get category')
    @access([2])
    def getRequestsNewCategory() -> None:
        """Список новых категорий вод.удост"""
    
        response: dict = DPS.getRequestsNewCategory(functional.wallet)
    
        if response['status']:
            cli.Logger.info(response['msg'])
    
            msg: str = f'"ID"{6 * " "}|{20 * " "}"Wallet"{20 * " "}| Category'
            cli.Logger.info(msg, prefix='CAT')
    
            for driver_licence in response['driver_licences']:
                msg: str = f'{driver_licence[0]}{(10 - len(str(driver_licence[0]))) * " "}| {driver_licence[1]}{(45 - len(driver_licence[1])) * " "} | {"A" if driver_licence[2][2] else ""} {"B" if driver_licence[2][3] else ""} {"C" if driver_licence[2][4] else ""}'
                cli.Logger.info(msg, prefix='CAT')
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('add dps <wallet_user:str> <private_key:str>')
    @access([3])
    def addDPS(private_key: str, wallet_user: str) -> None:
        """Выдать роль сотрудника ДПС"""
    
        response: dict = Admin.addDPS(functional.wallet, private_key, wallet_user)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('remove dps <wallet_user:str> <private_key:str>')
    @access([3])
    def removeDPS(private_key: str, wallet_user: str) -> None:
        """Снять с роли сотрудника ДПС"""
    
        response: dict = Admin.removeDPS(functional.wallet, private_key, wallet_user)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('bank send wei <value:int> <private_key:str>')
    @access([4])
    def sendETHBank(private_key: str, value: int) -> None:
        """Зачислить деньги на контракт банка """
    
        response: dict = Bank.sendETH(functional.wallet, private_key, value)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('bank withdraw wei <value:int> <private_key:str>')
    @access([4])
    def withdrawETHBank(private_key: str, value: int) -> None:
        """Cнять деньги с контракта банка """
    
        response: dict = Bank.withdrawETH(functional.wallet, private_key, value)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('insurance send wei <value:int> <private_key:str>')
    @access([5])
    def sendETHInsurance(private_key: str, value: int) -> None:
        """Зачислить деньги на контракт страховой """
    
        response: dict = Insurance.sendETH(functional.wallet, private_key, value)
    
        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('insurance withdraw wei <value:int> <private_key:str>')
    @access([5])
    def withdrawETHInsurance(private_key: str, value: int) -> None:
        """Cнять деньги с контракта страховой """

        response: dict = Insurance.withdrawETH(functional.wallet, private_key, value)

        if response['status']:
            cli.Logger.info(response['msg'])
        else:
            cli.Logger.warn(response['msg'])

    @staticmethod
    @cli.cmd('logout')
    @access([1, 2, 3, 4, 5])
    def logout() -> None:
        """Выйти из аккаунта """

        functional.logIn: bool = False
        functional.wallet: str = ''
        functional.role: int = 0
        functional.session_role: int = 0


if __name__ == '__main__':
    functional = Functional()
    cli.run()