FROM alpine/git:2.36.2 as download

COPY clone.sh /clone.sh
RUN . /clone.sh kohya-ss-gui https://github.com/bmaltais/kohya_ss.git  17f58c8bb9bc38773a870df58e1ae788abf6753b

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

COPY ./src/requirements_linux_docker.txt /kohya-ss-gui/requirements_linux_docker.txt

RUN --mount=type=cache,target=/cache --mount=type=cache,target=/root/.cache/pip \
    pip install -r ./requirements_linux_docker.txt  -i https://mirrors.aliyun.com/pypi/simple/ \
    pip install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/


# RUN python3 -m pip install -r ./requirements_linux_docker.txt  -i https://mirrors.aliyun.com/pypi/simple/
# RUN python3 -m pip install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

COPY ./entrypoint.sh ./entrypoint.sh
COPY  ./requirements.txt /opt/requirements.txt
RUN python3 -m pip install -r /opt/requirements.txt


# Replace pillow with pillow-simd
# RUN python3 -m pip uninstall -y pillow && \
#     CC="cc -mavx2" python3 -m pip install -U --force-reinstall pillow-simd

COPY  ./server_app.sh /opt/server_app.sh

RUN  jupyter server --generate-config
COPY  ./jupyter_server_config.json /root/.jupyter/jupyter_server_config.json
COPY ./src/make_captions_by_git.py /kohya-ss-gui/finetune/make_captions_by_git.py

COPY ./data/huggingface/hub/models--bert-base-uncased  /root/.cache/huggingface/hub/models--bert-base-uncased
COPY ./data/huggingface/hub/models--openai--clip-vit-large-patch14  /root/.cache/huggingface/hub/models--openai--clip-vit-large-patch14
COPY ./data/huggingface/hub/models--microsoft--git-large-textcaps  /root/.cache/huggingface/hub/models--microsoft--git-large-textcaps
COPY ./data/pretrain  /root/pretrain
COPY ./data/torch  /root/.cache/torch
COPY ./data/huggingface/hub/models--laion--CLIP-ViT-bigG-14-laion2B-39B-b160k  /root/.cache/huggingface/hub/models--laion--CLIP-ViT-bigG-14-laion2B-39B-b160k


COPY ./data/filebrowser  /opt/filebrowser

ENV LD_PRELOAD=libtcmalloc.so

EXPOSE 22
EXPOSE 8889
EXPOSE 6860
EXPOSE 6006
EXPOSE 8080

STOPSIGNAL SIGINT
ENTRYPOINT ["/bin/bash", "/opt/server_app.sh"]
