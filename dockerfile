FROM ubuntu:20.04
RUN echo 'APT::Install-Suggests "0";' >> /etc/apt/apt.conf.d/00-docker
RUN echo 'APT::Install-Recommends "0";' >> /etc/apt/apt.conf.d/00-docker
RUN DEBIAN_FRONTEND=noninteractive \
  apt-get update \
  && rm -rf /var/lib/apt/lists/*

ARG CC=gcc

COPY criu/scripts/ci/apt-install /bin/apt-install

# On Ubuntu, kernel modules such as ip_tables and xt_mark may not be loaded by default
# We need to install kmod to enable iptables to load these modules for us.
RUN apt-install \
	libnet-dev \
	libnl-route-3-dev \
	$CC \
	bsdmainutils \
	build-essential \
	git-core \
	iptables \
	libaio-dev \
	libbsd-dev \
	libcap-dev \
	libgnutls28-dev \
	libgnutls30 \
	libnftables-dev \
	libnl-3-dev \
	libprotobuf-c-dev \
	libprotobuf-dev \
	libselinux-dev \
	iproute2 \
	kmod \
	pkg-config \
	protobuf-c-compiler \
	protobuf-compiler \
        python-protobuf \
        python-ipaddress \
        python2 \
        sudo \
        wget \
        ca-certificates

# pip2 dependency needs to solved by using this method
RUN wget https://bootstrap.pypa.io/pip/2.7/get-pip.py
RUN python2 get-pip.py 

RUN mkdir -p /DynaCut
COPY . /DynaCut

WORKDIR /DynaCut/criu

RUN date && \
# Check single object build
	make -j $(nproc) CC="$CC" criu/parasite-syscall.o && \
# Compile criu
	make -j $(nproc) CC="$CC" && \
	date && \
# Check that "make mrproper" works
	make mrproper

# Re-compile criu and compile tests for 'make docker-test'
RUN make -j $(nproc) CC="$CC" && \
	date &&  make -j $(nproc) CC="$CC" -C test/zdtm && date

RUN pip2 install capstone pyelftools==0.29

WORKDIR /DynaCut
ENV USER=root
