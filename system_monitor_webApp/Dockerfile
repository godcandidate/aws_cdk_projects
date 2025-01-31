# use official python
FROM python:3.10.16-slim

# set working directory of container
WORKDIR /app

# copy the requiremeents files into container
COPY requirements.txt .

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# copy the rest of the application code
COPY . .

# Expose the port 
EXPOSE 8050

# Command to run the application
CMD ["python", "system_monitor.py", "one"]
