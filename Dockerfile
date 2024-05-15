# Use the official Python 3.9 image from Docker Hub
FROM python:3.9

# Set the working directory inside the container
WORKDIR /Forter_Challenge

# Copy the Python script and CSV file into the container
COPY forter_challenge.py /Forter_Challenge/
COPY names.csv /Forter_Challenge/

# Install the required Python package (editdistance)
RUN pip install editdistance

# Command to run the Python script when the container starts
CMD ["python", "forter_challenge.py", "names.csv"]
