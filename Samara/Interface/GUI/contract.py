from web3 import Web3, HTTPProvider

from settings import settings

w3 = Web3(HTTPProvider(f'HTTP://{settings["Contract"]["host"]}:{settings["Contract"]["port"]}'))


class ContractError(Exception):
    def __init__(self, text):
        self.text = text


def isConnected(func):
    def wrapper(*args, **kwargs):
        if w3.isConnected():
            res = func(*args, **kwargs)
            return res
        else:
            raise ContractError('Нет подключение к контракту')

    return wrapper


class Contract:
    @staticmethod
    def main(wallet: str) -> w3:
        w3.eth.defaultAccount = wallet
        exchange = w3.eth.contract(
            address=settings['Contract']['main']['address'],
            abi=settings['Contract']['main']['abi']
        )

        return exchange

    @staticmethod
    def mainSys() -> w3:
        w3.eth.defaultAccount = w3.geth.personal.list_accounts[0]
        exchange = w3.eth.contract(
            address=settings['Contract']['main']['address'],
            abi=settings['Contract']['main']['abi']
        )

        return exchange

    @staticmethod
    def insurance(wallet: str) -> w3:
        w3.eth.defaultAccount = wallet
        exchange = w3.eth.contract(
            address=settings['Contract']['insurance']['address'],
            abi=settings['Contract']['insurance']['abi']
        )

        return exchange

    @staticmethod
    def insuranceSys() -> w3:
        w3.eth.defaultAccount = w3.geth.personal.list_accounts[0]
        exchange = w3.eth.contract(
            address=settings['Contract']['insurance']['address'],
            abi=settings['Contract']['insurance']['abi']
        )

        return exchange

    @staticmethod
    def dps(wallet: str) -> w3:
        w3.eth.defaultAccount = wallet
        exchange = w3.eth.contract(
            address=settings['Contract']['dps']['address'],
            abi=settings['Contract']['dps']['abi']
        )

        return exchange

    @staticmethod
    def dpsSys() -> w3:
        w3.eth.defaultAccount = w3.geth.personal.list_accounts[0]
        exchange = w3.eth.contract(
            address=settings['Contract']['dps']['address'],
            abi=settings['Contract']['dps']['abi']
        )

        return exchange


class User:
    @staticmethod
    @isConnected
    def logIn(wallet: str, private_key: str) -> dict:
        """Авторизация"""

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            result = contract.functions.authorization().call()
            w3.geth.personal.lock_account(wallet)

            if result > 0:
                return {'status': True, 'msg': 'Авторизация прошла успешно', 'role': result}
            elif result == 0:
                return {'status': False, 'msg': 'Пользователь не найден'}
            else:
                return {'status': False, 'msg': 'Ошибка авторизации'}
        except:
            return {'status': False, 'msg': 'Ошибка авторизации'}

    @staticmethod
    @isConnected
    def register(wallet: str, private_key: str, fio: str) -> dict:
        """Регистрация аккаунта"""

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            contract.functions.registration(fio).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Регистрация аккаунта прошла успешно'}
        except:
            return {'status': False, 'msg': 'Ошибка регистрации аккаунта'}

    @staticmethod
    @isConnected
    def getUserInfo(wallet: str) -> dict:
        """Информация о пользователе"""

        try:
            contract: w3 = Contract.main(wallet)
            info = contract.functions.getUserInfo(wallet).call()
            balance = w3.eth.getBalance(wallet)

            return {'status': True, 'msg': 'Информация о пользователе успешно получена',
                    'info': {
                        'wallet': wallet,
                        'balance': balance,
                        'fio': info[0],
                        'driver_licence': info[1],
                        'exp': info[2],
                        'dtp_value': info[3],
                        'not_fines': info[4],
                        'role': info[5]
                    }}
        except:
            return {'status': False, 'msg': 'Ошибка получении информации о пользователе'}

    @staticmethod
    @isConnected
    def addNewCategory(wallet: str, private_key: str, catA: bool, catB: bool, catC: bool) -> dict:
        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.addNewCategory(catA, catB, catC).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Новая категория успешно добавлена'}
        except:
            return {'status': False, 'msg': 'Ошибка добавления новой категории'}

    @staticmethod
    @isConnected
    def getFines(wallet: str) -> dict:
        """ Список штрафов """

        try:
            contract: w3 = Contract.dps(wallet)
            fines = contract.functions.getFines(wallet).call()

            return {'status': True, 'msg': 'Cписок штрафов успешно получен',
                    'fines': fines}
        except:
            return {'status': False, 'msg': 'Ошибка получения списка штрафов'}

    @staticmethod
    @isConnected
    def getInsuranceHistory(wallet: str) -> dict:
        """ История страховок """

        try:
            contract: w3 = Contract.insurance(wallet)
            insurance_history = contract.functions.getInsuranceHistory().call()

            return {'status': True, 'msg': 'История страховок успешно получен', 'insurance_history': insurance_history}
        except:
            return {'status': False, 'msg': 'Ошибка получения истории страховок'}

    @staticmethod
    @isConnected
    def getInsurance(wallet: str, id_car: int) -> dict:
        """ Информация о страховке конкретного ТС"""

        try:
            contract: w3 = Contract.insurance(wallet)
            info_insurance = contract.functions.getInsurance(wallet, id_car).call()

            return {'status': True, 'msg': 'Информация о страховке успешно получен',
                    'info_insurance': {
                        'id': info_insurance[0],
                        'id_car': info_insurance[1],
                        'validity': info_insurance[2],
                        'price_insurance': info_insurance[3]
                    }}
        except:
            return {'status': False, 'msg': 'Ошибка получения информации о страховке'}

    @staticmethod
    @isConnected
    def getCar(wallet: str, id_car: int) -> dict:
        """ Информация о ТС """

        try:
            contract: w3 = Contract.main(wallet)
            info_car = contract.functions.getCar(wallet, id_car).call()

            return {'status': True, 'msg': 'Информация о ТС успешно получен',
                    'info_car': {
                        'id': info_car[0],
                        'model': info_car[1],
                        'category': info_car[2],
                        'market_price': info_car[3],
                        'insurance_price': info_car[4],
                        'validity': info_car[5]
                    }}
        except:
            return {'status': False, 'msg': 'Ошибка получения информации о ТС'}

    @staticmethod
    @isConnected
    def getCars(wallet: str) -> dict:
        """ Список ТС пользователя  """

        try:
            contract: w3 = Contract.main(wallet)
            cars = contract.functions.getCars(wallet).call()

            return {'status': True, 'msg': 'Информация о списке ТС пользователя успешно получен',
                    'cars': cars}
        except:
            return {'status': False, 'msg': 'Ошибка получения информации о списке ТС пользователя'}

    @staticmethod
    @isConnected
    def getDTP(wallet: str) -> dict:
        """ Список всех ДТП пользователя  """

        try:
            contract: w3 = Contract.dps(wallet)
            dtp = contract.functions.getDTP().call()

            return {'status': True, 'msg': 'Информация о списке ДТП пользователя успешно получен',
                    'dtp': dtp}
        except:
            return {'status': False, 'msg': 'Ошибка получения информации о списке ДТП пользователя'}

    @staticmethod
    @isConnected
    def addDL(wallet: str, private_key: str, experience: int, number: int, validity: int,
              catA: bool,
              catB: bool,
              catC: bool) -> dict:
        """ Добавить вод.удост  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.addDL(experience, number, validity, catA, catB, catC).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Вод.удост успешно добавлено'}
        except:
            return {'status': False, 'msg': 'Ошибка добавления вод.удост'}

    @staticmethod
    @isConnected
    def addNewDL(wallet: str, private_key: str, catA: bool, catB: bool, catC: bool) -> dict:
        """ Зарегистрировать новое вод.удост  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.addNewDL(catA, catB, catC).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Вод.удост успешно отправлено на подветрждение'}
        except:
            return {'status': False, 'msg': 'Ошибка отправки нового вод.удост на подтверждение'}

    @staticmethod
    @isConnected  # pyable
    def buyInsurance(wallet: str, private_key: str, id_car: int) -> dict:
        """Регистрация страховки"""

        try:
            value: int = User.requestInsurance(wallet, id_car)['price']
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.insurance(wallet)
            contract.functions.buyInsurance(id_car).transact(
                {'to': settings['Contract']['insurance']['address'], 'value': value})
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Регистрация страховки прошла успешно'}
        except:
            return {'status': False, 'msg': 'Ошибка регистрации страховки'}

    @staticmethod
    @isConnected
    def requestInsurance(wallet: str, car_id: int) -> dict:
        """Узнать стоимость страховки"""

        try:
            contract: w3 = Contract.insurance(wallet)
            price = contract.functions.requestInsurance(car_id).call()

            return {'status': True, 'msg': f'Стоимость страховки {price}',
                    'price': price}
        except:
            return {'status': False, 'msg': 'Ошибка получения стоимости страховки'}

    @staticmethod
    @isConnected  # pyable
    def payFine(wallet: str, private_key: str, id_fine: int) -> dict:
        """Оплатить штраф"""

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.payFine(id_fine).transact(
                {'to': settings['Contract']['dps']['address'], 'value': 10000000000000000000})
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Штраф успешно оплачен'}
        except:
            return {'status': False, 'msg': 'Ошибка оплаты штрафа'}

    @staticmethod
    @isConnected
    def addCar(wallet: str, private_key: str, model: str, category: str, market_price: int,
               year: int) -> dict:
        """Добавить ТС"""

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            if category == 'A':
                category = 0
            elif category == 'B':
                category = 1
            elif category == 'C':
                category = 2
            else:
                return {'status': False, 'msg': 'Недопустимая категория ТС'}

            contract.functions.addCar(model, category, market_price, year).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'ТС успешно добавлен'}
        except:
            return {'status': False, 'msg': 'Ошибка добавления ТС'}

    @staticmethod
    @isConnected
    def changeUserInfo(wallet: str, private_key: str, fio: str) -> dict:
        """Изменить информация о пользователе"""

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            contract.functions.changeUserInfo(fio).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Информация о пользователе успешно изменена'}
        except:
            return {'status': False, 'msg': 'Ошибка изменения информации о пользователе'}


class DPS:
    @staticmethod
    @isConnected
    def giveFine(wallet: str, private_key: str, number_dl: int) -> dict:
        """ Выдать штраф пользователю  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            fines = contract.functions.giveFine(number_dl).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Штраф успешно выдан'}
        except:
            return {'status': False, 'msg': 'Ошибка выдачи штрафа'}

    @staticmethod
    @isConnected
    def confirmDTP(wallet: str, private_key: str, number_dl: int, id_car: int) -> dict:
        """ Подтвердить ДТП  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.confirmDTP(number_dl, id_car).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'ДТП успешно подтверждено'}
        except:
            return {'status': False, 'msg': 'Ошибка подтверждения ДТП'}

    @staticmethod
    @isConnected
    def acceptNewDL(wallet: str, private_key: str, number_dl: int) -> dict:
        """ Принять новое вод.удост  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.acceptNewDL(number_dl).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Вод.удост успешно принято'}
        except:
            return {'status': False, 'msg': 'Не удалось принять новое вод.удост'}

    @staticmethod
    @isConnected
    def getRequestsDL(wallet: str) -> dict:
        """Список новых вод.удост"""

        try:
            contract: w3 = Contract.dps(wallet)
            driver_licences = contract.functions.getRequestsDL().call()

            return {'status': True, 'msg': 'Список новых вод.удост успешно получен',
                    'driver_licences': driver_licences}
        except:
            return {'status': False, 'msg': 'Ошибка получения списка новых вод.удост'}

    @staticmethod
    @isConnected
    def acceptNewCategory(wallet: str, private_key: str, id_category: int) -> dict:
        """ Принять новую категорию для вод.удост """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.acceptNewCategory(id_category).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Категория вод.удост успешно принято'}
        except:
            return {'status': False, 'msg': 'Не удалось принять новую категорию вод.удост'}

    @staticmethod
    @isConnected
    def getRequestsNewCategory(wallet: str) -> dict:
        """Список новых категорий вод.удост"""

        try:
            contract: w3 = Contract.dps(wallet)
            driver_licences = contract.functions.getRequestsNewCategory().call()

            return {'status': True, 'msg': 'Список категорий на подверждения для вод.удост успешно получен',
                    'driver_licences': driver_licences}
        except:
            return {'status': False, 'msg': 'Ошибка получения списка категорий на подверждения для вод.удост'}


class Wallet:
    @staticmethod
    @isConnected
    def register(private_key: str) -> dict:
        """Регистрация нового кошелька"""

        try:
            wallet = w3.geth.personal.new_account(private_key)

            return {'status': True, 'msg': 'Регистрация кошелька прошла успешно', 'wallet': wallet}
        except:
            return {'status': False, 'msg': 'Ошибка регистрации кошелька'}


class Admin:
    @staticmethod
    @isConnected
    def addDPS(wallet: str, private_key: str, wallet_user: str) -> dict:
        """ Выдать роль сотрудника ДПС  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.addDPS(wallet_user).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Роль сотрудника ДПС успешно выдана'}
        except:
            return {'status': False, 'msg': 'Ошибка выдачи роли'}

    @staticmethod
    @isConnected
    def removeDPS(wallet: str, private_key: str, wallet_user: str) -> dict:
        """ Снять с роли сотрудника ДПС  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.dps(wallet)
            contract.functions.removeDPS(wallet_user).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Роль сотрудника ДПС успешно снята'}
        except:
            return {'status': False, 'msg': 'Ошибка снятия с роли'}


class Bank:
    @staticmethod
    @isConnected  # pyable
    def sendETH(wallet: str, private_key: str, value: int) -> dict:
        """ Зачислить деньги на контракт банка  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            contract.functions.sendETH().transact({'to': settings['Contract']['main']['address'], 'value': value})
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Деньги успешно зачислены'}
        except:
            return {'status': False, 'msg': 'Ошибка зачисления денег'}

    @staticmethod
    @isConnected
    def withdrawETH(wallet: str, private_key: str, value: int) -> dict:
        """ Зачислить деньги на контракт банка  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            contract.functions.withdrawETH(value).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Деньги успешно сняты'}
        except:
            return {'status': False, 'msg': 'Ошибка снятия денег'}

    @staticmethod
    @isConnected
    def getBalanceETH(wallet: str) -> dict:
        """ Просмотр баланса банка  """

        try:
            contract: w3 = Contract.main(wallet)
            balance_contract: int = contract.functions.getBalanceETH().call()

            return {'status': True, 'msg': 'Баланс успешн получен', 'balance_contract': balance_contract}
        except:
            return {'status': False, 'msg': 'Ошибка получения баланса'}


class Insurance:
    @staticmethod
    @isConnected  # pyable
    def sendETH(wallet: str, private_key: str, value: int) -> dict:
        """ Зачислить деньги на контракт страховой  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            contract.functions.sendETH().transact({'to': settings['Contract']['main']['address'], 'value': value})
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Деньги успешно зачислены'}
        except:
            return {'status': False, 'msg': 'Ошибка зачисления денег'}

    @staticmethod
    @isConnected
    def withdrawETH(wallet: str, private_key: str, value: int) -> dict:
        """ Зачислить деньги на контракт страховой  """

        try:
            w3.geth.personal.unlock_account(wallet, private_key, 10)
            contract: w3 = Contract.main(wallet)
            contract.functions.withdrawETH(value).transact()
            w3.geth.personal.lock_account(wallet)

            return {'status': True, 'msg': 'Деньги успешно сняты'}
        except:
            return {'status': False, 'msg': 'Ошибка снятия денег'}

    @staticmethod
    @isConnected
    def getBalanceETH(wallet: str) -> dict:
        """ Просмотр баланса страховой  """

        try:
            contract: w3 = Contract.main(wallet)
            balance_contract: int = contract.functions.getBalanceETH().call()

            return {'status': True, 'msg': 'Баланс успешн получен', 'balance_contract': balance_contract}
        except:
            return {'status': False, 'msg': 'Ошибка получения баланса'}

    @staticmethod
    @isConnected
    def getInsuranceDebt(wallet: str) -> dict:
        """ Просмотр долга страховой  """

        try:
            contract: w3 = Contract.main(wallet)
            debt: int = contract.functions.getInsuranceDebt().call()

            return {'status': True, 'msg': 'Долг успешн получен', 'debt': debt}
        except:
            return {'status': False, 'msg': 'Ошибка получения долга'}

    @staticmethod
    @isConnected
    def getBalanceETH(wallet: str) -> dict:
        """ Просмотр баланса страховой  """

        try:
            contract: w3 = Contract.main(wallet)
            balance_contract: int = contract.functions.getBalanceETH().call()

            return {'status': True, 'msg': 'Баланс успешн получен', 'balance_contract': balance_contract}
        except:
            return {'status': False, 'msg': 'Ошибка получения баланса'}