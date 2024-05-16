# Use the official Python 3.9 image from Docker Hub as the base image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /Unique_Names

# Copy the Python script and CSV file into the container
COPY unique_names.py /Unique_Names/
COPY names.csv /Unique_Names/

# Install the required Python package (editdistance)
RUN pip install editdistance

# Set the entrypoint command to run the Python script
ENTRYPOINT ["python", "unique_names.py"]

# Default command arguments to be overridden at runtime
CMD ["", "", "", "", ""]