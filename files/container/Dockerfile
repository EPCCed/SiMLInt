FROM ubuntu

LABEL org.opencontainers.image.source https://github.com/EPCCed/SiMLInt
LABEL org.opencontainers.image.description="SiMLInt demo run of BOUT++ with learned correction."
LABEL org.opencontainers.image.licenses="Apache-2.0"

# Install the necessary packages
USER root

WORKDIR /

COPY files/HW-error-correction /hw-vort-n

RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libcurl4 \
    libcurl4-openssl-dev \
    libcurlpp-dev \
    git \
    cmake \
    make \
    gcc \
    g++ \
    wget \
    libfftw3-bin \
    libfftw3-dev \
    libfftw3-mpi-dev \
    libopenmpi-dev \
    libxml++2.6-dev

RUN mkdir /miniconda3 && mkdir /simlint-bin && chmod 777 /miniconda3 && chmod 777 /simlint-bin
RUN wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O /miniconda3/miniconda.sh
RUN bash /miniconda3/miniconda.sh -b -u -p /miniconda3

RUN /miniconda3/bin/conda create -y --name boutsmartsim python=3.10 cmake git-lfs
RUN /miniconda3/bin/conda init bash

RUN wget https://github.com/HDFGroup/hdf5/releases/download/hdf5-1_14_3/hdf5-1_14_3.tar.gz
RUN tar -xvzf hdf5-1_14_3.tar.gz
RUN cd /hdfsrc && ./configure --prefix=/usr/local --enable-parallel CC=mpicc CCX=mpicxx && make -j 6 && make install -j 6

RUN wget https://downloads.unidata.ucar.edu/netcdf-c/4.9.2/netcdf-c-4.9.2.tar.gz
RUN tar -xvzf netcdf-c-4.9.2.tar.gz
RUN cd /netcdf-c-4.9.2 && ./configure --prefix=/usr/local --enable-parallel4 CC=mpicc CCX=mpicxx && make -j 6 && make install -j 6 

RUN wget https://downloads.unidata.ucar.edu/netcdf-cxx/4.3.1/netcdf-cxx4-4.3.1.tar.gz
RUN tar -xvzf netcdf-cxx4-4.3.1.tar.gz
RUN cd /netcdf-cxx4-4.3.1 && ./configure --prefix=/usr/local CC=mpicc CCX=mpicxx && make -j 6 && make install -j 6 

ENV conda /miniconda3/bin/conda
ENV bashrc /root/.bashrc

RUN $conda init && . $bashrc && conda activate boutsmartsim && pip install numpy cython zoidberg

RUN git clone https://github.com/boutproject/BOUT-dev.git

RUN $conda init && . $bashrc && conda activate boutsmartsim \
    && cd /BOUT-dev \
    && MPICXX_CXX=mpicxx MPICXX=mpicc cmake . -B build  -DCMAKE_BUILD_TYPE=Release -DBOUT_BUILD_EXAMPLES=on \
    && export PYTHONPATH=/BOUT-dev/build/tools/pylib:/BOUT-dev/tools/pylib:$PYTHONPATH \
    && cmake --build build -j 6 \
    && cmake --build build --target hasegawa-wakatani -j 6 \
    && cp build/examples/hasegawa-wakatani/hasegawa-wakatani /simlint-bin/bout-hw \
    && chmod 777 /simlint-bin/bout-hw

RUN $conda init && . $bashrc && conda activate boutsmartsim \
    && cd /BOUT-dev \
    && rm -rf build \
    && sed -i 's/-Dn \* Delp4(n);/+Dn \* Delp2(n);/g' examples/hasegawa-wakatani/hw.cxx \
    && sed -i 's/-Dvort \* Delp4(vort);/+Dvort \* Delp2(vort);/g' examples/hasegawa-wakatani/hw.cxx \
    && MPICXX_CXX=mpicxx MPICXX=mpicc cmake . -B build  -DCMAKE_BUILD_TYPE=Release -DBOUT_BUILD_EXAMPLES=on \
    && export PYTHONPATH=/BOUT-dev/build/tools/pylib:/BOUT-dev/tools/pylib:$PYTHONPATH \
    && cmake --build build -j 6 \
    && cmake --build build --target hasegawa-wakatani -j 6 \
    && cp build/examples/hasegawa-wakatani/hasegawa-wakatani /simlint-bin/gt-hw \
    && chmod 777 /simlint-bin/gt-hw

RUN $conda init && . $bashrc && conda activate boutsmartsim \
    && git lfs install \
    && python -m pip install smartsim\[ml\] \
    && export CC=mpicc \
    && export CXX=mpicxx \
    && smart build --device cpu --no_pt

RUN $conda init && . $bashrc && conda activate boutsmartsim \
    && git clone https://github.com/CrayLabs/SmartRedis.git --branch v0.5.2 SmartRedis \
    && cd SmartRedis \
    && make lib CC=mpicc CXX=mpicxx

RUN $conda init && . $bashrc && conda activate boutsmartsim \
    && export PYTHONPATH=/BOUT-dev/build/tools/pylib:/BOUT-dev/tools/pylib:$PYTHONPATH \
    && cd /hw-vort-n \
    && sed -i 's/$WORK//g' CMakeLists.txt \
    && cmake . -B build -Dbout++_DIR=../BOUT-dev/build -DCMAKE_BUILD_TYPE=Release \
    && cmake --build build --target hasegawa-wakatani -j 6 \
    && cp build/hasegawa-wakatani /simlint-bin/smartsim-hw \
    && chmod 777 /simlint-bin/smartsim-hw

COPY files/container/entrypoint.sh /entrypoint.sh
COPY files/container/smartsim-hw.sh /simlint-bin/smartsim-hw.sh
COPY files/6-simulation/start_db.py /start_db.py

RUN mkdir -p /sim/data && chmod -R 777 /sim
RUN chmod -R 777 /miniconda3

# RUN useradd -ms /bin/bash simlint

# USER simlint

WORKDIR /sim

ENTRYPOINT [ "/entrypoint.sh" ]
