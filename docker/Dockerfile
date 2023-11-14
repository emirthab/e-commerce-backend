FROM tiangolo/uvicorn-gunicorn:python3.11
LABEL maintainer="Sebastian Ramirez <tiangolo@gmail.com>"

COPY . /home
WORKDIR /home
ENV ENV=dev
ENV DEBUG=1
RUN pip install "poetry==1.5.1"
RUN poetry config virtualenvs.create false \
    && poetry install --only main
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# RUN chmod +x /home/docker/startup.sh
# ENTRYPOINT /home/docker/startup.sh
CMD ["/bin/sh","/home/docker/startup.sh"]