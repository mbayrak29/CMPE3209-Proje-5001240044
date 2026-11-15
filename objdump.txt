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
        addi    sp, sp, -32
        sw      s0, 28(sp)
        addi    s0, sp, 32
        sw      a0, -20(s0)
        sw      a1, -24(s0)
        lw      a5, -20(s0)
        lw      a4, -24(s0)
        sll     a4, a5, a4
        lw      a3, -24(s0)
        neg     a3, a3
        andi    a3, a3, 31
        srl     a5, a5, a3
        or      a5, a5, a4
        mv      a0, a5
        lw      s0, 28(sp)
        addi    sp, sp, 32
        jr      ra
main:
        addi    sp, sp, -48
        sw      ra, 44(sp)
        sw      s0, 40(sp)
        addi    s0, sp, 48
        lui     a5, 0x12f
        addi    a5, a5, -1044
        sw      a5, -20(s0)
        addi    a5, zero, 43
        sw      a5, -44(s0)
        lui     a5, 0x12f
        addi    a5, a5, -1044
        andi    a5, a5, 255
        sw      a5, -24(s0)
        lw      a5, -24(s0)
        bne     a5, zero, .L4
        addi    a5, zero, 165
        sw      a5, -24(s0)
.L4:
        sw      zero, -28(s0)
        j       .L5
.L6:
        lw      a4, -20(s0)
        lui     a5, 0x196
        addi    a5, a5, 1549
        mul     a4, a4, a5
        lui     a5, 0x3c6ef
        addi    a5, a5, 863
        add     a5, a4, a5
        sw      a5, -20(s0)
        lw      a5, -20(s0)
        srli    a4, a5, 16
        addi    a5, zero, 26
        remu    a5, a4, a5
        addi    a5, a5, 65
        sw      a5, -48(s0)
        lui     a5, 0x10000
        addi    a4, a5, 0
        lw      a5, -28(s0)
        slli    a5, a5, 2
        add     a5, a4, a5
        lw      a4, -48(s0)
        sw      a4, 0(a5)
        lui     a5, 0x10000
        addi    a4, a5, 172
        lw      a5, -28(s0)
        slli    a5, a5, 2
        add     a5, a4, a5
        lw      a4, -48(s0)
        sw      a4, 0(a5)
        lw      a5, -28(s0)
        addi    a5, a5, 1
        sw      a5, -28(s0)
.L5:
        lw      a4, -28(s0)
        lw      a5, -44(s0)
        blt     a4, a5, .L6
        sw      zero, -32(s0)
        sw      zero, -36(s0)
        j       .L7
.L8:
        lui     a5, 0x10000
        addi    a4, a5, 0
        lw      a5, -36(s0)
        slli    a5, a5, 2
        add     a5, a4, a5
        lw      a4, 0(a5)
        lw      a5, -24(s0)
        xor     a4, a4, a5
        lui     a5, 0x10000
        addi    a3, a5, 0
        lw      a5, -36(s0)
        slli    a5, a5, 2
        add     a5, a3, a5
        sw      a4, 0(a5)
        addi    a1, zero, 1
        lw      a0, -32(s0)
        jal     ra, rotl
        mv      a3, a0
        lui     a5, 0x10000
        addi    a4, a5, 0
        lw      a5, -36(s0)
        slli    a5, a5, 2
        add     a5, a4, a5
        lw      a5, 0(a5)
        add     a5, a3, a5
        sw      a5, -32(s0)
        lw      a5, -36(s0)
        addi    a5, a5, 1
        sw      a5, -36(s0)
.L7:
        lw      a4, -36(s0)
        lw      a5, -44(s0)
        blt     a4, a5, .L8
        lui     a5, 0x10000
        lw      a4, -32(s0)
        sw      a4, 344(a5)
        sw      zero, -40(s0)
        j       .L9
.L11:
        lui     a5, 0x10000
        addi    a4, a5, 0
        lw      a5, -40(s0)
        slli    a5, a5, 2
        add     a5, a4, a5
        lw      a4, 0(a5)
        lw      a5, -24(s0)
        xor     a4, a4, a5
        lui     a5, 0x10000
        addi    a3, a5, 0
        lw      a5, -40(s0)
        slli    a5, a5, 2
        add     a5, a3, a5
        sw      a4, 0(a5)
        lui     a5, 0x10000
        addi    a4, a5, 0
        lw      a5, -40(s0)
        slli    a5, a5, 2
        add     a5, a4, a5
        lw      a4, 0(a5)
        lui     a5, 0x10000
        addi    a3, a5, 172
        lw      a5, -40(s0)
        slli    a5, a5, 2
        add     a5, a3, a5
        lw      a5, 0(a5)
        beq     a4, a5, .L10
        lui     a5, 0x10000
        sw      zero, 348(a5)
.L10:
        lw      a5, -40(s0)
        addi    a5, a5, 1
        sw      a5, -40(s0)
.L9:
        lw      a4, -40(s0)
        lw      a5, -44(s0)
        blt     a4, a5, .L11
        addi    a5, zero, 0
        mv      a0, a5
        lw      ra, 44(sp)
        lw      s0, 40(sp)
        addi    sp, sp, 48
        li      a7, 10
        ecall