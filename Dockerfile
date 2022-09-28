FROM python:3.7-slim
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV RUN_HEADLESS True

RUN apt update && \
    apt install --no-install-recommends -y \
                 xvfb \
                 wget \
                 unzip

RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb && \
    apt install -y ./google-chrome-stable_current_amd64.deb && \
    rm -rf /var/lib/apt/lists/* && \
    apt-get purge -y --auto-remove && \
    rm -rf /etc/apt/sources.list.d/temp.list && \
    rm google-chrome-stable_current_amd64.deb


ENV USERNAME ahadi
ENV USER_UID=1000
ENV USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd --uid $USER_UID --gid $USER_GID -m $USERNAME --home-dir /code

USER $USERNAME
WORKDIR /code

RUN wget -q https://chromedriver.storage.googleapis.com/LATEST_RELEASE -O LATEST_RELEASE.txt && \
    chromedriver_version=$(cat LATEST_RELEASE.txt | sed 's/\n//g' ) && \
    wget -q https://chromedriver.storage.googleapis.com/$chromedriver_version/chromedriver_linux64.zip && \
    unzip chromedriver_linux64.zip && \
    rm chromedriver_linux64.zip LATEST_RELEASE.txt && \
    chmod +x chromedriver &&\
    mkdir screenshots &&\
    pip install --upgrade pip

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]

