import unique_names

# Define the relative path to the CSV file
CSV_FILE_NAME = "names.csv"

def run_tests():
    """
    Run test cases to validate the count_unique_names function.

    @return: None
    """

    name_processor = unique_names.NameProcessor(CSV_FILE_NAME)

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
        result = name_processor.count_unique_names(*args)
        assert result == expected_result, f"Test case {idx} failed: Expected {expected_result}, but got {result}"

    print("All test cases passed!")

if __name__ == '__main__':

    run_tests()
