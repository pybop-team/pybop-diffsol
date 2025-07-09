!#/bin/bash
if [ -f "/etc/debian_version" ]; then
    apt install -y wget
    wget https://apt.llvm.org/llvm.sh
    chmod +x llvm.sh
    ./llvm.sh 17
    export LLVM_DIR=/usr/lib/llvm-17
    export LLVM_SYS_170_PREFIX=/usr/lib/llvm-17
else
    yum -y install llvm-libs-17.0.6
    export LLVM_DIR=/usr/lib/clang/17
    export LLVM_SYS_170_PREFIX=/usr/lib/clang/17
fi


