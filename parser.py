import pdfplumber
import re
import os
from transaction import Transaction
from transaction_summary import TransactionSummary
from yearly_summary import YearlySummary
from category import Category
from category_list import CategoryList

DEPOSIT_INDICATOR = "Deposits and other credits"
WITHDRAWL_INDICATOR = "Withdrawals and other debits"
CHECK_INDICATOR = "Checks"
AMOUNT_REGEX = re.compile("^(-)?\d+\.\d{2}$")
DATE_REGEX = re.compile("^\d{2}\/\d{2}\/(\d{2}|\d{4})$")

CATEGORY_DIR = "Category_Txts/"
DEPOSIT_CATEGORY_FILE = CATEGORY_DIR + "Deposit Categories.txt"
WITHDRAWL_CATEGORY_FILE = CATEGORY_DIR + "Withdrawls Categories.txt"
CHECKS_CATEGORY_FILE = CATEGORY_DIR + "Checks Categories.txt"


def is_valid_date(date_text):
    return DATE_REGEX.match(date_text)


def parse_amount_from_string(float_text):
    """
    Parse text and return a float or None
    """
    try:
        # get rid of misc symbols and convert string
        float_text = float_text.replace(',', '')
        float_text = float_text.replace('$', '')

        if AMOUNT_REGEX.match(float_text):
            return float(float_text)
        else:
            return None

    except ValueError:
        return None


def parse_transaction_string(transaction: str):
    """ Returns list of transactions from a string
    Expected string format: mm/dd/yy description... float_val ... mm/dd/yy description... float_val... mm/dd/yy
    
    :param transaction: a string with a transactions in it
    :type transaction: str
    :return: list of transactions parsed from string
    :rtype list[Transactions]
    """
    if not transaction:
        return None

    trans_details = transaction.split()
    trans_list = []
    date = ""
    description = ""
    amount = None

    if is_valid_date(trans_details[0]):
        for string in trans_details:
            if (date and description and amount):
                trans_list.append(Transaction(date, description.strip(), abs(amount)))
                date = ""
                description = ""
                amount = None

            if not date:
                if is_valid_date(string):
                    date = string.strip()

            else:
                if not amount:
                    float_val = parse_amount_from_string(string)

                    if float_val:
                        amount = float_val

                        if not description:
                            date = ""
                            description = ""
                            amount = None
                    else:
                        description += (string.strip() + " ")

    if (date and description and amount):
        trans_list.append(Transaction(date, description.strip(), abs(amount)))

    return trans_list


def init_categories(transaction_summary: TransactionSummary):
    """
    Read categories for each transaction type from Category_Txts directory
    """
    transaction_summary.setDepositCategoryList(parse_deposit_categories())
    transaction_summary.setWithdrawlsCategoryList(parse_withdrawl_categories())
    transaction_summary.setChecksCategoryList(parse_check_categories())


def extract_transaction_summary(pages):
    transaction_summary = TransactionSummary()

    init_categories(transaction_summary)

    reading_deposits = False
    reading_withdrawls = False
    reading_checks = False

    for page in pages:

        lines = page.extract_text().split("\n")

        for line in lines:

            if line.lower().strip() == WITHDRAWL_INDICATOR.lower():
                reading_withdrawls = True
                reading_deposits = False
                reading_checks = False

                # print("reading withdrawls")

            if line.lower().strip() == DEPOSIT_INDICATOR.lower():
                reading_withdrawls = False
                reading_deposits = True
                reading_checks = False

                # print("reading deposits")

            if line.lower().strip() == CHECK_INDICATOR.lower() and reading_withdrawls:
                reading_withdrawls = False
                reading_deposits = False
                reading_checks = True

                # print("reading checks")

            trans_list = parse_transaction_string(line)

            if trans_list:
                if reading_deposits:
                    transaction_summary.addDeposits(trans_list)
                elif reading_withdrawls:
                    transaction_summary.addWithdrawls(trans_list)
                elif reading_checks:
                    transaction_summary.addChecks(trans_list)

                    # print(transaction_summary)
    return transaction_summary

    # for trans in transaction_summary.deposits:
    #     print(trans)


def parse_pdf_statement(file_path: str):
    with pdfplumber.open(file_path) as pdf:
        monthly_transactions = extract_transaction_summary(pdf.pages)
        return monthly_transactions


def get_ordered_file_list(dir_path):
    directory = r'{}'.format(dir_path)

    file_list = []

    for entry in os.scandir(directory):
        if entry.path.endswith(".pdf") and entry.is_file():
            file_list.append(entry.path)

    file_list.sort()
    return file_list


def parse_pdf_statements_from_directory(dir_path: str):
    file_list = get_ordered_file_list(dir_path)
    yearly_summary = YearlySummary()

    for file_path in file_list:
        print(file_path)
        monthly_transactions = parse_pdf_statement(file_path)
        yearly_summary.addSummary(monthly_transactions)

    return yearly_summary


def parse_categories_from_file(file):
    category_list = []

    with open(file) as category_file:
        categories = category_file.readlines()

        # each category on its own line
        # format: cat_name - key1, key2, ...
        for category_str in categories:
            if category_str[0] != '/' and len(category_str.strip()) > 0:
                split_category = category_str.split('-')
                category_name = split_category[0].strip()
                key_word_list = set([key_word.strip() for key_word in split_category[1].split(',')])
                category_list.append(Category(category_name, key_word_list))

    return CategoryList(category_list)

def parse_deposit_categories():
    return parse_categories_from_file(DEPOSIT_CATEGORY_FILE)


def parse_withdrawl_categories():
    return parse_categories_from_file(WITHDRAWL_CATEGORY_FILE)


def parse_check_categories():
    return parse_categories_from_file(CHECKS_CATEGORY_FILE)
