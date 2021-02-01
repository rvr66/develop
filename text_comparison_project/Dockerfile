# Using lightweight alpine image
FROM python:3.7-alpine

# Installing packages
RUN apk update
RUN pip install --no-cache-dir pipenv

# Set an environment variable with the directory
# where we'll be running the app
ENV APP /app

# Create the directory and instruct Docker to operate
# from there from now on
RUN mkdir $APP
WORKDIR $APP

# Defining working directory and adding source code
#WORKDIR /home/raghuveer666/text_comparison_project
#COPY Pipfile Pipfile.lock bootstrap.sh ./
# Copy folder structure and everything in it and place in same place
COPY . .

# Install API dependencies
RUN pipenv install
RUN pipenv install flask

# Start app
EXPOSE 5000
ENTRYPOINT ["/app/bootstrap.sh"]
