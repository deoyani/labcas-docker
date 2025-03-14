# mock-auth-service/Dockerfile
FROM node:16-alpine

# Create app directory
WORKDIR /usr/src/app

# Copy package*.json
COPY package*.json ./

# Install dependencies
RUN npm install --only=production

# Bundle app source
COPY . .

# Expose port (optional; for clarity)
EXPOSE 3001

CMD [ "node", "mockAuth.js" ]
