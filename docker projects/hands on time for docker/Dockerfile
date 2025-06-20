FROM node:18 AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .


FROM node:18-slim AS production
WORKDIR /app
COPY package*.json ./
RUN npm install --only=production
COPY --from=builder /app/app.js .
EXPOSE 3000
HEALTHCHECK --interval=30s --timeout=3s \
  CMD curl -f http://localhost:3000/ || exit 1

CMD ["node", "app.js"]

