FROM node:20.18.2-alpine3.21 AS final

WORKDIR /app

COPY frontend/package.json /app/package.json
COPY frontend/package-lock.json /app/package-lock.json

RUN npm install

COPY frontend /app/

EXPOSE 5173

CMD ["npm", "run", "dev"]
