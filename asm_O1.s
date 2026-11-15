.data
v:
        .zero   172
orig_v:
        .zero   172
checksum:
        .zero   4
decrypt_ok:
        .word   1
SID:
        .word   1240044

.text
.globl main
_start:
        j       main

rotl:
        sll     a5, a0, a1
        neg     a1, a1
        srl     a0, a0, a1
        or      a0, a0, a5
        ret

main:
        lui     a2, 0x10000
        addi    a4, a2, 0
        addi    a1, a4, 172
        mv      a0, a1
        mv      a6, a1
        addi    a2, a2, 0
        li      a3, 1241088
        addi    a3, a3, -1044
        li      t1, 1662976
        addi    t1, t1, 1549
        li      a7, 1013903360
        addi    a7, a7, 863
        li      t3, 26

.L3:
        mul     a3, a3, t1
        add     a3, a3, a7
        srli    a5, a3, 16
        remu    a5, a5, t3
        addi    a5, a5, 65
        sw      a5, 0(a2)
        sw      a5, 0(a6)
        addi    a2, a2, 4
        addi    a6, a6, 4
        bne     a2, a0, .L3

        mv      a3, a4
        li      a5, 0

.L4:
        lw      a2, 0(a3)
        xori    a2, a2, 236
        sw      a2, 0(a3)
        slli    a6, a5, 1
        srli    a5, a5, 31
        or      a5, a5, a6
        add     a5, a2, a5
        addi    a3, a3, 4
        bne     a3, a0, .L4

        lui     a3, 0x10000
        sw      a5, 344(a3)
        li      a2, 0
        li      a6, 1
        j       .L6

.L5:
        addi    a4, a4, 4
        addi    a1, a1, 4
        beq     a4, a0, .L11

.L6:
        lw      a5, 0(a4)
        xori    a5, a5, 236
        sw      a5, 0(a4)
        lw      a3, 0(a1)
        beq     a5, a3, .L5
        mv      a2, a6
        j       .L5

.L11:
        beq     a2, zero, .L7
        lui     a5, 0x10000
        sw      zero, 348(a5)

.L7:
        li      a0, 0
        ret