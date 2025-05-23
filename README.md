# kohya_ss-gui-docker

## 训练经验
- 精度选择bf16(mixed_precision,save_precision, full_bf16)
- 学习率 learning_rate = 2e-5，learning_rate_te = 2e-5
- train_batch_size = 8/16 不清楚官方推荐是多少

## 拉取镜像

这是kohya-ss提供的镜像，不再自己做镜像了
```
docker pull ghcr.io/bmaltais/kohya-ss-gui:latest
```

## FP8训练需要更新torch版本
```
pip uninstall torch torchvision torchaudio xformers -y
pip install torch==2.3.0 torchvision==0.18.0 torchaudio==2.3.0 --index-url https://download.pytorch.org/whl/cu121
pip install xformers==0.0.26.post1
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
    ```bash
    cp 国风数据-8000张-img_txt/* "img-10k/10_sks person"
    cp 国风数据-8000张/* "img-10k/10_sks person"
    cp 周愚昧-img_txt/* "img-10k/10_sks person" 
    cp 周愚昧-img/* "img-10k/10_sks person" 

    find "img-10k/10_sks person" -type f -name "*.txt" | wc -l
    find "img-10k/10_sks person" -type f -name "*.png" | wc -l
    ```
    
    ```
    /app/data/train/img
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

## Flux.1 funeting | lora 
- 训练Flux.1大模型
```bash
/home/1000/.local/bin/accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision bf16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 /app/sd-scripts/flux_train.py --config_file /app/outputs/config_dreambooth-20250427-085645.toml 2>&1 | tee outputs/logs.txt
```

- 训练Flux.1 lora
```bash
/home/1000/.local/bin/accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision bf16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 /app/sd-scripts/flux_train_network.py --config_file /app/outputs/config_lora-20250427-101924.toml 2>&1 | tee outputs/logs.txt
```

- 测试Lora
- 拷贝到comfyui
```bash
cp /dev/shm/workspace/kohya_ss-gui-docker/dataset/outputs/models/*.safetensors  /dev/shm/workspace/comfyui-docker/volumes/comfyui-dev/data/models/loras
```

- 融合Flux.1 lora
- 分别融合三个版本 bf16,fp16,fp8
```bash
cd /app/sd-scripts
/usr/local/bin/python3 /app/sd-scripts/networks/flux_merge_lora.py --flux_model /app/models/unet/flux1-dev.safetensors --save_precision bf16 --precision bf16 --save_to /app/outputs/merge_models/F.1-国风汉服-鹤羽谣-bf16.safetensors --loading_device cuda --working_device cuda --models /app/outputs/models/国风lora-img-13k-Adafactor-LR1e-4-B2-Dim128-000003.safetensors --ratios 1
/usr/local/bin/python3 /app/sd-scripts/networks/flux_merge_lora.py --flux_model /app/models/unet/flux1-dev.safetensors --save_precision fp16 --precision bf16 --save_to /app/outputs/merge_models/F.1-国风汉服-鹤羽谣-fp16.safetensors --loading_device cuda --working_device cuda --models /app/outputs/models/国风lora-img-13k-Adafactor-LR1e-4-B2-Dim128-000003.safetensors --ratios 1
/usr/local/bin/python3 /app/sd-scripts/networks/flux_merge_lora.py --flux_model /app/models/unet/flux1-dev.safetensors --save_precision fp8 --precision bf16 --save_to /app/outputs/merge_models/F.1-国风汉服-鹤羽谣-fp8.safetensors --loading_device cuda --working_device cuda --models /app/outputs/models/国风lora-img-13k-Adafactor-LR1e-4-B2-Dim128-000003.safetensors --ratios 1
```

- 拷贝到comfyui
```bash
cp /dev/shm/workspace/kohya_ss-gui-docker/dataset/outputs/merge_models/* /dev/shm/workspace/comfyui-docker/volumes/comfyui-dev/data/models/unet 
```

## SD3.5 funeting | lora 

- 训练SD3.5 lora
```bash
/home/1000/.local/bin/accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision bf16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 /app/sd-scripts/sd3_train_network.py --config_file /app/outputs/config_lora.toml 2>&1 | tee outputs/logs.txt
```