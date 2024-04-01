FROM kasmweb/ubuntu-jammy-dind-rootless:1.14.0

USER root

# Install package
RUN apt update -y
RUN apt install -y build-essential zlib1g-dev libssl-dev libncurses5-dev \
libreadline-dev libsqlite3-dev libbz2-dev libffi-dev liblzma-dev libgdbm-dev tk-dev
RUN apt install -y --only-upgrade google-chrome-stable
RUN apt install -y openssh-client openssh-server

# Copy Chrome config
COPY .config /home/kasm-user/
RUN chown kasm-user:kasm-user -R /home/kasm-user
RUN chmod -R a+rwx /home/kasm-user/.config

USER kasm-user 
ENV USER="kasm-user"

# Install pyenv
RUN curl https://pyenv.run | bash
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

# Clone source
RUN git clone https://github.com/xmduhan/flygpt.git /home/kasm-user/source/flygpt

# Create run environment
WORKDIR /home/kasm-user/source/flygpt
RUN pyenv install 3.10
RUN pyenv virtualenv 3.10 flygpt
RUN pyenv local flygpt
RUN pip install -r requirements.txt 
RUN pip install -e .
