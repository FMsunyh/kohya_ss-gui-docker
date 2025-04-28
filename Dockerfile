# Dockerfile
FROM ghcr.io/bmaltais/kohya-ss-gui:latest

USER root

# 用户参数
ARG UID=1001
ENV USERNAME=aigc

# 创建用户
RUN groupadd -g ${UID} ${USERNAME} && \
    useradd -l -u ${UID} -g ${UID} -m -s /bin/bash -N ${USERNAME}

# 将 /home/1000 目录和文件的所有者改为 1001 用户
# RUN mv /home/1000 /home/1001 && \
#     chown -R 1001:1001 /home/1001

# 修改 /app 目录的权限，确保新用户可以访问
RUN chown -R 1001:1001  /home/1000 /app

# 切换默认用户
USER aigc

# 默认执行命令（可选，看你的原镜像情况）
ENTRYPOINT ["python3", "kohya_gui.py", "--listen", "0.0.0.0", "--server_port", "7860", "--headless", "--noverify"]
