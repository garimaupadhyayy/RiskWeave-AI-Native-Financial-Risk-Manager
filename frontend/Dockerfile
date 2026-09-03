FROM node:20-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

# Next.js telemetry
ENV NEXT_TELEMETRY_DISABLED=1

RUN npm run build

CMD ["npm", "start"]
