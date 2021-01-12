from transaction import Transaction
from category import Category
from category_list import CategoryList

COL_SPACER = 5

class TransactionList:
    def __init__(self):
        self.total = 0.0
        self.transactions = []
        # category_list correspond to category objects
        self.category_list = CategoryList()

    def addKeyWordsToCategory(self, key_words: set, category_name: str):
        self.category_list.addKeyWords(category_name, key_words)

    def addCategory(self, category_name: str, key_words: set):
        self.category_list.addCategory(Category(category_name, key_words))

    def addTransaction(self, transaction: Transaction):
        """
        Adds transaction to list and updates corresponding sums
        """
        self.category_list.addTransaction(transaction)
        self.total += abs(transaction.amount)
        self.transactions.append(transaction)

    def extend(self, trans_list):
        self.total += trans_list.total
        self.transactions.extend(trans_list.transactions)
        self.category_list.extend(trans_list.category_list)

    def __str__(self):
        str_rep = f"Total: {self.total}\n"
        # str_rep += '\n'.join([str(trans) for trans in self.transactions]) + '\n'
        str_rep += str(self.category_list)
        str_rep += str(self.category_list.getSummary())

        return str_rep

    def totalToDataJSON(self):
        total_row_data = {
            "values": [
                {
                    "userEnteredValue": {
                        "stringValue": "",
                    },
                },
                {
                    "userEnteredValue": {
                        "stringValue": "TOTAL:",
                    },
                },
                {
                    "userEnteredValue": {
                        "numberValue": self.total,
                    },
                },
            ]
        }

        return total_row_data

    def toDataJSON(self):
        """
        return list of json row data used for sheets api
        """
        row_num = 0
        col_num = 0
        data_list = []

        row_data = [trans.toRowDataJSON() for trans in self.transactions]
        row_data.append(self.totalToDataJSON())

        data_json = {
            "startRow": row_num,
            "startColumn": col_num,
            "rowData": row_data
        }

        data_list.append(data_json)
        data_list.extend(self.category_list.toDataJSON(row_num, col_num + COL_SPACER))

        return data_list
