FROM node:18-alpine

WORKDIR /app

# Copy dependency mappings
COPY package.json ./

# Install npm packages
RUN npm install

# Copy frontend source files
COPY . .

# Expose Vite dev port
EXPOSE 3000

# Start Vite dev server in host mode
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
