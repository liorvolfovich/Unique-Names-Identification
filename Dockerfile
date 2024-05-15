# Use the official Python 3.9 image from Docker Hub
FROM python:3.9

# Set the working directory inside the container
WORKDIR /Unique_Names

# Copy the Python script and CSV file into the container
COPY unique_names.py /Unique_Names/
COPY names.csv /Unique_Names/

# Install the required Python package (editdistance)
RUN pip install editdistance

# Command to run the Python script when the container starts
CMD ["python", "unique_names.py", "names.csv"]
