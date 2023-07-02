FROM alpine:3.17

EXPOSE 8080

RUN apk add --no-cache python3
RUN python3 -m ensurepip

RUN mkdir app/

RUN addgroup -S flask && adduser -S flask -G flask
RUN chown flask:flask app/
USER flask

COPY setup.py rssify.py app/

WORKDIR app/
RUN pip3 install .

CMD ["python3", "rssify.py"]
