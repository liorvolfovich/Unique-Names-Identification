import csv
import editdistance
import os

# Define the relative path to the CSV file
CSV_FILE_NAME = "names.csv"
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), CSV_FILE_NAME)

# dictionary to store nickname mappings
nicknames_dict = dict()


def load_nicknames_from_csv():
    """
    Load nickname mappings from a CSV file into the global nicknames_dict dictionary.

    @param csv_file_path: Path to the CSV file containing nickname mappings.
    @return: None
    """
    with open(CSV_FILE_PATH, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            original_name = row[0].strip().lower()
            nicknames_list = [nickname.strip().lower() for nickname in row[1:]]
            nicknames_dict[original_name] = nicknames_list


def count_unique_names(bill_first_name: str,
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
    low_bill_first_name = pre_process_first_name(bill_first_name)
    low_bill_last_name = bill_last_name.strip().lower()
    low_ship_first_name = pre_process_first_name(ship_first_name)
    low_ship_last_name = ship_last_name.strip().lower()
    low_name_on_card = bill_name_on_card.strip().lower()
    low_name_card_array = low_name_on_card.split()

    if not (2 <= len(low_name_card_array) <= 3):
        raise ValueError("Name on card must consist of 2 to 3 words")

    # comparing names, including typo and middle name handling, and swapping first and last name on bill_name_on_card
    first_bool = (names_compare(low_bill_first_name[0], low_ship_first_name[0])
                  and names_compare(low_bill_last_name, low_ship_last_name))
    if len(low_bill_first_name) == 2 and len(low_ship_first_name) == 2 and first_bool:
        # both names have a middle name
        first_bool = first_bool and names_compare(low_bill_first_name[1], low_ship_first_name[1])
    second_bool = ((names_compare(low_bill_first_name[0], low_name_card_array[0])
                   and names_compare(low_bill_last_name, low_name_card_array[-1]))
                   or (names_compare(low_bill_first_name[0], low_name_card_array[-1])
                       and names_compare(low_bill_last_name, low_name_card_array[0])))

    if len(low_bill_first_name) == 2 and len(low_name_card_array) == 3 and second_bool:
        # both names have a middle name
        second_bool = second_bool and (names_compare(low_bill_first_name[1], low_name_card_array[1]))

    if first_bool and second_bool:
        return 1

    if not first_bool and not second_bool:
        third_bool = (names_compare(low_ship_first_name[0], low_name_card_array[0])
                      and names_compare(low_ship_last_name, low_name_card_array[-1]))
        if len(low_ship_first_name) == 2 and len(low_name_card_array) == 3 and third_bool:
            # both names have a middle name
            third_bool = third_bool and names_compare(low_ship_first_name[1], low_name_card_array[1])

        if not third_bool:
            return 3

    return 2


def names_compare(name1: str, name2: str) -> bool:
    """
    Compare two names to determine if they are similar based on nicknames or edit distance.

    @param name1: First name to compare.
    @param name2: Second name to compare.
    @return: True if the names are considered similar (based on nicknames or edit distance <= 2), False otherwise.
    We define a typo as 1 <= edit distance <= 2.
    """

    if checking_nicknames(name1, name2) or editdistance.eval(name1, name2) <= 2:
        return True

    return False


def checking_nicknames(name1: str, name2: str) -> bool:
    """
    Check if two names are related through nicknames stored in the nicknames_dict dictionary.

    @param name1: First name to check.
    @param name2: Second name to check.
    @return: True if there is a nickname relationship between the names, False otherwise.
    """
    if name1 in nicknames_dict and name2 in nicknames_dict[name1]:
        return True
    if name2 in nicknames_dict and name1 in nicknames_dict[name2]:
        return True
    return False


def pre_process_first_name(name: str) -> list:
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


def run_tests():
    """
    Run test cases to validate the count_unique_names function.

    @return: None
    """

    # # Test cases based on provided examples
    # assert count_unique_names("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli") == 1
    # assert count_unique_names("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli") == 1
    # assert count_unique_names("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli") == 1
    # assert count_unique_names("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah") == 1
    # assert count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michele Egli") == 2
    #
    # # Test cases with typos
    # assert count_unique_names("John", "Doe", "Jon", "Doe", "John Doe") == 1  # Typo in ship first name
    # assert count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michelle Egli") == 2  # Typo in card name
    # assert count_unique_names("Johntrak", "Doe", "Jon", "Doe", "alice Doe") == 3  # no typo
    #
    # # Test cases with nicknames
    # assert count_unique_names("Al", "Smith", "Alanson", "Smith", "Alanson Smith") == 1  # Al is a nickname of Alanson
    # assert count_unique_names("Charles", "Johnson", "Charlie", "Johnson", "Chuck Johnson") == 1  # Chuck is a nickname of Charlie
    # assert count_unique_names("Brenda", "Wolf", "Brandy", "Wolf", "Brenda Brandy") == 2  # Brandy is a nickname of Brenda
    #
    # # Test cases with middle names
    # assert count_unique_names("Anna J", "Levi", "Anna", "Levi", "Anna J levi") == 1  # Bill name matches ship name and card name
    # assert count_unique_names("Deborah S", "Egli", "Deborah cohen", "Egli", "Deborah Egli") == 2  # Bill name matches card name
    # assert count_unique_names("Michele", "Egli", "Deborah", "Egli", "Michele Deborah Egli") == 2  # Card name matches bill name
    # assert count_unique_names("Ron Shimon", "Bar", "Ron David", "Bar", "Ron Even Bar") == 3  # middle names don't match
    #
    # print("All test cases passed!")

    test_cases = [
        # Test cases based on provided examples
        (("Deborah", "Egli", "Deborah", "Egli", "Deborah Egli"), 1),
        (("Deborah", "Egli", "Debbie", "Egli", "Debbie Egli"), 1),
        (("Deborah", "Egni", "Deborah", "Egli", "Deborah Egli"), 1),
        (("Deborah S", "Egli", "Deborah", "Egli", "Egli Deborah"), 1),
        (("Michele", "Egli", "Deborah", "Egli", "Michele Egli"), 2),

        # Test cases with typos
        (("John", "Doe", "Jon", "Doe", "John Doe"), 1),  # Typo in ship first name
        (("Michele", "Egli", "Deborah", "Egli", "Michelle Egli"), 2),  # Typo in card name
        (("Johntrak", "Doe", "Jon", "Doe", "alice Doe"), 3),  # No typos

        # Test cases with nicknames
        (("Al", "Smith", "Alanson", "Smith", "Alanson Smith"), 1),  # Al is a nickname of Alanson
        (("Charles", "Johnson", "Charlie", "Johnson", "Chuck Johnson"), 1),  # Chuck is a nickname of Charlie
        (("Brenda", "Wolf", "Brandy", "Wolf", "Brenda Brandy"), 2),  # Brandy is a nickname of Brenda

        # Test cases with middle names
        (("Anna J", "Levi", "Anna", "Levi", "Anna J levi"), 1),  # Bill name matches ship name and card name
        (("Deborah S", "Egli", "Deborah cohen", "Egli", "Deborah Egli"), 2),  # Bill name matches card name
        (("Michele", "Egli", "Deborah", "Egli", "Michele Deborah Egli"), 2),  # Card name matches bill name
        (("Ron Shimon", "Bar", "Ron David", "Bar", "Ron Even Bar"), 3),  # Middle names don't match
    ]

    for idx, (args, expected_result) in enumerate(test_cases, 1):
        result = count_unique_names(*args)
        assert result == expected_result, f"Test case {idx} failed: Expected {expected_result}, but got {result}"

    print("All test cases passed!")


if __name__ == '__main__':

    # Load nicknames into a dictionary from the CSV file
    load_nicknames_from_csv()

    # if len(sys.argv) != 2:
    #     print("insert nicknames csv file path as a command-line argument")
    #     sys.exit(1)
    # # Get the CSV file path from the command-line arguments
    # csv_path_from_args = sys.argv[NICKNAME_CSV_ARG]
    #
    # # Load nicknames into a dictionary
    # load_nicknames_from_csv(csv_path_from_args)

    run_tests()
