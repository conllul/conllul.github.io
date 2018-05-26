FROM ubuntu
MAINTAINER Amir More (habeanf@gmail.com)
RUN apt -qq update
# base installation
RUN apt -qq -y install python3 python3-pip wget git
# needed for TRmorph
RUN apt -qq -y install foma-bin make
# install go for yap
RUN wget https://dl.google.com/go/go1.10.2.linux-amd64.tar.gz -O /tmp/go1.10.2.tar.gz
RUN tar -C /usr/local -xzf /tmp/go1.10.2.tar.gz
ENV PATH $PATH:/usr/local/go/bin

# yap (baseline + hebrew MA)
RUN mkdir /home/gopath
WORKDIR /home/gopath
ENV GOPATH /home/gopath
RUN mkdir /home/gopath/src /home/gopath/bin
WORKDIR /home/gopath/src
RUN git clone https://github.com/habeanf/yap
WORKDIR /home/gopath/src/yap
RUN go get .
RUN go build .

# trmorph2 (turkish MA)
WORKDIR /home/
RUN git clone https://github.com/coltekin/TRmorph
WORKDIR /home/TRmorph
RUN git checkout trmorph2
RUN make depend
RUN make

# add data-driven lexicons
ADD *json /home/gopath/src/yap/data/
ADD UDLex* /home/gopath/src/yap/data/

# update yap
WORKDIR /home/gopath/src/yap
RUN git pull
RUN go build .

# get dispatcher
ENV YAP=/home/gopath/src/yap LEX_DIR=/home/gopath/src/yap/data DISPATCH=/home
ADD dispatch/*.py /home/
ADD dispatch/*csv /home/

# leave a mount dir
RUN mkdir /local
WORKDIR /local

ENTRYPOINT ["/home/conllul_dispatch.py"]
