# Stage 1 — build frontend
FROM node:20-alpine AS frontend-builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend/ .
ARG VITE_APP_API_ROOT=""
ARG VITE_APP_REPO_URL=""
ARG VITE_APP_BUG_REPORT_URL=""
RUN npm run build

# Stage 2 — nginx with routing + built frontend
FROM nginx:alpine
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/coolify.conf /etc/nginx/conf.d/default.conf
COPY --from=frontend-builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
