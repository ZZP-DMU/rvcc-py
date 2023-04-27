#!/bin/zsh

RISCV="/home/ZZP/workspace/src/rvcc/rvcc_doc/rvcc-course/riscv/"


assert() {
    expected="$1"
    input="$2"

    ./main.py "$input" >./playground/tmp.s ||exit

    riscv64-unknown-linux-gnu-gcc -static -o ./playground/tmp ./playground/tmp.s  ||exit

    $RISCV/bin/qemu-riscv64 -L $RISCV/sysroot ./playground/tmp 

    actual="$?"

    if [ "$actual" = "$expected" ];then
        echo "$input => $actual"
    else 
        echo "$input => $expected, but got $actual"
        exit 1
    fi


}

assert "-13" "12- 9*3+ (8-4)/2"

echo ok