# Use the official Nginx image as a base
FROM nginx:latest

# Install wget and install/updates certificates
RUN apt-get update && apt-get install -y wget && apt-get install -y ca-certificates \
    && update-ca-certificates

# Download and install Dockerize
RUN wget https://github.com/jwilder/dockerize/releases/download/v0.6.1/dockerize-linux-amd64-v0.6.1.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-v0.6.1.tar.gz \
    && rm dockerize-linux-amd64-v0.6.1.tar.gz

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy a new configuration file from your project to the container
COPY nginx/default.conf /etc/nginx/conf.d/

# (Optional) Copy static assets from your project to the container
# COPY static/ /usr/share/nginx/html/

# Expose port 80
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]

