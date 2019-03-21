# See file COPYING distributed with python-hypothesis for copyright and 
# license.

FROM debian:latest

EXPOSE 5000

RUN apt-get -y update && apt-get install -y --no-install-recommends \
                            build-essential git libevent-dev libffi-dev \
                            libfontconfig libpq-dev libssl-dev python-dev \
                            python-pip curl gnupg2 socat
RUN curl -sL https://deb.nodesource.com/setup_11.x | bash -
RUN apt-get install -y nodejs
RUN pip install setuptools
RUN pip install tox tox-pip-extensions
RUN npm install -g npm
RUN npm install -g gulp-cli
COPY runner /runner

CMD /runner

# eof
