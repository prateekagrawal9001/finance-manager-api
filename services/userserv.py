from services.currency import convert_currency


def total_balance_calc(trg_currency: str, accounts: list) -> float:
    total_balance = 0.0
    for account in accounts:
        total_balance += convert_currency(account.act_balance, account.account_currency, trg_currency)
    return total_balance