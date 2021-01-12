from category import Category
from transaction import Transaction

DEFAULT_CATEGORY = "MISC"
COL_SPACER = 5
ROW_SPACER = 5
START_COLUMN = 5
MAX_COL_COUNT = 25


class CategoryList:
    def __init__(self, list_of_categories=None):
        self.categories = {
            DEFAULT_CATEGORY: Category(DEFAULT_CATEGORY)
        }

        if list_of_categories:
            for category in list_of_categories:
                self.categories[category.name] = category

    def __str__(self):
        str_rep = "Categories: "
        str_rep += ', '.join([str(category) for category in self.categories])
        str_rep += "\n"
        str_rep += '\n'.join([str(self.categories[category]) for category in self.categories])

        return str_rep

    def addCategory(self, category: Category):
        if category.name not in self.categories:
            self.categories[category.name] = category

    def getTransactionCategory(self, trans: Transaction):
        for category_name in self.categories:
            if self.categories[category_name].includesTransaction(trans):
                return category_name

        return DEFAULT_CATEGORY

    def getCategoryNames(self):
        return [category_name for category_name in self.categories]

    def addTransaction(self, transaction: Transaction):
        self.categories[self.getTransactionCategory(transaction)].addTransaction(transaction)

    def getCategory(self, category_name):
        return self.categories[category_name]

    def getSummary(self):
        summary = {}

        for category_name in self.categories:
            summary[category_name] = self.categories[category_name].total

        return summary

    def extend(self, category_list):
        for category_name in category_list.categories:
            if category_name not in self.categories:
                self.categories[category_name] = category_list.getCategory(category_name).copy()
            else:
                self.categories[category_name].extend(category_list.getCategory(category_name))

    def toDataJSON(self, row_num=0, col_num=0):
        """
        add to sheet to resemble following pattern
        trans 1     category 1  category 2  category 3
        trans 2     trans c11   trans21     trans31
        trans 3     ...
        ...         trans c1n

                    category 4
                    trans c41


        trans n


        """
        data_list = []
        first_row_completed = False

        # keep track of the number of categories that fit on the row
        start_col = col_num
        start_row = row_num
        next_row_num = row_num
        cat_col_nums = []

        cat_num_on_row = 0

        for category in self.categories:
            if self.categories[category].total == 0.0:
                continue

            data_json = {
                "startRow": start_row,
                "startColumn": start_col,
                "rowData": self.categories[category].toRowDataJSON()
            }

            data_list.append(data_json)
            cat_num_on_row += 1

            if first_row_completed:
                if cat_num_on_row >= len(cat_col_nums):
                    cat_num_on_row %= len(cat_col_nums)
                    start_row = next_row_num

                start_col = cat_col_nums[cat_num_on_row]

                # update the starting row for the new category in the col
                next_row_num = max(next_row_num, start_row + len(self.categories[category]) + ROW_SPACER)

                print("row_nums:", next_row_num)

            else:
                cat_col_nums.append(start_col)
                next_row_num = max(next_row_num, start_row + len(self.categories[category]) + ROW_SPACER)
                start_col += COL_SPACER

                print(cat_col_nums)
                print(next_row_num)

                if start_col >= MAX_COL_COUNT:
                    start_col = cat_col_nums[0]
                    start_row = next_row_num
                    first_row_completed = True
                    cat_num_on_row = 0

        return data_list
