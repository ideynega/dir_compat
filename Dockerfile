# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /build

# Copy the current directory contents into the container at /app
COPY . /build
EXPOSE 5000

COPY build.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/build.sh

CMD ["/usr/local/bin/build.sh"]
