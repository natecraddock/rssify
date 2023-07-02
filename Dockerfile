FROM python:3.11-alpine

EXPOSE 8080

RUN mkdir app/

RUN addgroup -S flask && adduser -S flask -G flask
RUN chown flask:flask app/
USER flask

COPY setup.py rssify.py app/

WORKDIR app/
RUN pip3 install .

CMD ["python", "rssify.py"]
