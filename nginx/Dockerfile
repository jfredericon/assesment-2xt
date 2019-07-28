FROM nginx

RUN touch /etc/nginx/conf.d/default.conf

RUN rm /etc/nginx/conf.d/default.conf

COPY nginx.conf /etc/nginx/conf.d/

VOLUME /etc/nginx

