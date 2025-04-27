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

- 训练Flux.1大模型
```bash
/home/1000/.local/bin/accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision bf16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 /app/sd-scripts/flux_train.py --config_file /app/outputs/config_dreambooth-20250427-085645.toml
```

- 训练Flux.1 lora
```bash
/home/1000/.local/bin/accelerate launch --dynamo_backend no --dynamo_mode default --mixed_precision bf16 --num_processes 1 --num_machines 1 --num_cpu_threads_per_process 2 /app/sd-scripts/flux_train_network.py --config_file /app/outputs/config_lora-20250427-101924.toml
```


- 训练Flux.1 lora 命令行启动训练
    ```
    bash train_flux_lora.sh
    ```

    写入脚本
    ```bash
    cat <<'EOF' > train_flux_lora.sh
    #!/bin/bash

    /home/1000/.local/bin/accelerate launch \
        --dynamo_backend=tensorrt \
        --dynamo_mode=default \
        --mixed_precision=fp16 \
        --num_processes=1 \
        --num_machines=1 \
        --num_cpu_threads_per_process=2 \
        /app/sd-scripts/flux_train_network.py \
        --pretrained_model_name_or_path=/app/models/unet/flux1-dev-fp8.safetensors \
        --t5xxl=/app/models/clip/t5xxl_fp16.safetensors \
        --clip_l=/app/models/clip/clip_l.safetensors \
        --ae=/app/models/vae/ae.safetensors \
        --train_data_dir=/app/data/train/img \
        --logging_dir=/app/logs \
        --output_dir=/app/outputs \
        --output_name=qili \
        --train_batch_size=2 \
        --bucket_no_upscale \
        --bucket_reso_steps=64 \
        --cache_latents \
        --cache_latents_to_disk \
        --caption_extension=".txt" \
        --clip_skip=1 \
        --discrete_flow_shift=3.0 \
        --enable_bucket \
        --gradient_accumulation_steps=1 \
        --guidance_scale=3.5 \
        --huber_c=0.1 \
        --huber_scale=1 \
        --huber_schedule=snr \
        --loss_type=l2 \
        --unet_lr=0.0001 \
        --lr_scheduler=cosine_with_min_lr  \
        --lr_scheduler_num_cycles=2 \
        --lr_scheduler_power=1 \
        --lr_warmup_steps=0.1 \
        --lr_decay_steps=0.5 \
        --lr_scheduler_min_lr_ratio=0.1 \
        --max_bucket_reso=2048 \
        --max_data_loader_n_workers=0 \
        --max_grad_norm=1 \
        --max_timestep=1000 \
        --max_train_epochs=10 \
        --max_train_steps=10000 \
        --min_bucket_reso=256 \
        --mixed_precision=bf16 \
        --model_prediction_type=raw \
        --network_alpha=32 \
        --network_args="train_double_block_indices=all" \
        --network_args="train_single_block_indices=all" \
        --network_dim=32 \
        --network_module=networks.lora_flux \
        --network_train_unet_only \
        --optimizer_type=PagedAdamW8bit \
        --optimizer_args weight_decay=0.01 betas=0.9,0.95 \
        --prior_loss_weight=1 \
        --resolution=1024,1024 \
        --sample_prompts=/app/outputs/sample/prompt.txt \
        --sample_sampler=euler_a \
        --save_every_n_epochs=1 \
        --save_model_as=safetensors \
        --save_precision=bf16 \
        --t5xxl_max_token_length=512 \
        --timestep_sampling=sigma \
        --wandb_run_name=qili \
        --xformers
    EOF

    ```