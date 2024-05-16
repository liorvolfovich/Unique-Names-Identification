import csv
import editdistance
import os
import sys

# Define the relative path to the CSV file
CSV_FILE_NAME = "names.csv"

# Define constants for numbers
BILL_FIRST_NAME = 1
BILL_LAST_NAME = 2
SHIP_FIRST_NAME = 3
SHIP_LAST_NAME = 4
BILL_NAME_ON_CARD = 5
ONE_UNIQUE_NAME = 1
TWO_UNIQUE_NAMES = 2
THREE_UNIQUE_NAMES = 3
MAX_LEN_FIRST_NAME = 2
MAX_LEN_NAME_ON_CARD = 3
MIN_LEN_NAME_ON_CARD = 2
NUM_OF_ARGS = 6


class NameProcessor:
    def __init__(self, csv_file_name):
        # Define the relative path to the CSV file
        self.csv_file_path = os.path.join(os.path.dirname(__file__), csv_file_name)
        self.nicknames_dict = dict()  # dictionary to store nickname mappings
        self.load_nicknames_from_csv()

    def load_nicknames_from_csv(self):
        """
        Load nickname mappings from a CSV file into the global nicknames_dict dictionary.

        @return: None
        """
        with open(self.csv_file_path, newline='') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                original_name = row[0].strip().lower()
                nicknames_list = [nickname.strip().lower() for nickname in row[1:]]
                self.nicknames_dict[original_name] = nicknames_list


    def count_unique_names(self,
                           bill_first_name: str,
                           bill_last_name: str,
                           ship_first_name: str,
                           ship_last_name: str,
                           bill_name_on_card: str) -> int:
        """
        count the number of unique names in a transaction.

        @param bill_first_name: First name on the billing information.
        @param bill_last_name: Last name on the billing information.
        @param ship_first_name: First name on the shipping information.
        @param ship_last_name: Last name on the shipping information.
        @param bill_name_on_card: Name on the card used for billing.
        @return: An integer code indicating the uniqueness of the names (1 = unique, 2 = match with typos, 3 = no match).
        """

        if None in (bill_first_name, bill_last_name, ship_first_name, ship_last_name, bill_name_on_card):
            raise ValueError("None values are not allowed")

        # remove leading and trailing whitespaces and converting uppercase letters to lowercase letters
        low_bill_first_name = self.pre_process_first_name(bill_first_name)
        low_bill_last_name = bill_last_name.strip().lower()
        low_ship_first_name = self.pre_process_first_name(ship_first_name)
        low_ship_last_name = ship_last_name.strip().lower()
        low_name_on_card = bill_name_on_card.strip().lower()
        low_name_card_array = low_name_on_card.split()

        if not (MIN_LEN_NAME_ON_CARD <= len(low_name_card_array) <= MAX_LEN_NAME_ON_CARD):
            raise ValueError("Name on card must consist of 2 to 3 words")

        # comparing names, including typo and middle name handling, and swapping first and last name on bill_name_on_card
        first_bool = (self.names_compare(low_bill_first_name[0], low_ship_first_name[0])
                      and self.names_compare(low_bill_last_name, low_ship_last_name))
        if len(low_bill_first_name) == MAX_LEN_FIRST_NAME and len(low_ship_first_name) == MAX_LEN_FIRST_NAME and first_bool:
            # both names have a middle name
            first_bool = first_bool and self.names_compare(low_bill_first_name[1], low_ship_first_name[1])
        second_bool = ((self.names_compare(low_bill_first_name[0], low_name_card_array[0])
                       and self.names_compare(low_bill_last_name, low_name_card_array[-1]))
                       or (self.names_compare(low_bill_first_name[0], low_name_card_array[-1])
                           and self.names_compare(low_bill_last_name, low_name_card_array[0])))

        if len(low_bill_first_name) == MAX_LEN_FIRST_NAME and len(low_name_card_array) == MAX_LEN_NAME_ON_CARD and second_bool:
            # both names have a middle name
            second_bool = second_bool and (self.names_compare(low_bill_first_name[1], low_name_card_array[1]))

        if first_bool and second_bool:
            return ONE_UNIQUE_NAME

        if not first_bool and not second_bool:
            third_bool = (self.names_compare(low_ship_first_name[0], low_name_card_array[0])
                          and self.names_compare(low_ship_last_name, low_name_card_array[-1]))
            if len(low_ship_first_name) == MAX_LEN_FIRST_NAME and len(low_name_card_array) == MAX_LEN_NAME_ON_CARD and third_bool:
                # both names have a middle name
                third_bool = third_bool and self.names_compare(low_ship_first_name[1], low_name_card_array[1])

            if not third_bool:
                return THREE_UNIQUE_NAMES

        return TWO_UNIQUE_NAMES


    def names_compare(self, name1: str, name2: str) -> bool:
        """
        Compare two names to determine if they are similar based on nicknames or edit distance.

        @param name1: First name to compare.
        @param name2: Second name to compare.
        @return: True if the names are considered similar (based on nicknames or edit distance <= 2), False otherwise.
        We define a typo as 1 <= edit distance <= 2.
        """

        if self.checking_nicknames(name1, name2) or editdistance.eval(name1, name2) <= 2:
            return True

        return False


    def checking_nicknames(self, name1: str, name2: str) -> bool:
        """
        Check if two names are related through nicknames stored in the nicknames_dict dictionary.

        @param name1: First name to check.
        @param name2: Second name to check.
        @return: True if there is a nickname relationship between the names, False otherwise.
        """
        if name1 in self.nicknames_dict and name2 in self.nicknames_dict[name1]:
            return True
        if name2 in self.nicknames_dict and name1 in self.nicknames_dict[name2]:
            return True
        return False


    def pre_process_first_name(self, name: str) -> list:
        """
        Pre-process a given name by stripping whitespace, converting to lowercase, and handling middle names.

        @param name: The name to pre-process.
        @return: A list containing the pre-processed name (split by whitespace if middle name exists).
        """
        name = name.strip().lower()
        # we remove the middle name if it exists
        ret_list = []
        if ' ' in name:
            space_idx = name.index(' ')
            ret_list.append(name[:space_idx])
            ret_list.append(name[space_idx+1:])
        else:
            ret_list.append(name)
        return ret_list



if __name__ == '__main__':

    name_processor = NameProcessor(CSV_FILE_NAME)

    if len(sys.argv) != NUM_OF_ARGS:
        print("please enter params of a transaction as follows:\n"
              "bill_first_name bill_last_name ship_first_name ship_last_name bill_name_on_card\n"
              "make sure to use double quotes for the names!\n")
        sys.exit(1)
    for idx in range(1, NUM_OF_ARGS):
        if len(sys.argv[idx]) == 0:
            print("please enter all the names in the transaction\n")
            sys.exit(1)

    res = name_processor.count_unique_names(sys.argv[BILL_FIRST_NAME], sys.argv[BILL_LAST_NAME],
                                            sys.argv[SHIP_FIRST_NAME], sys.argv[SHIP_LAST_NAME],
                                            sys.argv[BILL_NAME_ON_CARD])
    print("Number of unique names in the transaction: " + str(res))
