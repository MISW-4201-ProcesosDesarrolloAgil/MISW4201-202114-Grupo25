FROM node:alpine AS my-app-build
WORKDIR /app
COPY . .

ARG ENV_TYPE
RUN npm ci && npm run build

FROM nginx:alpine
COPY --from=my-app-build /app/dist/tutorial-canciones /usr/share/nginx/html

COPY ./nginx.conf /etc/nginx/conf.d/default.conf

CMD sed -i -e 's/$PORT/'"$PORT"'/g' /etc/nginx/conf.d/default.conf && nginx -g 'daemon off;'