from datetime import datetime as dt
import functools
import os

from flask import Flask, render_template, redirect, flash, session, request

from contract import User, Admin, Wallet, Bank, Insurance, DPS, w3
from settings import settings

app = Flask(__name__)


def isLogin(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if session.get('islogIn'):
            return func(*args, **kwargs)
        else:
            lastPage = '/'
            return render_template('html/main.html', lastPage=lastPage, logIn=True)
    return wrapper


@app.route('/user/login/', methods=['POST'])
def login() -> render_template:
    """Авторизация"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = request.form['wallet']
        private_key: str = request.form['private_key']

        response = User.logIn(wallet, private_key)
        if response['status']:
            session['islogIn'] = True
            session['wallet'] = wallet
            session['role'] = response['role']
            session['session_role'] = response['role']
            
            return redirect(lastPage)
        else:
            flash(response['msg'])
    return render_template('html/main.html', lastPage=lastPage, logIn=True)


@app.route('/user/register/', methods=['POST'])
def register() -> render_template:
    """Регистрация"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = request.form['wallet']
        private_key: str = request.form['private_key']
        name: str = request.form['name']
        surname: str = request.form['surname']
        middlename: str = request.form['middlename']

        fio: str = f'{surname} {name} {middlename}'

        response = User.register(wallet, private_key, fio)
        if response['status']:
            return render_template('html/main.html', lastPage=lastPage, register=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, register=True)


@app.route('/user/register/wallet/', methods=['POST'])
def registerWallet() -> render_template:
    """Регистрация кошелька"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        private_key: str = request.form['private_key']

        response: dict = Wallet.register(private_key)
        if response['status']:
            flash(response['wallet'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, registerWallet=True)


@app.route('/rider_licence/add/', methods=['POST'])
def addRiderLicence() -> render_template:
    """Добавить вод.удовст"""
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        number: int = int(request.form['number'])
        if 'catA' in request.form:
            catA: bool = True
        else:
            catA: bool = False
            
        if 'catB' in request.form:
            catB: bool = True
        else:
            catB: bool = False
            
        if 'catC' in request.form:
            catC: bool = True
        else:
            catC: bool = False
            
        experience: int = int(request.form['experience'])
        date_: str = request.form['date']
        private_key: str = request.form['private_key']

        date = dt.strptime(date_, '%Y-%d-%m')
        date = int(date.timestamp())
        response = User.addDL(wallet, private_key, experience, number, date, catA, catB, catC)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addRiderLicence=True)


@app.route('/rider_licence/category/add/', methods=['POST'])
def addNewCategory() -> render_template:
    """Добавить новую категорию ТС"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        if 'catA' in request.form:
            catA: bool = True
        else:
            catA: bool = False
            
        if 'catB' in request.form:
            catB: bool = True
        else:
            catB: bool = False
            
        if 'catC' in request.form:
            catC: bool = True
        else:
            catC: bool = False
        private_key: str = request.form['private_key']

        response = User.addNewCategory(wallet, private_key, catA, catB, catC)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addCategoryRiderLicence=True)


@app.route('/user/change/info/', methods=['POST'])
def changeUserInfo() -> render_template:
    """Изменить информацию"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        name: str = request.form['name']
        surname: str = request.form['surname']
        middlename: str = request.form['middlename']
        fio: str = f'{surname} {name} {middlename}'
        private_key: str = request.form['private_key']

        response: dict = User.changeUserInfo(wallet, private_key, fio)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, resetInfo=True)


@app.route('/insurence/add/', methods=['POST'])
def buyInsurance() -> render_template:
    """Купить страховку"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        car_id: int = int(request.form['car_id'])
        private_key: str = request.form['private_key']

        response: dict = User.buyInsurance(wallet, private_key, car_id)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addInsurence=True)


@app.route('/insurence/info/', methods=['POST'])
def requestInsurance() -> render_template:
    """Узнать смоимость страховки"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        car_id: int = int(request.form['car_id'])

        response: dict = User.requestInsurance(wallet, car_id)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, infoInsurence=True)


@app.route('/pay/fine/', methods=['POST'])
def payFine() -> render_template:
    """Оплатить штраф"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        id_fine: int = int(request.form['id_fine'])
        private_key: str = request.form['private_key']

        response: dict = User.payFine(wallet, private_key, id_fine)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, payFine=True)


@app.route('/dps/add/', methods=['POST'])
def addDps() -> render_template:
    """Добавить сотрудника ДПС"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        wallet_user: str = request.form['wallet_user']
        private_key: str = request.form['private_key']

        response: dict = Admin.addDPS(wallet, private_key, wallet_user)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addDps=True)


@app.route('/dps/remove/', methods=['POST'])
def removeDps() -> render_template:
    """Убрать сотрудника ДПС"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        wallet_user: str = request.form['wallet_user']
        private_key: str = request.form['private_key']

        response: dict = Admin.removeDPS(wallet, private_key, wallet_user)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, removeDps=True)


@app.route('/rider_licence/add/base/', methods=['POST'])
def addNewDL() -> render_template:
    """Зарегистрировать новые вод.удовст"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        private_key: str = request.form['private_key']
        if 'catA' in request.form:
            catA: bool = True
        else:
            catA: bool = False
            
        if 'catB' in request.form:
            catB: bool = True
        else:
            catB: bool = False
            
        if 'catC' in request.form:
            catC: bool = True
        else:
            catC: bool = False

        response = User.addNewDL(wallet, private_key, catA, catB, catC)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addRiderLicenceToBase=True)


@app.route('/fines/add/', methods=['POST'])
def giveFine() -> render_template:
    """Выдать штраф"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        private_key: str = request.form['private_key']
        number: int = int(request.form['number'])

        response: dict = DPS.giveFine(wallet, private_key, number)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addFines=True)


@app.route('/car/add/', methods=['POST'])
def addCar() -> render_template:
    """Добавить ТС"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        private_key: str = request.form['private_key']
        price: int = int(request.form['price'])
        model: str = request.form['model']
        category: str = request.form['category']
        year: int = int(request.form['year'])

        response: dict = User.addCar(wallet, private_key, model, category, price, year)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addCar=True)


@app.route('/dtp/add/', methods=['POST'])
def confirmDTP() -> render_template:
    """Подтвердить ДТП"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        private_key: str = request.form['private_key']
        number: int = int(request.form['number'])
        id_car: int = int(request.form['id_car'])

        response: dict = DPS.confirmDTP(wallet, private_key, number, id_car)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, addDtp=True)


@app.route('/rider_licence/accept/', methods=['POST'])
def acceptNewDL() -> render_template:
    """Принять новые вод.удовст"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        private_key: str = request.form['private_key']
        number: int = int(request.form['number'])

        response: dict = DPS.acceptNewDL(wallet, private_key, number)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, acceptRiderLicenses=True)


@app.route('/category/accept/', methods=['POST'])
def acceptNewCategory() -> render_template:
    """Принять новую категорию"""
    
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'

    if request.method == 'POST':
        wallet: str = session.get('wallet')
        private_key: str = request.form['private_key']
        id_category: int = int(request.form['id_category'])

        response: dict = DPS.acceptNewCategory(wallet, private_key, id_category)
        if response['status']:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, info=True)
        else:
            flash(response['msg'])
            return render_template('html/main.html', lastPage=lastPage, acceptNewCategory=True)


@app.route('/eth/send/', methods=['POST'])
def sendETH() -> render_template:
    """Зачислить деньги на контракт """

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    wallet: str = session.get('wallet')
    private_key: str = request.form['private_key']
    value: int = int(request.form['value'])
    response: dict = Bank.sendETH(wallet, private_key, int(value))

    if response['status']:
        flash(response['msg'])
        return render_template('html/main.html', lastPage=lastPage, info=True)
    else:
        flash(response['msg'])
        return render_template('html/main.html', lastPage=lastPage, sendETH=True)


@app.route('/eth/withdraw/', methods=['POST'])
def withdrawETH() -> render_template:
    """Cнять деньги с контракта """

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    wallet: str = session.get('wallet')
    private_key: str = request.form['private_key']
    value: int = int(request.form['value'])
    response: dict = Bank.withdrawETH(wallet, private_key, int(value))

    if response['status']:
        flash(response['msg'])
        return render_template('html/main.html', lastPage=lastPage, info=True)
    else:
        flash(response['msg'])
        return render_template('html/main.html', lastPage=lastPage, withdrawETH=True)


@app.route('/reset/role/', methods=['POST'])
def resetRole() -> redirect:
    """Смена роли """
    
    if session.get('session_role') == 2:
        wallet: str = session.get('wallet')
        private_key: str = request.form['private_key']
        w3.geth.personal.unlock_account(wallet, private_key, 10)
        if session.get('role') == 1:
            session['role'] = 2
        elif session.get('role') == 2:
            session['role'] = 1

        w3.geth.personal.lock_account(wallet)

    return redirect('/')

# -------


@app.route('/')
def main() -> render_template:
    """Главная страница"""
    
    islogIn: bool = True if session.get('islogIn') else False
    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    session['lastPage'] = '/'
    wallet: str = session.get('wallet')
    role: int = session.get('role')
    session_role: int = session.get('session_role')
    info: dict = {}

    if wallet:
        info: dict = User.getUserInfo(wallet)['info']
        if role == 4:
            balance_contract: int = Bank.getBalanceETH(wallet)['balance_contract']
            info.update({'balance_contract': balance_contract})
        elif role == 5:
            debt: int = Insurance.getInsuranceDebt(wallet)['debt']
            balance_contract: int = Insurance.getBalanceETH(wallet)['balance_contract']
            info.update({'balance_contract': balance_contract, 'debt': debt})

    return render_template('html/main.html', islogIn=islogIn, lastPage=lastPage, info=info, role=role, session_role=session_role, datetime=dt)


@app.route('/list/car/')
@isLogin
def getCars() -> render_template:
    """Список машин"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    islogIn: bool = True if session.get('islogIn') else False
    session['lastPage'] = '/list/car/'
    wallet: str = session.get('wallet')
    role: int = session.get('role')
    session_role: int = session.get('session_role')
    list_cars: list = []


    if wallet:
        info: dict = User.getUserInfo(wallet)['info']
        response: dict = User.getCars(wallet)
        if response['status']:
            list_cars: list = response['cars']

        return render_template('html/list_car.html', islogIn=islogIn, lastPage=lastPage, list_cars=list_cars, info=info, role=role, session_role=session_role, datetime=dt)


@app.route('/list/dtp/')
@isLogin
def getDTP() -> render_template:
    """Список ДТП"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    islogIn: bool = True if session.get('islogIn') else False
    wallet: str = session.get('wallet')
    session['lastPage'] = '/list/dtp/'
    role: int = session.get('role')
    session_role: int = session.get('session_role')
    list_dtp: list = []


    if wallet:
        info: dict = User.getUserInfo(wallet)['info']
        response = User.getDTP(wallet)
        if response['status']:
            list_dtp = response['dtp']

        return render_template('html/list_dtp.html', islogIn=islogIn, lastPage=lastPage, list_dtp=list_dtp, info=info, role=role, session_role=session_role, datetime=dt)


@app.route('/list/fines/')
@isLogin
def getFines() -> render_template:
    """Список штрафов"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    islogIn: bool = True if session.get('islogIn') else False
    wallet: str = session.get('wallet')
    session['lastPage'] = '/list/fines/'
    role: int = session.get('role')
    session_role: int = session.get('session_role')
    list_fines: list = []


    if wallet:
        info: dict = User.getUserInfo(wallet)['info']
        response = User.getFines(wallet)
        if response['status']:
            list_fines = response['fines']


        return render_template('html/list_fines.html', islogIn=islogIn, lastPage=lastPage, list_fines=list_fines, info=info, role=role, session_role=session_role, datetime=dt)


@app.route('/list/insurence/')
@isLogin
def getInsuranceHistory() -> render_template:
    """Вся история страховок"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    islogIn: bool = True if session.get('islogIn') else False
    wallet: str = session.get('wallet')
    role: int = session.get('role')
    session['lastPage'] = '/list/insurence/'
    session_role: int = session.get('session_role')
    list_insurence: list = []


    if wallet:
        info: dict = User.getUserInfo(wallet)['info']
        response = User.getInsuranceHistory(wallet)
        if response['status']:
            list_insurence = response['insurance_history']

        return render_template('html/list_insurence.html', islogIn=islogIn, lastPage=lastPage, list_insurence=list_insurence, info=info, role=role, session_role=session_role, datetime=dt)


@app.route('/list/rider_licence_dps/')
@isLogin
def getRequestsDL() -> render_template:
    """Список вод.удовст для регистрации в базу ДПС"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    islogIn: bool = True if session.get('islogIn') else False
    wallet: str = session.get('wallet')
    role: int = session.get('role')
    session['lastPage'] = '/list/rider_licence_dps/'
    session_role: int = session.get('session_role')
    list_rider_license_dps: list = []

    if wallet:
        info: dict = User.getUserInfo(wallet)['info']
        response = DPS.getRequestsDL(wallet)
        if response['status']:
            list_rider_license_dps = response['driver_licences']

        return render_template('html/list_rider_license_dps.html', islogIn=islogIn, lastPage=lastPage, list_rider_license_dps=list_rider_license_dps, info=info, role=role, session_role=session_role, datetime=dt)


@app.route('/list/category_dps/')
@isLogin
def getRequestsNewCategory() -> render_template:
    """Список новых категорий ТС вод.удовст для регистрации в базу ДПС"""

    lastPage: str = session.get('lastPage') if session.get('lastPage') else '/'
    islogIn: bool = True if session.get('islogIn') else False
    wallet: str = session.get('wallet')
    role: int = session.get('role')
    session['lastPage'] = '/list/category_dps/'
    session_role: int = session.get('session_role')
    list_category: list = []


    if wallet:
        info: dict = User.getUserInfo(wallet)['info']
        response = DPS.getRequestsNewCategory(wallet)
        if response['status']:
            list_category = response['driver_licences']

        return render_template('html/category_dps.html', islogIn=islogIn, lastPage=lastPage, list_category=list_category, info=info, role=role, session_role=session_role, datetime=dt)
    
    
@app.route('/logout/')
def logout() -> redirect:
    """Выход"""
    
    session.clear()
    return redirect('/')
    
    
if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(host=settings['Flask']['host'], port=settings['Flask']['port'])