FROM kasmweb/ubuntu-jammy-dind-rootless:1.14.0
USER root
RUN apt update -y
RUN apt install -y build-essential zlib1g-dev libssl-dev libncurses5-dev \
libreadline-dev libsqlite3-dev libbz2-dev libffi-dev liblzma-dev libgdbm-dev tk-dev
RUN apt install -y --only-upgrade google-chrome-stable
USER kasm-user 
RUN curl https://pyenv.run | bash
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"
RUN eval "$(pyenv init -)"
RUN eval "$(pyenv virtualenv-init -)"
RUN eval "$(direnv hook bash)"
WORKDIR /home/kasm_user/flygpt
RUN pyenv install 3.10
RUN pyenv virtualenv 3.10 flygpt
RUN pyenv local flygpt
COPY requirements.txt .
RUN pip install -r requirements.txt 
COPY src/* ./src/
WORKDIR /home/kasm_user/flygpt
RUN python src/install_chromedriver.py
