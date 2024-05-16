# Unique Names Identification

This project implements a method to determine the uniqueness of names in a transaction based on various criteria, including nickname mappings and edit distance.

## Setup

To run this project, you can use Docker. Ensure you have Docker installed on your system before proceeding.

### Cloning the Git Repository

You can clone this Git repository to get the project files locally. Use the following command in your terminal:

```bash
git clone https://github.com/liorvolfovich/Unique-Names-Identification.git
```

This will create a local copy of the project in a directory named `unique-names`.

### Docker Instructions

#### Build the Docker Image

Navigate into the project directory (`unique-names`) and run the following command to build the Docker image:

```bash
docker build -t unique-names .
```

#### Run the Docker Container

After building the image, you can run the Docker container using the following command:

```bash
docker run --rm unique-names "bill_first_name" "bill_last_name" "ship_first_name" "ship_last_name" "bill_name_on_card"
```

Replace `bill_first_name`, `bill_last_name`, `ship_first_name`, `ship_last_name`, and `bill_name_on_card` with the actual names for your transaction. Make sure to use double quotes (`"`) for each name if they contain spaces.

This command will execute the Python script inside the container, which counts the number of unique names in the transaction.

## Files

The project consists of the following components:

- **Dockerfile**: Specifies the environment setup for running the Python script.
- **unique_names.py**: Contains the implementation of the `count_unique_names` function, which determines the uniqueness of names in a transaction.
- **names.csv**: A CSV file containing nickname mappings used by the `count_unique_names` function.
- **tests.py**: Contains test cases to validate the `count_unique_names` function.


## Running Tests

The `tests.py` script contains test cases to validate the `count_unique_names` function. To run the tests, execute the following command in your terminal from the project directory (`unique-names`):

```bash
python tests.py
```

This will run the test cases and display the results. All test cases should pass if the `count_unique_names` function is implemented correctly.

## Requirements

- Docker
- Python 3.9
- Git

----

![Docker Image](https://d1.awsstatic.com/acs/characters/Logos/Docker-Logo_Horizontel_279x131.b8a5c41e56b77706656d61080f6a0217a3ba356d.png)
