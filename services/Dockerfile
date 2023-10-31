FROM alpine/git:2.36.2 as download

COPY clone.sh /clone.sh
RUN . /clone.sh kohya-ss-gui https://github.com/bmaltais/kohya_ss.git  0ce88bba71c069b70ca7609efce3b7d4463c6dc0

FROM fmsunyh/kohya-ss-gui:21.8.9

ENV ROOT=/kohya-ss-gui
WORKDIR ${ROOT}

COPY --from=download /repositories/kohya-ss-gui ${ROOT}

# Install requirements
# COPY ./requirements.txt ./requirements_linux_docker.txt ./
# COPY ./setup/docker_setup.py ./setup.py

COPY ./entrypoint.sh ./entrypoint.sh

RUN --mount=type=cache,target=/root/.cache/pip \
   pip install -r ./requirements_linux_docker.txt  -i https://mirrors.aliyun.com/pypi/simple/ \
   pip install -r ./requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

# Replace pillow with pillow-simd
RUN python3 -m pip uninstall -y pillow && \
    CC="cc -mavx2" python3 -m pip install -U --force-reinstall pillow-simd

USER root

STOPSIGNAL SIGINT
ENV LD_PRELOAD=libtcmalloc.so
# ENV PATH="$PATH:/home/appuser/.local/bin"
ENTRYPOINT ["./entrypoint.sh"]
CMD python3 "./kohya_gui.py" ${CLI_ARGS} --listen 0.0.0.0 --server_port 7860
