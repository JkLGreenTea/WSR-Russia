settings: dict = {
    'Flask': {
      'host': '192.168.30.202',
      'port': 3101
    },
    'Contract': {
        'host': '192.168.30.201',
        'port': 8545,
        'main': {
            'address': '0x9c304eda49a4F8EE98894419a74efB4B5BE61c07',
            'abi': [
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "enum structures.categories",
				"name": "category",
				"type": "uint8"
			},
			{
				"internalType": "uint88",
				"name": "marketValue",
				"type": "uint88"
			},
			{
				"internalType": "uint16",
				"name": "useTime",
				"type": "uint16"
			}
		],
		"name": "addCar",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "newFIO",
				"type": "string"
			}
		],
		"name": "changeUserInfo",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "address payable",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "uint128",
				"name": "value",
				"type": "uint128"
			}
		],
		"name": "pay",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "string",
				"name": "FIO",
				"type": "string"
			}
		],
		"name": "registration",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [],
		"name": "sendETH",
		"outputs": [],
		"payable": True,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "carId",
				"type": "uint16"
			},
			{
				"internalType": "bool",
				"name": "newCar",
				"type": "bool"
			},
			{
				"internalType": "string",
				"name": "name",
				"type": "string"
			},
			{
				"internalType": "enum structures.categories",
				"name": "category",
				"type": "uint8"
			},
			{
				"internalType": "uint88",
				"name": "marketValue",
				"type": "uint88"
			},
			{
				"internalType": "uint88",
				"name": "insuranceFee",
				"type": "uint88"
			},
			{
				"internalType": "uint16",
				"name": "useTime",
				"type": "uint16"
			}
		],
		"name": "setCarData",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"components": [
					{
						"internalType": "uint24",
						"name": "number",
						"type": "uint24"
					},
					{
						"internalType": "uint64",
						"name": "validity",
						"type": "uint64"
					},
					{
						"internalType": "bool",
						"name": "categoryA",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "categoryB",
						"type": "bool"
					},
					{
						"internalType": "bool",
						"name": "categoryC",
						"type": "bool"
					}
				],
				"internalType": "struct structures.DL",
				"name": "driverLicense",
				"type": "tuple"
			},
			{
				"internalType": "uint16",
				"name": "experience",
				"type": "uint16"
			},
			{
				"internalType": "bool",
				"name": "DTPCount",
				"type": "bool"
			},
			{
				"internalType": "int8",
				"name": "fines",
				"type": "int8"
			},
			{
				"internalType": "enum structures.roles",
				"name": "role",
				"type": "uint8"
			}
		],
		"name": "setUserData",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address payable",
				"name": "_bank",
				"type": "address"
			},
			{
				"internalType": "address payable",
				"name": "_insuranceCompany",
				"type": "address"
			},
			{
				"internalType": "address payable",
				"name": "_admin",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "DPS",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "driver1",
				"type": "address"
			},
			{
				"internalType": "address",
				"name": "driver2",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint128",
				"name": "value",
				"type": "uint128"
			}
		],
		"name": "withdrawETH",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "admin",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "authorization",
		"outputs": [
			{
				"internalType": "enum structures.roles",
				"name": "",
				"type": "uint8"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "bank",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getBalanceETH",
		"outputs": [
			{
				"internalType": "uint128",
				"name": "",
				"type": "uint128"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			},
			{
				"internalType": "uint16",
				"name": "carId",
				"type": "uint16"
			}
		],
		"name": "getCar",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "enum structures.categories",
						"name": "category",
						"type": "uint8"
					},
					{
						"internalType": "uint88",
						"name": "marketValue",
						"type": "uint88"
					},
					{
						"internalType": "uint88",
						"name": "insuranceFee",
						"type": "uint88"
					},
					{
						"internalType": "uint16",
						"name": "useTime",
						"type": "uint16"
					}
				],
				"internalType": "struct structures.car",
				"name": "",
				"type": "tuple"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "getCars",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"internalType": "string",
						"name": "name",
						"type": "string"
					},
					{
						"internalType": "enum structures.categories",
						"name": "category",
						"type": "uint8"
					},
					{
						"internalType": "uint88",
						"name": "marketValue",
						"type": "uint88"
					},
					{
						"internalType": "uint88",
						"name": "insuranceFee",
						"type": "uint88"
					},
					{
						"internalType": "uint16",
						"name": "useTime",
						"type": "uint16"
					}
				],
				"internalType": "struct structures.car[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getInsuranceDebt",
		"outputs": [
			{
				"internalType": "uint128",
				"name": "",
				"type": "uint128"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "getUserInfo",
		"outputs": [
			{
				"components": [
					{
						"internalType": "string",
						"name": "FIO",
						"type": "string"
					},
					{
						"components": [
							{
								"internalType": "uint24",
								"name": "number",
								"type": "uint24"
							},
							{
								"internalType": "uint64",
								"name": "validity",
								"type": "uint64"
							},
							{
								"internalType": "bool",
								"name": "categoryA",
								"type": "bool"
							},
							{
								"internalType": "bool",
								"name": "categoryB",
								"type": "bool"
							},
							{
								"internalType": "bool",
								"name": "categoryC",
								"type": "bool"
							}
						],
						"internalType": "struct structures.DL",
						"name": "driverLicense",
						"type": "tuple"
					},
					{
						"internalType": "uint16",
						"name": "experience",
						"type": "uint16"
					},
					{
						"internalType": "uint8",
						"name": "DTPCount",
						"type": "uint8"
					},
					{
						"internalType": "uint8",
						"name": "fines",
						"type": "uint8"
					},
					{
						"internalType": "enum structures.roles",
						"name": "role",
						"type": "uint8"
					}
				],
				"internalType": "struct structures.user",
				"name": "",
				"type": "tuple"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "insuranceCompany",
		"outputs": [
			{
				"internalType": "address payable",
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "onlyDPS",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "onlyRegistred",
		"outputs": [
			{
				"internalType": "bool",
				"name": "",
				"type": "bool"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
]
        },
        'insurance': {
            'address': '0x4E2f45eFb2aAb51d35b922F5872910E8bEfb6aB0',
            'abi': [
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint16",
				"name": "carId",
				"type": "uint16"
			}
		],
		"name": "buyInsurance",
		"outputs": [],
		"payable": True,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "contract main",
				"name": "mAddr",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "uint16",
				"name": "carId",
				"type": "uint16"
			}
		],
		"name": "getInsurance",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"internalType": "uint16",
						"name": "carId",
						"type": "uint16"
					},
					{
						"internalType": "uint64",
						"name": "validity",
						"type": "uint64"
					},
					{
						"internalType": "uint88",
						"name": "insuranceFee",
						"type": "uint88"
					}
				],
				"internalType": "struct structures.insurance",
				"name": "",
				"type": "tuple"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getInsuranceHistory",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"internalType": "uint16",
						"name": "carId",
						"type": "uint16"
					},
					{
						"internalType": "uint64",
						"name": "validity",
						"type": "uint64"
					},
					{
						"internalType": "uint88",
						"name": "insuranceFee",
						"type": "uint88"
					}
				],
				"internalType": "struct structures.insurance[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "uint16",
				"name": "carId",
				"type": "uint16"
			}
		],
		"name": "requestInsurance",
		"outputs": [
			{
				"internalType": "uint128",
				"name": "cost",
				"type": "uint128"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
]
        },
        'dps': {
            'address': '0x96CB965387daB998B44Fc5C9Cd509267CF849249',
            'abi': [
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint16",
				"name": "id",
				"type": "uint16"
			}
		],
		"name": "acceptNewCategory",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint16",
				"name": "id",
				"type": "uint16"
			}
		],
		"name": "acceptNewDL",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint16",
				"name": "experience",
				"type": "uint16"
			},
			{
				"internalType": "uint24",
				"name": "number",
				"type": "uint24"
			},
			{
				"internalType": "uint64",
				"name": "validity",
				"type": "uint64"
			},
			{
				"internalType": "bool",
				"name": "catA",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catB",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catC",
				"type": "bool"
			}
		],
		"name": "addDL",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "addDPS",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "bool",
				"name": "catA",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catB",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catC",
				"type": "bool"
			}
		],
		"name": "addNewCategory",
		"outputs": [
			{
				"internalType": "uint16",
				"name": "id",
				"type": "uint16"
			}
		],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "bool",
				"name": "catA",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catB",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catC",
				"type": "bool"
			}
		],
		"name": "addNewDL",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint24",
				"name": "DLNumber",
				"type": "uint24"
			},
			{
				"internalType": "uint16",
				"name": "carId",
				"type": "uint16"
			}
		],
		"name": "confirmDTP",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint24",
				"name": "number",
				"type": "uint24"
			},
			{
				"internalType": "uint64",
				"name": "validity",
				"type": "uint64"
			},
			{
				"internalType": "bool",
				"name": "catA",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catB",
				"type": "bool"
			},
			{
				"internalType": "bool",
				"name": "catC",
				"type": "bool"
			}
		],
		"name": "deleteRequest",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint24",
				"name": "DLNumber",
				"type": "uint24"
			}
		],
		"name": "giveFine",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "uint16",
				"name": "id",
				"type": "uint16"
			}
		],
		"name": "payFine",
		"outputs": [],
		"payable": True,
		"stateMutability": "payable",
		"type": "function"
	},
	{
		"constant": False,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "removeDPS",
		"outputs": [],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "contract main",
				"name": "mContr",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "uint24",
				"name": "number",
				"type": "uint24"
			}
		],
		"name": "DLNumToDriver",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getDTP",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"internalType": "uint16",
						"name": "carId",
						"type": "uint16"
					},
					{
						"internalType": "uint64",
						"name": "time",
						"type": "uint64"
					}
				],
				"internalType": "struct structures.DTP[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [
			{
				"internalType": "address",
				"name": "user",
				"type": "address"
			}
		],
		"name": "getFines",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"internalType": "uint64",
						"name": "time",
						"type": "uint64"
					},
					{
						"internalType": "bool",
						"name": "paid",
						"type": "bool"
					}
				],
				"internalType": "struct structures.fine[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getRequestsDL",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"components": [
							{
								"internalType": "uint24",
								"name": "number",
								"type": "uint24"
							},
							{
								"internalType": "uint64",
								"name": "validity",
								"type": "uint64"
							},
							{
								"internalType": "bool",
								"name": "categoryA",
								"type": "bool"
							},
							{
								"internalType": "bool",
								"name": "categoryB",
								"type": "bool"
							},
							{
								"internalType": "bool",
								"name": "categoryC",
								"type": "bool"
							}
						],
						"internalType": "struct structures.DL",
						"name": "driverLicense",
						"type": "tuple"
					},
					{
						"internalType": "address payable",
						"name": "driver",
						"type": "address"
					},
					{
						"internalType": "bool",
						"name": "completed",
						"type": "bool"
					}
				],
				"internalType": "struct structures.requestDL[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	},
	{
		"constant": True,
		"inputs": [],
		"name": "getRequestsNewCategory",
		"outputs": [
			{
				"components": [
					{
						"internalType": "uint16",
						"name": "id",
						"type": "uint16"
					},
					{
						"internalType": "address",
						"name": "driver",
						"type": "address"
					},
					{
						"components": [
							{
								"internalType": "uint24",
								"name": "number",
								"type": "uint24"
							},
							{
								"internalType": "uint64",
								"name": "validity",
								"type": "uint64"
							},
							{
								"internalType": "bool",
								"name": "categoryA",
								"type": "bool"
							},
							{
								"internalType": "bool",
								"name": "categoryB",
								"type": "bool"
							},
							{
								"internalType": "bool",
								"name": "categoryC",
								"type": "bool"
							}
						],
						"internalType": "struct structures.DL",
						"name": "driverLicense",
						"type": "tuple"
					},
					{
						"internalType": "bool",
						"name": "completed",
						"type": "bool"
					}
				],
				"internalType": "struct structures.requestNewCategory[]",
				"name": "",
				"type": "tuple[]"
			}
		],
		"payable": False,
		"stateMutability": "view",
		"type": "function"
	}
]
        }
    }
}