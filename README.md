Python 3 application to parse pdf bank statements and extract transactions information. Parses bank statements and categorizes transaction into user defined categories. Great for end of the year financial summaries. Provides a categorical breakdown of bank statements on a yearly and a monthly basis. Uploads transaction summaries to your google sheets for ease of use and readability.

Usage:
1. Download pdf bank statements from Bank of America
2. Place all the pdf statements into the same folder as the program in the Bank_Statements directory. If the directory does not already exist then create it.
3. In the Category_Txts folder follow the instructions in each file to create categories for all of your transaction types
4. Open terminal and cd into the directory where the program is stored
5. Run program using following command on the command line:
	python3 main.py
6. Program will prompt you to log into google to allow access for uploading the transaction summary file.

