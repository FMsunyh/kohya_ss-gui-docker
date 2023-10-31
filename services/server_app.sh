#!/bin/bash


# set -m

# /usr/sbin/sshd -D &
# jupyter lab --no-browser --port=8889 &

# fg %1


# Start the first process
/usr/sbin/sshd -D &

/root/miniconda3/bin/python3  -m lmdeploy.serve.gradio.app /root/internlm/models/turbomind-internlm-chat-20b-w4 --server_name 0.0.0.0 --server_port 7860 &

# Start the second process
# /opt/conda/envs/env/bin/jupyter lab  --allow-root --no-browser  --port=8889 --ip=0.0.0.0 &

# Wait for any process to exit
wait -n

# Exit with status of process that exited first
exit $?