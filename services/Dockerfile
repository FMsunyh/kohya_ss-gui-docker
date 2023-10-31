FROM alpine/git:2.36.2 as download

COPY clone.sh /clone.sh
RUN . /clone.sh kohya-ss-gui https://github.com/bmaltais/kohya_ss.git  0ce88bba71c069b70ca7609efce3b7d4463c6dc0

FROM fmsunyh/kohya-ss-gui:21.8.9

ENV ROOT=/kohya-ss-gui
WORKDIR ${ROOT}

RUN rm -rf ${ROOT}/*

COPY --from=download /repositories/kohya-ss-gui ${ROOT}

RUN --mount=type=cache,target=/var/cache/apt \
  apt-get update && \
  # we need those
  apt-get install -y openssh-server vim  aria2

USER root

RUN echo 'root:l6y#VJWJA4LGr1eI' | chpasswd 

##config ssh
RUN echo 'Port 22' >> /etc/ssh/sshd_config 
RUN echo 'PermitRootLogin yes' >>  /etc/ssh/sshd_config
RUN mkdir /var/run/sshd

# RUN --mount=type=cache,target=/cache --mount=type=cache,target=/root/.cache/pip \
#     pip install -r ./requirements_linux_docker.txt  -i https://mirrors.aliyun.com/pypi/simple/ \
#     pip install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/


RUN python3 -m pip install -r ./requirements_linux_docker.txt  -i https://mirrors.aliyun.com/pypi/simple/
RUN python3 -m pip install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY ./entrypoint.sh ./entrypoint.sh
COPY  ./requirements.txt /opt/requirements.txt
RUN python3 -m pip install -r /opt/requirements.txt


# Replace pillow with pillow-simd
RUN python3 -m pip uninstall -y pillow && \
    CC="cc -mavx2" python3 -m pip install -U --force-reinstall pillow-simd

COPY  ./server_app.sh /opt/server_app.sh

RUN  jupyter server --generate-config
COPY  ./jupyter_server_config.json /root/.jupyter/jupyter_server_config.json

ENV LD_PRELOAD=libtcmalloc.so

EXPOSE 22
EXPOSE 8889
EXPOSE 6860
EXPOSE 6006

STOPSIGNAL SIGINT
ENTRYPOINT ["/bin/bash","./entrypoint.sh", "/opt/server_app.sh"]
