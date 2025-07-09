#!/usr/bin/env bash
if [ -f "/etc/debian_version" ]; then
    apt update
    apt install -y wget lsb-release software-properties-common gnupg
    wget https://apt.llvm.org/llvm.sh
    chmod +x llvm.sh
    ./llvm.sh 17
    apt install -y libpolly-17-dev libzstd-dev
    export LLVM_DIR=/usr/lib/llvm-17
    export LLVM_SYS_170_PREFIX=/usr/lib/llvm-17
else
    # must be AlmaLinux 8. You can install the llvm library with llvm-libs-17.0.6,
    # but this doesn't come with llvm-config, so we have to build it from source. 
    yum update -y
    git clone --depth 1 https://github.com/llvm/llvm-project
    cd llvm-project
    mkdir build
    cd build
    cmake -DCMAKE_BUILD_TYPE=Release ../llvm \
          -DLLVM_ENABLE_PROJECTS="polly"
    cmake --build .  --target install
    export LLVM_DIR=/usr/lib64
    export LLVM_SYS_170_PREFIX=/usr/lib64
fi
ls -l $LLVM_DIR


