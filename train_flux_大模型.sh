/home/1000/.local/bin/accelerate launch \
    --dynamo_backend=tensorrt \
    --dynamo_mode=default \
    --mixed_precision=bf16 \
    --num_processes=1 \
    --num_machines=1 \
    --num_cpu_threads_per_process=2 \
    /app/sd-scripts/flux_train.py \

    --config_file  config_dreambooth.toml