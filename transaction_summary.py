from transaction import Transaction
from transaction_list import TransactionList

MONTH_NAMES = {
    1: "JANUARY",
    2: "FEBRUARY",
    3: "MARCH",
    4: "APRIL",
    5: "MAY",
    6: "JUNE",
    7: "JULY",
    8: "AUGUST",
    9: "SEPTEMBER",
    10: "OCTOBER",
    11: "NOVEMBER",
    12: "DECEMBER",
}


class TransactionSummary:
    def __init__(self):
        self.date = ""
        self.deposits = TransactionList()
        self.withdrawls = TransactionList()
        self.checks = TransactionList()

    def __str__(self):
        str_rep = f"{self.date}\n"
        str_rep += "Deposits:\n"
        str_rep += str(self.deposits) + "\n"
        str_rep += "\nWithdrawls:\n"
        str_rep += str(self.withdrawls) + "\n"
        str_rep += "\Checks:\n"
        str_rep += str(self.checks) + "\n"

        return str_rep

    def getYear(self):
        if self.deposits.transactions:
            date_dict = self.deposits.transactions[0].parseDate()
            return date_dict["year"]

        return None

    def setDepositCategoryList(self, category_list):
        self.deposits.category_list = category_list

    def setChecksCategoryList(self, category_list):
        self.checks.category_list = category_list

    def setWithdrawlsCategoryList(self, category_list):
        self.withdrawls.category_list = category_list

    def addCheckCategory(self, category_name: str, key_words: set):
        self.checks.addCategory(category_name, key_words)

    def addDepositCategory(self, category_name: str, key_words: set):
        self.deposits.addCategory(category_name, key_words)

    def addWithdrawlCategory(self, category_name: str, key_words: set):
        self.withdrawls.addCategory(category_name, key_words)

    def addKeyWordsToCheckCategory(self, key_words: set, category_name: str):
        self.checks.addKeyWordsToCategory(key_words, category_name)

    def addKeyWordsToDepositCategory(self, key_words: set, category_name: str):
        self.deposits.addKeyWordsToCategory(key_words, category_name)

    def addKeyWordsToWithdrawlCategory(self, key_words: set, category_name: str):
        self.withdrawls.addKeyWordsToCategory(key_words, category_name)

    def addChecks(self, transactions: list):
        for transaction in transactions:
            self.addCheck(transaction)

    def addDeposits(self, transactions: list):
        for transaction in transactions:
            self.addDeposit(transaction)

    def addWithdrawls(self, transactions: list):
        for transaction in transactions:
            self.addWithdrawl(transaction)

    def addCheck(self, transaction: Transaction):
        if not self.date:
            self.setDateFromTransaction(transaction)

        self.checks.addTransaction(transaction)

    def addDeposit(self, transaction: Transaction):
        if not self.date:
            self.setDateFromTransaction(transaction)

        self.deposits.addTransaction(transaction)

    def addWithdrawl(self, transaction: Transaction):
        if not self.date:
            self.setDateFromTransaction(transaction)

        self.withdrawls.addTransaction(transaction)

    def setDateFromTransaction(self, transaction: Transaction):
        parsed_date = transaction.parseDate()
        self.date = f'{MONTH_NAMES[parsed_date["month"]]}'

    def toSheetJSON(self):
        """
        return [sheet_jsons] used for sheets api
        """
        # create Sheet json object
        sheet_list = []

        sheet_json = {
            "properties": {
                "title": f"{self.date} Deposits",
            },
            "data": [self.deposits.toDataJSON()],
        }
        sheet_list.append(sheet_json)

        sheet_json = {
            "properties": {
                "title": f"{self.date} Withdrawls",
            },
            "data": [self.withdrawls.toDataJSON()],
        }
        sheet_list.append(sheet_json)

        sheet_json = {
            "properties": {
                "title": f"{self.date} Checks",
            },
            "data": [self.checks.toDataJSON()],
        }
        sheet_list.append(sheet_json)

        return sheet_list
