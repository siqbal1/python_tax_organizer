CURR_YEAR = 2000


class Transaction:
    def __init__(self, date: str = "", description: str = "", amount: float = 0.0):

        # assume date in form mm/dd/yy or mm/dd/yyyy
        self.date = date
        self.description = description
        self.amount = amount

    def __str__(self):
        ret_str = f"{self.date} {self.description} ${self.amount}"
        return ret_str

    def parseDate(self):
        """
        parse date as return list as [month, day, year]
        """
        date_parts = self.date.split("/")
        date_dict = {
            "month": int(date_parts[0]),
            "day": int(date_parts[1]),
        }

        if(len(date_parts[-1]) > 2):
            date_dict["year"] = int(date_parts[-1])
        else:
            date_dict["year"] = CURR_YEAR + int(date_parts[-1])

        return date_dict

    def getMonth(self) -> str:
        date_parts = self.parseDate()
        return date_parts["month"]

    def getDay(self) -> str:
        date_parts = self.parseDate()
        return date_parts["day"]

    def getYear(self) -> str:
        date_parts = self.parseDate()
        return date_parts["year"]

    def toRowDataJSON(self):
        json = {
            "values": [
                {
                    "userEnteredValue": {
                        "stringValue": str(self.date),
                    },
                },
                {
                    "userEnteredValue": {
                        "stringValue": str(self.description),
                    },
                },
                {
                    "userEnteredValue": {
                        "numberValue": self.amount,
                    },
                },
            ]
        }

        return json
