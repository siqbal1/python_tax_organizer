import json
from transaction_summary import TransactionSummary
from transaction_summary import MONTH_NAMES
from category import Category
from category_list import CategoryList
"""
Attributes:

transaction_summaries = list(ts: TransactionSummary)
summary_titles = list(titles: str) list of the titles of the transaction summaries in order
all_monthly_summaries = list(transaction_summary:TransactionSummary)
all_transactions = [trans: TransactionList]
all_categories = set()
all_category_transactions = dict("category" : list(trans:Transaction))
all_category_totals = dict()
total_deposits = float
total_withdrawls = float
total_checks = float

Yearly stuff:
"""

DEPOSITS_KEY = "Deposits"
WITHDRAWLS_KEY = "Withdrawls"
CHECKS_KEY = "Checks"


class YearlySummary:

    def __init__(self):
        # list of the titles for each summary
        self.title = "Yearly Summary"
        self.monthly_summaries = dict()

        self.transaction_type_categories = {
            DEPOSITS_KEY: CategoryList(),
            WITHDRAWLS_KEY: CategoryList(),
            CHECKS_KEY: CategoryList(),
        }

        self.total_deposits = 0.0
        self.total_withdrawls = 0.0
        self.total_checks = 0.0

    def getDepositCategories(self):
        return self.transaction_type_categories[DEPOSITS_KEY].getCategoryNames()

    def addDepositCategory(self, category: Category):
        self.transaction_type_categories[DEPOSITS_KEY].addCategory(category)

    def addWithdrawlCategory(self, category: Category):
        self.transaction_type_categories[WITHDRAWLS_KEY].addCategory(category)

    def addCheckCategory(self, category: Category):
        self.transaction_type_categories[CHECKS_KEY].addCategory(category)

    def addSummary(self, transaction_summary: TransactionSummary):
        self.monthly_summaries[transaction_summary.date] = transaction_summary

        self.total_deposits += transaction_summary.deposits.total
        self.total_withdrawls += transaction_summary.withdrawls.total
        self.total_checks += transaction_summary.checks.total

        self.transaction_type_categories[DEPOSITS_KEY].extend(
            transaction_summary.deposits.category_list)
        self.transaction_type_categories[WITHDRAWLS_KEY].extend(
            transaction_summary.withdrawls.category_list)
        self.transaction_type_categories[CHECKS_KEY].extend(
            transaction_summary.checks.category_list)

    def getAllTransactions(self):
        transactions = []

        for month in self.monthly_summaries:
            transactions.extend(self.monthly_summaries[month].transactions)

        return transactions

    def __len__(self):

        length = 0

        for month in self.monthly_summaries:
            length += self.monthly_summaries[month].transactions

    def getMonthSummary(self, month):
        if month in self.monthly_summaries:
            return self.monthly_summaries[month]

        if month in MONTH_NAMES:
            return self.monthly_summaries[MONTH_NAMES[month]]

        return None

    def getMonthDepositCategories(self, month) -> CategoryList:
        month_summary = self.getMonthSummary(month)

        if month_summary:
            return month_summary.deposits.category_list

        return None

    def getMonthWithdrawlCategories(self, month) -> CategoryList:
        month_summary = self.getMonthSummary(month)

        if month_summary:
            return month_summary.withdrawls.category_list

        return None

    def getMonthCheckCategories(self, month) -> CategoryList:
        month_summary = self.getMonthSummary(month)

        if month_summary:
            return month_summary.checks.category_list

        return None

    def getYear(self):
        if self.monthly_summaries:
            return self.getMonthSummary(1).getYear()

    def __str__(self):
        str_rep = ""

        # for month in self.monthly_summaries:
        #     str_rep += str(self.monthly_summaries[month]) + "\n"

        for trans_type in self.transaction_type_categories:
            str_rep += f"{trans_type} \n"
            str_rep += str(self.transaction_type_categories[trans_type]) + "\n"

        str_rep += f"Total deposits: {self.total_deposits}\n"
        str_rep += f"Total withdrawls: {self.total_withdrawls}\n"
        str_rep += f"Total checks: {self.total_checks}\n"

        return str_rep

    def printSummaries(self):
        for month_name in self.monthly_summaries:
            print(self.monthly_summaries[month_name])


    def categoriesToSheetsJSON(self):
        sheets_list = []
        row_num = 0
        col_num = 0

        for trans_type in self.transaction_type_categories:
            sheet_json = {
                "properties": {
                    "title": f"{trans_type} Categories",
                },
                "data": self.transaction_type_categories[trans_type].toDataJSON(row_num, col_num),
            }

            sheets_list.append(sheet_json)

        return sheets_list

    def toSpreadsheetJSON(self):
        """
        Makes a spreadsheet in json for google sheets api
        return SpreadsheetJSON
        """
        sheets_json = []

        # create sheets for each categories for deposits, withdrawls, and checks
        sheets_json.extend(self.categoriesToSheetsJSON())

        for trans_summary in self.monthly_summaries:
            sheets_json.extend(self.monthly_summaries[trans_summary].toSheetJSON())

        json = {
            "properties": {
                "title": f"{self.title} {self.getYear()}",
            },
            "sheets": sheets_json,
        }

        return json
