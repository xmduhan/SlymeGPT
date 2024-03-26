FROM kasmweb/ubuntu-jammy-dind-rootless:1.14.0

USER root

# Install package
RUN apt update -y
RUN apt install -y build-essential zlib1g-dev libssl-dev libncurses5-dev \
libreadline-dev libsqlite3-dev libbz2-dev libffi-dev liblzma-dev libgdbm-dev tk-dev
RUN apt install -y --only-upgrade google-chrome-stable
# RUN apt install -y openssh-client openssh-server

# Copy Chrome config
COPY .config /home/kasm-user/
RUN chown kasm-user:kasm-user -R /home/kasm-user
RUN chmod -R a+rwx ~/.config

USER kasm-user 
ENV USER="kasm-user"

# Install pyenv
RUN curl https://pyenv.run | bash
ENV PYENV_ROOT="$HOME/.pyenv"
ENV PATH="$PYENV_ROOT/bin:$PYENV_ROOT/shims:$PATH"

# Clone source
RUN echo '3'
RUN git clone https://github.com/xmduhan/flygpt.git /home/kasm-user/source/flygpt

# Create run environment
WORKDIR /home/kasm-user/source/flygpt
RUN pyenv install 3.10
RUN pyenv virtualenv 3.10 flygpt
RUN pyenv local flygpt
RUN pip install -r requirements.txt 

# vim
# RUN git clone https://github.com/xmduhan/config.git /home/kasm-user/.config/config/
# RUN python /home/kasm-user/.config/config/apply.py
# RUN vim -E -s -u "$HOME/.vimrc" +PlugInstall +qall
