FROM nginx:1.25.3-alpine

# Remove the default nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom nginx configuration
# Note: nginx.conf should be in the same directory as this Dockerfile
COPY ./nginx.conf /etc/nginx/conf.d/default.conf
