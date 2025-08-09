# Multi-stage build for Flutter Web
# Stage 1: Build the Flutter web app
FROM cirrusci/flutter:3.16.0 AS build

# Set work directory
WORKDIR /app

# Copy pubspec files first for better caching
COPY pubspec.yaml pubspec.lock ./

# Get Flutter dependencies
RUN flutter pub get

# Copy the entire project
COPY . .

# Enable Flutter web
RUN flutter config --enable-web

# Build the web app for production
RUN flutter build web --release

# Stage 2: Serve the app with Nginx
FROM nginx:alpine

# Copy the built web app from the previous stage
COPY --from=build /app/build/web /usr/share/nginx/html

# Copy custom nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost:80/ || exit 1

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]