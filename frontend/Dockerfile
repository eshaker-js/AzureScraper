# 1) Build stage
FROM node:18-alpine AS builder
WORKDIR /app

# Install dependencies & build
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# 2) Static‐serve stage
FROM node:18-alpine
WORKDIR /app

# Install a lightweight static server
RUN npm install -g serve

# Copy build output
COPY --from=builder /app/dist ./dist

# Expose port 80 (or whatever you choose)
EXPOSE 80

# Serve the `dist` folder
CMD ["serve", "-s", "dist", "-l", "80"]
