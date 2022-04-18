FROM alpine:3.15

RUN apk add --update --no-cache tzdata git python3 py-pip tzdata py3-pynacl
COPY requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt
COPY exec.sh /srv/exec.sh
COPY /src/main.py /srv/main.py
RUN chmod +x /srv/exec.sh
CMD ["/srv/exec.sh"]