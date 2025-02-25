# Use Node.js to build the React frontend
FROM node:20 as build

# Step 2: Set the working directory in the container
WORKDIR /app

# Step 3: Copy package.json and package-lock.json for installing dependencies
COPY package.json package-lock.json ./

# Step 4: Install dependencies
RUN npm install

# Step 5: Copy the rest of the application source code
COPY . .

# Step 6: Build the ReactJS application for production
RUN npm run build

# Step 7: Use Nginx to serve the built application
FROM nginx:alpine

# Step 8: Copy the built React app from the build stage to the Nginx server
COPY --from=build /app/build /usr/share/nginx/html

# Step 9: Expose the port for the frontend
EXPOSE 80

# Step 10: Start Nginx
CMD ["nginx", "-g", "daemon off;"]
