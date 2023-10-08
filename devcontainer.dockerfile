FROM incebellipipo/devcontainer:jammy

RUN sudo apt-get -qy \
    install ruby-full build-essential zlib1g-dev ; \
    echo 'export GEM_HOME="$HOME/gems"' >> ~/.bashrc ;\
    echo 'export PATH="$HOME/gems/bin:$PATH"' >> ~/.bashrc ;\
    source ~/.bashrc ;\
    gem install jekyll bundler
