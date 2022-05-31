BR_STATES = {
    "AC": "ACRE",
    "AL": "ALAGOAS",
    "AP": "AMAPÁ",
    "AM": "AMAZONAS",
    "BA": "BAHIA",
    "CE": "CEARÁ",
    "DF": "DISTRITO FEDERAL",
    "ES": "ESPÍRITO SANTO",
    "GO": "GOIÁS",
    "MA": "MARANHÃO",
    "MT": "MATO GROSSO",
    "MS": "MATO GROSSO DO SUL",
    "MG": "MINAS GERAIS",
    "PA": "PARÁ",
    "PB": "PARAÍBA",
    "PR": "PARANÁ",
    "PE": "PERNAMBUCO",
    "PI": "PIAUÍ",
    "RJ": "RIO DE JANEIRO",
    "RN": "RIO GRANDE DO NORTE",
    "RS": "RIO GRANDE DO SUL",
    "RO": "RONDÔNIA",
    "RR": "RORAIMA",
    "SC": "SANTA CATARINA",
    "SP": "SÃO PAULO",
    "SE": "SERGIPE",
    "TO": "TOCANTINS",
}


def is_br_state_valid(value):
    return True if value in BR_STATES.keys() else False


def is_state_format_valid(value):
    return False if value in BR_STATES.values() else True
