# Dockerfile
FROM ghcr.io/bmaltais/kohya-ss-gui:latest

USER root

# 创建一个1001的用户，名字叫 aigc
RUN useradd -u 1001 -m aigc

# 切换默认用户
USER aigc

# 默认执行命令（可选，看你的原镜像情况）
ENTRYPOINT ["python3", "kohya_gui.py", "--listen", "0.0.0.0", "--server_port", "7860", "--headless", "--noverify"]
