FROM nginx:1.25-alpine

# Install brotli module
RUN apk add --no-cache nginx-mod-http-brotli \
     && rm -rf /var/cache/apk/*

COPY nginx.conf /etc/nginx/nginx.conf
COPY conf.d/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80 443
CMD ["nginx", "-g", "daemon off;"]
