FROM node:22-alpine AS build

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .
RUN npm run build -- --configuration production

FROM nginx:alpine
EXPOSE 8096
COPY nginx.conf /etc/nginx/nginx.conf
COPY --from=build /app/dist/comp642/browser /usr/share/nginx/html