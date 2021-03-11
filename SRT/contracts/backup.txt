pragma solidity ^0.5.12;
pragma experimental ABIEncoderV2;

/*
Это проект "Безопасное дорожное движение" на платформе блокчейн. Смарт-контракты написаны на языке Solidity.
Этот проект обеспечивает контроль за страховками и водительскими правами.
В проекте есть следующий функционал:
Регистрация пользователей в системе. Авторизация пользователей. Получение личной информации о пользователе.
Возможность просмотреть все свои авто. Возможность добавить новое авто в систему.
Возможность изменить свои личные данные. Возможность для банка и страховой внести средства на контракт.
Возможность снять средства с контракта для страховой и банка. Возможность просматреть баланс средств на
контракте для банка и страховой. Возможность узнать долг страховой компании.
Возможность просмотреть историю всех своих страховок.
Функция просмотра страховки конкретной личной машины.
Функция запроса стоимости оформления страховки на машину.
Функция оформления или продления страховки на авто.
Функция просмотра всех своих штрафов. Функция выдачи штрафов (ДПС).
Функция для поиска адреса кошелька по номеру водительских прав.
Функция подтверждения ДТП (для ДПС). После подтверждения выплачивается страховка.
Возможность просмотра всех своих ДТП, с указанием авто и времени.
Возможность добавления действующих прав или продление внесенных прав в системе.
Возможность отправки заявки на оформление новых прав, если таковых не было.
Функция подтверждения заявки на оформление новых прав. Функция просмотра всех заявок на новые права.


*/

library structures {    // Библиотека со структурами
    enum roles {    // Роли в системе
        guest,      //Гость
        driver,     // водитель
        DPS,        // сотрудник ДПС
        admin,      //Админ
        bank,       //Банк
        insuranceCompany    // страховая компания
    }
    
    enum categories {       // категории авто
        A,
        B,
        C
    }
    
    struct DL {     // DL - driver license Водительские права. Категории могут быть все сразу
        uint24 number;      // номер прав
        uint64 validity;    // срок действия (до какого)
        // Категории прав:
        bool categoryA;
        bool categoryB;
        bool categoryC;
    }
    
    struct user {       // структура данных пользователя
        string FIO;     // ФИО пользователя
        DL driverLicense;   // Водительские права
        uint16 experience;  // Стаж (год начала водительского стажа)
        uint8 DTPCount;     // Количество ДТП у водителя
        uint8 fines;    // неоплаченные штрафы
        roles role;     // роль
    }
    
    struct car {        //структура данных авто
        uint16 id;      // индекс в массиве
        string name;        // Марка и модель авто
        categories category;    // категория
        uint88 marketValue;     // рыночная стоимость
        uint88 insuranceFee;    // страховой взнос
        uint16 useTime;     // время эксплуатации (в годах)
        
    }
    
    struct fine {       // структура штрафа
        uint16 id;      //индекс штрафа
        uint64 time;        //время получения
        bool paid;      // статус штрафа, оплачен или нет
    }
    
    struct DTP {        //структура данных о ДТП
        uint16 id;      // индекс в массиве
        uint16 carId;   // индекс авто в массиве авто
        uint64 time;        // время проишествия
    }
    
    struct insurance {      // структура страховки
        uint16 id;      // индекс
        uint16 carId;       // индекс авто
        uint64 validity;        //срок действия (до какого, в unix)
        uint88 insuranceFee;    // страховой взнос
    }
    
    struct requestDL {      // структура запроса на новые водительские права
        uint16 id;      // индекс
        DL driverLicense;       // данные водительских прав
        address payable driver;     // адрес водителя
        bool completed;     // статус готовности
    }
    
    struct requestNewCategory {     // структура запросов на добавление новой категории
        uint16 id;      // индекс
        address driver;     //адрес водителя
        DL driverLicense;       // данные прав
        bool completed;     // статус выполнения
    }
    
}

// главный контракт. Содержит в себе данные о пользователях и их авто.

contract main {
    address payable public bank;        // адрес банка
    address payable public insuranceCompany;        //адрес страховой
    address payable public admin;       // адрес админа
    
    uint128 private bankBalance;    // баланс банка на контракте
    uint128 private insuranceCompanyBalance;        //баланс компании на балансе
    uint128 private insuranceCompanyDebt;       // долг страховой компании
    
    mapping (address => structures.user) users;     // маппинг с данными пользователя
    mapping (address => structures.car[]) userCars;     // маппинг машин пользователя
    
    constructor (address payable _bank, address payable _insuranceCompany, address payable _admin, address DPS, address driver1, address driver2) public {
        bank = _bank;
        insuranceCompany = _insuranceCompany;
        admin = _admin;
        users[_bank] = structures.user("BANK", structures.DL(0,0,false,false,false), 0,0,0, structures.roles.bank);     // создаем аккаунты для банка, компании, админа.
        users[_insuranceCompany] = structures.user("InsuranceCo", structures.DL(0,0,false,false,false), 0,0,0, structures.roles.insuranceCompany);
        users[_admin] = structures.user("Admin", structures.DL(1488,0,true,true,true), 20,0,0, structures.roles.admin);
        users[DPS] = structures.user("Иванов Иван Иванович", structures.DL(0, 0, false, false, false), 2, 0, 0, structures.roles.DPS);
        users[driver1] = structures.user("Сенов Семен Семенович", structures.DL(0,0,false,false,false), 5, 0, 0, structures.roles.driver);
        users[driver2] = structures.user("Петров Петр Петрович", structures.DL(0,0,false,false,false), 10, 3, 0, structures.roles.driver);
        // добавить ДПС и 2х водителей...
    }
    
    function onlyDPS (address user) public view returns (bool) {    // функция проверки на права ДПС
        require (users[user].role == structures.roles.DPS, 'Вы не сотрудник ДПС');
        return true;
    }
    function onlyRegistred (address user) public view returns (bool) {      // функция проверки на наличие регистрации
        require (users[user].role != structures.roles.guest, 'Вы не зарегистрированны');
        return true;
    }
    
    function sendETH () public payable {        // функция для внесения эфира на контракт (для компании и банка)
        require (msg.sender == bank || msg.sender == insuranceCompany, 'Эта функция вам не доступна');
        if (msg.sender == bank) bankBalance += uint128(msg.value);
        else if (msg.sender == insuranceCompany) {
            if (insuranceCompanyDebt != 0 && msg.value <= insuranceCompanyDebt) insuranceCompanyDebt -= uint128(msg.value);
            else if (insuranceCompanyDebt !=0 && msg.value > insuranceCompanyDebt) {
                uint128 value = uint128(msg.value) - insuranceCompanyDebt;
                insuranceCompanyDebt = 0;
                insuranceCompanyBalance += value;
            }
            else insuranceCompanyBalance += uint128(msg.value);
        }
    }
    
    function withdrawETH (uint128 value) public {       // функция снятия эфира с контракта (для компании и банка)
        require (msg.sender == bank || msg.sender == insuranceCompany, 'Эта функция вам не доступна');
        require (value <= address(this).balance, 'На контракте недостаточно средств');
        if (msg.sender == bank) {
            require (value <= bankBalance, 'У вас недостаточно средств для списания');
            bankBalance -= value;
            msg.sender.transfer(value);
        }
        else {
            require (value <= insuranceCompanyBalance, 'У вас недостаточно средств для списания');
            insuranceCompanyBalance -= value;
            msg.sender.transfer(value);
        }
    }
    
    function getBalanceETH () public view returns (uint128) {       //просмотреть баланс на контракте
        require (msg.sender == bank || msg.sender == insuranceCompany, 'Вы не можете просматреть эту функцию');
        if (msg.sender == bank) return bankBalance;
        else return insuranceCompanyBalance;
    }
    
    function getInsuranceDebt () public view returns (uint128) {        //узнать долг компании
        require (msg.sender == insuranceCompany, 'Вы не страховая компания');
        return insuranceCompanyDebt;
    }
    
    function registration (string memory FIO) public {      //функция регистрации
        require (users[msg.sender].role == structures.roles.guest, 'Вы уже зарегистрированны');
        require (bytes(FIO).length > 0, 'Поле ФИО не может быть пустым');
        users[msg.sender] = structures.user(
            FIO,
            structures.DL(0, 0, false, false, false),
            0,
            0,
            0,
            structures.roles.driver
        );
    }
    
    function authorization () public view returns (structures.roles) {      // функция Авторизация
        require (onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        return users[msg.sender].role;
    }
    
    function getUserInfo (address user) public view returns (structures.user memory) {  //функция просмотра данных пользователя
        return users[user];
    }
    
    function getCars (address user) public view returns (structures.car[] memory) {     // Просмотр всех авто пользователя
        require (userCars[user].length != 0, 'У вас нет машин');
        return userCars[user];
    }
    
    function getCar (address user, uint16 carId) public view returns (structures.car memory) {  // найти конкретную машину пользователя
        require (userCars[user].length > carId, 'Неверный id авто');
        return userCars[user][carId];
    }
    
    function addCar (string memory name, structures.categories category, uint88 marketValue, uint16 useTime) public {       //функция добавления нового авто, выполняетя автоматически
        require (onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        require (bytes(name).length != 0, 'Поле марки машины не может быть пустым');
        if (category == structures.categories.A) require (users[msg.sender].driverLicense.categoryA, 'Вы не имеете категорию A');
        else if (category == structures.categories.B) require (users[msg.sender].driverLicense.categoryB, 'Вы не имеете категорию B');
        else require (users[msg.sender].driverLicense.categoryC, 'Вы не имеете категорию C');
        userCars[msg.sender].push(structures.car(
            uint16(userCars[msg.sender].length),
            name,
            category,
            marketValue,
            0,
            useTime
        ));
    }
    
    function changeUserInfo (string memory newFIO) public {     // изменить данные о пользователе
        require (bytes(newFIO).length != 0, 'ФИО не может быть пустым');
        require (keccak256(bytes(users[msg.sender].FIO)) != keccak256(bytes(newFIO)), 'Ваше старое ФИО одинаково с новым');
        users[msg.sender].FIO = newFIO;
    }
    
    function setUserData (address user, structures.DL memory driverLicense, uint16 experience, bool DTPCount, int8 fines, structures.roles role) public {       // заменить данные пользователя
        // require ()   // проверка на отправителя. Это должны быть наши контракты
        if (driverLicense.number != 0) users[user].driverLicense = driverLicense;
        if (experience != 0) users[user].experience = experience;
        if (DTPCount == true) users[user].DTPCount++;
        if (fines == -1) users[user].fines--;
        else if (fines == 1) users[user].fines++;
        else if (fines > 1 || fines < -1) require(fines > -1 || fines < 1, 'Неверное число');
        if (role != structures.roles.guest) users[user].role = role;
    }
    
    function setCarData (address user, uint16 carId, bool newCar, string memory name, structures.categories category, uint88 marketValue, uint88 insuranceFee, uint16 useTime) public {     // изменить данные авто
        // require ()   // проверка на отправителя. Это должны быть наши контракты
        if (newCar == true) {
            require (bytes(name).length != 0, 'Поле марки машины не может быть пустым');
            require (users[msg.sender].fines == 0, 'У вас есть неоплаченные штрафы');
            require (marketValue != 0, 'Рыночная стоимость не может равной нулю');
            userCars[user].push(structures.car(
                uint16(userCars[msg.sender].length),
                name,
                category,
                marketValue,
                0,
                useTime
            ));
        }
        else if (newCar == false) {
            userCars[user][carId].insuranceFee = insuranceFee;
        }
    }
    
    function pay (address payable user, uint128 value) public { // функция оплаты 
        // require ()   // проверка на отправителя. Это должны быть наши контракты
        require (address(this).balance >= value, 'На контракте недостаточно средств');
        if (insuranceCompanyBalance < value) {
            uint128 debt = value - insuranceCompanyBalance;
            bankBalance -= debt;
            insuranceCompanyBalance = 0;
            insuranceCompanyDebt += debt;
            user.transfer(value);
        }
        else {
            insuranceCompanyBalance -= value;
            user.transfer(value);
        }
    }
    
}

contract Insurance {            //контракт с функциями страховки
    main mainContract;
    
    mapping (address => structures.insurance[]) userInsurances;     // список страховок пользователя
    
    constructor (main mAddr) public {
        mainContract = mAddr;
    }
    
    function getInsuranceHistory () public view returns (structures.insurance[] memory) {       //просмотреть историю всех страховок пользователя
        require (mainContract.onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        require (userInsurances[msg.sender].length != 0, 'У вас не было страховок');
        return userInsurances[msg.sender];
    }
    
    function getInsurance (uint16 carId) public view returns (structures.insurance memory) {    // просмотреть страховку конкретной машины
        require (mainContract.onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        // structures.car[] memory cars = mainContract.getCars(msg.sender
        
        uint16 length = uint16(mainContract.getCars(msg.sender).length);
        require (length > carId, 'Неверный id авто');
        structures.car memory car = mainContract.getCar(msg.sender, carId);
        require (car.insuranceFee != 0, 'Это авто не застраховано');
        uint16 trueId;
        for (uint16 i = 0; i < userInsurances[msg.sender].length; i++) {
            if (userInsurances[msg.sender][i].carId == carId) {
                trueId = i;
                break;
            }
        }
        return userInsurances[msg.sender][trueId];
    }
    
    function requestInsurance (uint16 carId) public view returns (uint128 cost) {   // узнать стоимость страховки на данное авто
        require (mainContract.onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        uint88 eth = 1000000000000000000;
        structures.user memory usr = mainContract.getUserInfo(msg.sender);
        structures.car memory car = mainContract.getCar(msg.sender, carId);
        if (car.useTime > 10) {
            uint val1 = (car.marketValue) / (10*eth) * ( (car.useTime*eth / 10) - (1*eth) ) + ( (usr.fines * eth) / 5 ) + usr.DTPCount;
            uint val2 = (usr.experience*eth) / 5;
            if (val1 <= val2) cost = car.marketValue / 100;      // 1% от рыночной стоимости
            else cost = uint128(val1 - val2);
        }
        else {
            uint val1 = (car.marketValue) / (10*eth) * ( (1*eth) - (car.useTime*eth / 10) ) + ( (usr.fines * eth) / 5 ) + usr.DTPCount;
            uint val2 = (usr.experience*eth) / 5;
            if (val1 <= val2) cost = car.marketValue / 100;      // 1% от рыночной стоимости
            else cost = uint128(val1 - val2);
        }
        return cost;
    }
    /* 
    Поскольку формула может выдать значение менее нуля или ноль, страховка становится фиксированной и равна 1% от рыночной стоимости
    */
    
    function buyInsurance (uint16 carId) public payable {   // купить или продлить страховку
        require (mainContract.onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        uint88 eth = 1000000000000000000;
        structures.user memory user = mainContract.getUserInfo(msg.sender);
        structures.car memory car = mainContract.getCar(msg.sender, carId);
        uint128 insuranceFee;
        if (car.useTime > 10) {
            uint val1 = (car.marketValue) / (10*eth) * ( (car.useTime*eth / 10) - (1*eth) ) + ( (user.fines * eth) / 5 ) + user.DTPCount;
            uint val2 = (user.experience*eth) / 5;
            if (val1 <= val2) insuranceFee = car.marketValue / 100;
            else insuranceFee = uint128(val1 - val2);
        }
        else {
            uint val1 = (car.marketValue) / (10*eth) * ( (1*eth) - (car.useTime*eth / 10) ) + ( (user.fines * eth) / 5 ) + user.DTPCount;
            uint val2 = (user.experience*eth) / 5;
            if (val1 <= val2) insuranceFee = car.marketValue / 100;
            else insuranceFee = uint128(val1 - val2);
        }
        
        require (msg.value == insuranceFee, 'Неверная сумма за страховку');
        
        if (car.insuranceFee == 0) {
            userInsurances[msg.sender].push(structures.insurance(
                uint16(userInsurances[msg.sender].length),
                carId,
                uint64(block.timestamp + (10 * 1855)),
                uint88(insuranceFee)
            ));
            mainContract.setCarData(msg.sender, carId, false, "", structures.categories.B, 0, uint88(insuranceFee), 0);
        }
        else {
            uint16 insId;
            for (uint16 i = 0; i < userInsurances[msg.sender].length; i++) {
                if (userInsurances[msg.sender][i].carId == carId) insId = i;
            }
            require ((userInsurances[msg.sender][insId].validity - 150) <= uint64(block.timestamp), 'Срок вашей страховки в норме');
            userInsurances[msg.sender].push(structures.insurance(
                uint16(userInsurances[msg.sender].length),
                carId,
                uint64(block.timestamp + (10 * 1855)),
                uint88(insuranceFee)
            ));
            mainContract.setCarData(msg.sender, carId, false, "", structures.categories.B, 0, uint88(insuranceFee), 0);
        }
        mainContract.insuranceCompany().transfer(msg.value);
    }
}

contract DPS {      //контракт с функциями ДПС
    main mainContract;
    
    structures.requestDL[] DLRequests;      // хранилище запросов на новые права
    structures.DL[] DLBase;     // база данных с правами
    structures.requestNewCategory[] newCategoryRequests;        // ххранилище запросов на добавление новой категории
    
    mapping (address => structures.fine[]) userFines;       //штрафы пользователя
    mapping (address => structures.DTP[]) userDTP;      //ДТП пользователя
    mapping (uint24 => address payable) DLNumberToDriver;       // поиск пользователя (адрес) по его вод.правам
    
    constructor (main mContr) public {
        mainContract = mContr;
        DLNumberToDriver[mainContract.getUserInfo(mainContract.admin()).driverLicense.number] = mainContract.admin();
        // uint64 start = uint64(block.timestamp);
        // не получилось добавить готовые права, т к это требует много газа за раз
        // DLBase.push(structures.DL( 0, start + 0, true, false, false ));
        // DLBase.push(structures.DL( 111, start + 0, false, true, false ));
        // DLBase.push(structures.DL( 222, start + 0, false, false, true ));
        // DLBase.push(structures.DL( 333, start + 0, true, false, false ));
        // DLBase.push(structures.DL( 444, start + 0, false, true, false ));
        // DLBase.push(structures.DL( 555, start + 0, false, false, true ));
        // DLBase.push(structures.DL( 666, start + 0, true, false, false ));
    }
    
    function giveFine (uint24 DLNumber) public {
        require (mainContract.onlyDPS(msg.sender), 'Вы не сотрудник ДПС');
            userFines[DLNumToDriver(DLNumber)].push(structures.fine(
                uint16(userFines[msg.sender].length),
                uint64(block.timestamp),
                false
            ));
        mainContract.setUserData(msg.sender, structures.DL(0, 0, false, false, false), 0, false, 1, structures.roles.guest);
    }    // выдать штраф
    
    function DLNumToDriver (uint24 number) public view returns (address) {
        return DLNumberToDriver[number];
    }  // узнать адрес водителя по его водительским правам
    
    function getFines (address user) public view returns (structures.fine[] memory) {
        require (userFines[user].length != 0, 'У вас не было штрафов');
        return userFines[user];
    }   // получить все штрафы пользователя
    
    function confirmDTP (uint24 DLNumber, uint16 carId) public {
        require (mainContract.onlyDPS(msg.sender), 'Вы не сотрудник ДПС');
        userDTP[DLNumberToDriver[DLNumber]].push(structures.DTP(
            uint16(userDTP[DLNumberToDriver[DLNumber]].length),
            carId,
            uint64(block.timestamp)
        ));
        mainContract.setUserData(DLNumberToDriver[DLNumber], structures.DL(0, 0, false, false, false), 0, true, 0, structures.roles.guest);
        uint128 ins = mainContract.getCar(DLNumberToDriver[DLNumber], carId).insuranceFee * 10;
        mainContract.pay(DLNumberToDriver[DLNumber], ins);
    }        // подтвердить случий ДТП
    
    function getDTP () public view returns (structures.DTP[] memory) {
        require (userDTP[msg.sender].length != 0, 'У вас не было ДТП');
        return userDTP[msg.sender];
    }      // получить все ДТП пользователя
    
    function addDL (uint16 experience, uint24 number, uint64 validity, bool catA, bool catB, bool catC) public {    //Функция добавления действующих прав или продления прав
        require (mainContract.onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        if (mainContract.getUserInfo(msg.sender).driverLicense.validity != 0) {
            require ((mainContract.getUserInfo(msg.sender).driverLicense.validity - 150) <= uint64(block.timestamp), 'Срок ваших прав в норме');
            structures.DL memory dl = mainContract.getUserInfo(msg.sender).driverLicense;
            dl.validity = uint64(block.timestamp + 18250);
            mainContract.setUserData(msg.sender, dl, 0, false, 0, structures.roles.guest);
            uint16 needId;
            for (uint16 i = 0; i < DLBase.length; i++) {
                if (DLBase[i].number == number) {
                    needId = i;
                    break;
                }
                
            }
            DLBase[needId].validity = mainContract.getUserInfo(msg.sender).driverLicense.validity;
        }
        else {
            require (experience != 0, 'Неверная дата начала опыта вождения');
            require (DLNumberToDriver[number] == 0x0000000000000000000000000000000000000000, 'Это водительское удостоверение уже зарегистрированно');
            require (validity != 0, 'Неверная дата окончания прав');
            for (uint i = 0; i < DLBase.length; i++) {
                if (DLBase[i].number == number) break;
                // require(false == true, 'Данных прав нет в системе');
            }
            mainContract.setUserData(msg.sender, structures.DL(number, validity, catA, catB, catC), experience, false, 0, structures.roles.guest);
            DLNumberToDriver[number] = msg.sender;
        }
        
    }
    
    function addNewDL (bool catA, bool catB, bool catC) public {    // функция добавления новых прав
        require (mainContract.onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        require (mainContract.getUserInfo(msg.sender).driverLicense.validity == 0, 'У вас уже есть права');
        for (uint16 i = 0; i < DLRequests.length; i++) {
            require(DLRequests[i].driver != msg.sender, 'Вы уже оставляли заявку, ожидайте');
        }
        DLRequests.push(structures.requestDL(
            uint16(DLRequests.length),
            structures.DL(0, 0, catA, catB, catC),
            msg.sender,
            false
        ));
    }
    
    function acceptNewDL (uint16 id) public {   // функция подтверждения новых прав
        require (mainContract.onlyDPS(msg.sender), 'Вы не сотрудник ДПС');
        require (id < DLRequests.length, 'Неверный id запроса');
        
        structures.DL memory dl = DLRequests[id].driverLicense;
        
        dl.number = uint24(block.timestamp) / 10;
        dl.validity = uint64(block.timestamp + 18250);
        DLBase.push(dl);
        mainContract.setUserData(DLRequests[id].driver, dl, 2020, false, 0, structures.roles.guest);
        DLNumberToDriver[dl.number] = DLRequests[id].driver;
        DLRequests[id].completed = true;
        // deleteRequest(id, true);
        // for (uint16 i = id; i <= DLRequests.length-1; i++) {
        //     DLRequests[i] = DLRequests[i+1];
        // }
        // DLRequests.length--;
    }
    
    // функция удаления запроса
    function deleteRequest (uint24 number, uint64 validity, bool catA, bool catB, bool catC) public {       // reqType - тип массива запросов. Запросы на новые вод.права или на новую категорию    true - DLRequests uint16 id, bool reqType
        DLBase.push(structures.DL(
            number,
            validity,
            catA,
            catB,
            catC
        ));
        // if (reqType == true) {
        //     // require (DLRequests[id].completed, 'Нельзя удалить незавершенную заявку');
        //     for (uint16 i = id; i <= DLRequests.length-1; i++) {
        //         DLRequests[i] = DLRequests[i+1];
        //     }
        //     DLRequests.length--;
        // }
        // else {
        //     for (uint16 i = id; i <= newCategoryRequests.length-1; i++) {
        //         newCategoryRequests[i] = newCategoryRequests[i+1];
        //     }
        //     newCategoryRequests.length--;
        // }
    } 
    
    function getRequestsDL () public view returns (structures.requestDL[] memory) {     // функция получения запросов на новые права
        return DLRequests;
    }
    
    function addNewCategory (bool catA, bool catB, bool catC) public returns (uint16 id) {      // функция добавления новой категории
        require (mainContract.getUserInfo(msg.sender).driverLicense.categoryA != catA, 'У вас уже есть категория A');
        require (mainContract.getUserInfo(msg.sender).driverLicense.categoryB != catB, 'У вас уже есть категория B');
        require (mainContract.getUserInfo(msg.sender).driverLicense.categoryC != catC, 'У вас уже есть категория C');
        require (catA || catB || catC, 'Вы не можете отправить пустую заявку');
        structures.DL memory dl = mainContract.getUserInfo(msg.sender).driverLicense;
        if (catA == true) {
            dl.categoryA = true;
        }
        if (catB == true) {
            dl.categoryB = true;
        }
        if (catC == true) {
            dl.categoryC = true;
        }
        newCategoryRequests.push(structures.requestNewCategory(
           uint16(newCategoryRequests.length),
           msg.sender,
           dl,
           false
        ));
        return uint16(newCategoryRequests.length-1);
    }
    
    function acceptNewCategory (uint16 id) public {     // функция подтверждения добавления новой категории
        require (mainContract.onlyDPS(msg.sender), 'Вы не сотрудник ДПС');
        require (id < newCategoryRequests.length, 'Неверный id запроса');
        mainContract.setUserData(newCategoryRequests[id].driver, newCategoryRequests[id].driverLicense, 0, false, 0, structures.roles.guest);
        newCategoryRequests[id].completed = true;
        // deleteRequest(id, false);
        // for (uint16 i = id; i <= newCategoryRequests.length-1; i++) {
        //     newCategoryRequests[i] = newCategoryRequests[i+1];
        // }
        // newCategoryRequests.length--;
    }
    
    function getRequestsNewCategory () public view returns (structures.requestNewCategory[] memory) {   // узнать запросы на новые категории
        return newCategoryRequests;
    }
    
    function payFine (uint16 id) public payable {       // оплатить штраф
        require (mainContract.onlyRegistred(msg.sender), 'Вы не зарегистрированны');
        require (msg.value == 10 ether, 'Неверная сумма штрафа');
        require (userFines[msg.sender][id].paid == false, 'Штраф уже оплачен');
        mainContract.bank().transfer(msg.value);
        userFines[msg.sender][id].paid = true;
        mainContract.setUserData(msg.sender, structures.DL(0, 0, false, false, false), 0, false, -1, structures.roles.guest);
    }
    
    function addDPS (address user) public {     // добавить сотрудника ДПС
        require (msg.sender == mainContract.admin(), 'Вы не админ');
        require (mainContract.getUserInfo(user).role != structures.roles.DPS, 'Этот пользователь уже сотрудник ДПС');
        mainContract.setUserData(user, structures.DL(0, 0, false, false, false), 0, false, 0, structures.roles.DPS);
    }
    
    function removeDPS (address user) public {      // удалить сотрудника ДПС
        require (msg.sender == mainContract.admin(), 'Вы не админ');
        require (mainContract.getUserInfo(msg.sender).role == structures.roles.DPS, 'Этот пользователь не сотрудник ДПС');
        mainContract.setUserData(user, structures.DL(0, 0, false, false, false), 0, false, 0, structures.roles.driver);
    }
}