# kohya_ss-gui-docker

## 拉取镜像

这是kohya-ss提供的镜像，不再自己做镜像了
```
docker pull ghcr.io/bmaltais/kohya-ss-gui:latest
```

## 配置
- 映射目录权限
    ```
    chmod -R 777 .cache dataset models
    ```

    容器启动时，使用的UID=1000,但是我的宿主机账户不是1000，也就是映射到容器时，无法访问.cache dataset models,所以直接把文件夹的权限打开。

    如果权限是同一个UID，这一步可以忽略。


- 修改docker-compose.yaml
    
    在docker-compose.yaml中添加一下内容，覆写dockerfile的启动命令：
    ```yaml
    command: ["python3", "kohya_gui.py", "--listen", "0.0.0.0", "--server_port", "7860", "--headless" "--noverify"]
    ```
    "--noverify" 启动服务时，不要再做python环境的检查

- 下载模型
    ```bash
    cd kohya_ss-gui-docker
    bash download_models.sh "$PWD"
    ```

- 数据结构
    
    训练数据 
    
    ```
    /app/data/img
    .
    └── 10_skm qili
        ├── 10x4096_4096x4096_flux.npz
        ├── 10x4096.jpg
        ├── 10x4096.txt
        ├── 11x4096_4096x4096_flux.npz
        ├── 11x4096.jpg
        ├── 11x4096.txt
        ├── 12x4096_4096x4096_flux.npz
        ├── 12x4096.jpg
        ├── 12x4096.txt
        ├── 13x4096_4096x4096_flux.npz
        ├── 13x4096.jpg
        ├── 13x4096.txt
        ├── 14x4096_4096x4096_flux.npz
    ```

    log输出目录
    ```
    /app/data/log
    ```

    lora模型输出目录
    ```
    /app/data/model
    ```

- 启动容器应用
    ```
    docker compose up
    ```
    端口号：62899


- 进入容器应用
    ```
    docker exec -it  kohya-ss-gui bash
    ```
    我不喜欢用界面，所以进入容器里面，直接命令行开启训练


- 启动训练
    ```
    bash train_flux_lora.sh
    ```