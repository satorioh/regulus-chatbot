# build stage
FROM python:3.10-slim

# copy files
COPY pyproject.toml pdm.lock /project/
WORKDIR /project

# install PDM
RUN pip install -U pip setuptools wheel
RUN pip install pdm

# install dependencies
RUN pdm install
COPY . .

# Install Doppler CLI
RUN apt-get update && apt-get install -y apt-transport-https ca-certificates curl gnupg build-essential libssl-dev libasound2 wget && \
    curl -sLf --retry 3 --tlsv1.2 --proto "=https" 'https://packages.doppler.com/public/cli/gpg.DE2A7741A397C129.key' | apt-key add - && \
    echo "deb https://packages.doppler.com/public/cli/deb/debian any-version main" | tee /etc/apt/sources.list.d/doppler-cli.list && \
    apt-get update && \
    apt-get -y install doppler
ARG DOPPLER_TOKEN
ENV DOPPLER_TOKEN=$DOPPLER_TOKEN
EXPOSE 8000
CMD ["pdm", "run", "start"]