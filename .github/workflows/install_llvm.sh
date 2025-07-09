#!/usr/bin/env bash
if [ -f "/etc/debian_version" ]; then
    apt update
    apt install -y wget lsb_core
    wget https://apt.llvm.org/llvm.sh
    chmod +x llvm.sh
    ./llvm.sh 17
    apt install -y libpolly-17-dev libzstd-dev
    export LLVM_DIR=/usr/lib/llvm-17
    export LLVM_SYS_170_PREFIX=/usr/lib/llvm-17
else
    yum update -y
    yum -y install llvm-libs-17.0.6
    export LLVM_DIR=/usr/lib/clang/17
    export LLVM_SYS_170_PREFIX=/usr/lib/clang/17
fi
ls -l $LLVM_DIR


