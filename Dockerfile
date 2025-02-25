RUN apt-get install -y libgl1

# Stage 1: Build the React frontend
FROM node:20 AS frontend

WORKDIR /fe
COPY fe/ .
RUN npm install && npm run build

# Stage 2: Setup Flask backend with Gunicorn
FROM python:3.12 AS backend

# Install system dependencies
RUN apt-get update && apt-get install -y libgl1-mesa-glx

WORKDIR /app
COPY app/ .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy built frontend into the Flask static directory
COPY --from=frontend /fe/build /app/static

# Expose the Flask backend port
EXPOSE 8000

# Start Flask with Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]

# Stage 3: Use Nginx to serve the frontend and reverse proxy API requests
FROM nginx:latest

# Copy built frontend from backend stage
COPY --from=backend /app/static /usr/share/nginx/html

# Copy custom Nginx configuration to the correct location
COPY ./nginx.conf /etc/nginx/nginx.conf
#COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80 for the frontend
EXPOSE 80

# Start Nginx
CMD ["nginx", "-g", "daemon off;"]
