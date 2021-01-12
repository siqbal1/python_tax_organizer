from transaction import Transaction
import copy

BLANK_FILLER = ""


class Category:

    def __init__(self, category_name: str, key_words: set = set()):
        self.name = category_name
        self.key_words = key_words
        self.transactions = []
        self.total = 0.0

    def copy(self):
        return copy.deepcopy(self)

    def __str__(self):
        str_rep = f"Category: {self.name}\n"
        str_rep += f"Total: {self.total}\n"
        str_rep += '\n'.join([str(trans) for trans in self.transactions]) + "\n"
        return str_rep

    def __len__(self):
        return len(self.transactions)

    def includesTransaction(self, transaction: Transaction):
        for key_word in self.key_words:
            if key_word.lower() in transaction.description.lower():
                return True

        return False

    def addTransaction(self, transaction: Transaction):
        self.transactions.append(transaction)
        self.total += abs(transaction.amount)

    def addKeyWords(self, key_words: set):
        self.key_words.update(key_words)

    def extend(self, other_category):
        if self.name == other_category.name:
            self.addKeyWords(other_category.key_words)
            self.transactions.extend(other_category.transactions)
            self.total += other_category.total

    def transactionsToCellDataJSON(self):
        values_list = []

        for trans in self.transactions:
            values_list.append(trans.toRowDataJSON())

        return values_list

    def toRowDataJSON(self):
        values_list = []

        value_json = {
            "values": [
                {
                    "userEnteredValue": {
                        "stringValue": self.name.upper(),
                    },
                },
            ]
        }

        values_list.append(value_json)
        values_list.extend(self.transactionsToCellDataJSON())

        value_json = {
            "values": [
                {
                    "userEnteredValue": {
                        "stringValue": BLANK_FILLER,
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

        values_list.append(value_json)

        return values_list
