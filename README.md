# kohya_ss-gui-docker

用于训练大模型和Lora模型的镜像


## 环境
- python 3.10 
- pytorch 2.0.1
- JupyterLab 4.0.6
- kuhya-ss-gui 22.1.0

## 拉取镜像
```bash
sudo docker pull registry.cn-shenzhen.aliyuncs.com/ai_base/kohya-ss-gui:22.1.0
```

## 启动容器
```bash
sudo docker run --gpus all -it  -p 8889:8889 9090:22 6006:6006 6860:6860 -v <local>/userdata/:/userdata/ --rm registry.cn-shenzhen.aliyuncs.com/ai_base/kohya-ss-gui:22.1.0
```
云端目录：/userdata/kohya-ss-gui

## SSH配置
用户名： root
密码：l6y#VJWJA4LGr1eI
端口：22

## jupyterlab配置
端口：8889
密码：hdn3tTBzKZ&g4IBM