.data
v:
        .zero   172
orig_v:
        .zero   172
checksum:
        .zero   4
decrypt_ok:
        .word   1
        .text
        j main
rotl:
        addi    sp,sp,-32
        sw      s0,28(sp)
        addi    s0,sp,32
        sw      a0,-20(s0)
        sw      a1,-24(s0)
        lw      a5,-20(s0)
        lw      a4,-24(s0)
        sll     a4,a5,a4
        lw      a3,-24(s0)
        neg     a3,a3
        andi    a3,a3,31
        srl     a5,a5,a3
        or      a5,a5,a4
        mv      a0,a5
        lw      s0,28(sp)
        addi    sp,sp,32
        jr      ra
main:
        addi    sp,sp,-48
        sw      ra,44(sp)
        sw      s0,40(sp)
        addi    s0,sp,48
        li      a5,1241088
        addi    a5,a5,-1044
        sw      a5,-20(s0)
        li      a5,43
        sw      a5,-44(s0)
        li      a5,236
        sw      a5,-24(s0)
        lw      a5,-24(s0)
        bne     a5,zero,.L4
        li      a5,165
        sw      a5,-24(s0)
.L4:
        sw      zero,-28(s0)
        j       .L5
.L6:
        lw      a4,-20(s0)
        li      a5,1662976
        addi    a5,a5,1549
        mul     a4,a4,a5
        li      a5,1013903360
        addi    a5,a5,863
        add     a5,a4,a5
        sw      a5,-20(s0)
        lw      a5,-20(s0)
        srli    a4,a5,16
        li      a5,26
        remu    a5,a4,a5
        addi    a5,a5,65
        sw      a5,-48(s0)
        lui     a5,%hi(v)
        addi    a4,a5,%lo(v)
        lw      a5,-28(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a4,-48(s0)
        sw      a4,0(a5)
        lui     a5,%hi(orig_v)
        addi    a4,a5,%lo(orig_v)
        lw      a5,-28(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a4,-48(s0)
        sw      a4,0(a5)
        lw      a5,-28(s0)
        addi    a5,a5,1
        sw      a5,-28(s0)
.L5:
        lw      a4,-28(s0)
        lw      a5,-44(s0)
        blt     a4,a5,.L6
        sw      zero,-32(s0)
        sw      zero,-36(s0)
        j       .L7
.L8:
        lui     a5,%hi(v)
        addi    a4,a5,%lo(v)
        lw      a5,-36(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a4,0(a5)
        lw      a5,-24(s0)
        xor     a4,a4,a5
        lui     a5,%hi(v)
        addi    a3,a5,%lo(v)
        lw      a5,-36(s0)
        slli    a5,a5,2
        add     a5,a3,a5
        sw      a4,0(a5)
        li      a1,1
        lw      a0,-32(s0)
        call    rotl
        mv      a3,a0
        lui     a5,%hi(v)
        addi    a4,a5,%lo(v)
        lw      a5,-36(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a5,0(a5)
        add     a5,a3,a5
        sw      a5,-32(s0)
        lw      a5,-36(s0)
        addi    a5,a5,1
        sw      a5,-36(s0)
.L7:
        lw      a4,-36(s0)
        lw      a5,-44(s0)
        blt     a4,a5,.L8
        lui     a5,%hi(checksum)
        lw      a4,-32(s0)
        sw      a4,%lo(checksum)(a5)
        sw      zero,-40(s0)
        j       .L9
.L11:
        lui     a5,%hi(v)
        addi    a4,a5,%lo(v)
        lw      a5,-40(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a4,0(a5)
        lw      a5,-24(s0)
        xor     a4,a4,a5
        lui     a5,%hi(v)
        addi    a3,a5,%lo(v)
        lw      a5,-40(s0)
        slli    a5,a5,2
        add     a5,a3,a5
        sw      a4,0(a5)
        lui     a5,%hi(v)
        addi    a4,a5,%lo(v)
        lw      a5,-40(s0)
        slli    a5,a5,2
        add     a5,a4,a5
        lw      a4,0(a5)
        lui     a5,%hi(orig_v)
        addi    a3,a5,%lo(orig_v)
        lw      a5,-40(s0)
        slli    a5,a5,2
        add     a5,a3,a5
        lw      a5,0(a5)
        beq     a4,a5,.L10
        lui     a5,%hi(decrypt_ok)
        sw      zero,%lo(decrypt_ok)(a5)
.L10:
        lw      a5,-40(s0)
        addi    a5,a5,1
        sw      a5,-40(s0)
.L9:
        lw      a4,-40(s0)
        lw      a5,-44(s0)
        blt     a4,a5,.L11
        li      a5,0
        mv      a0,a5
        lw      ra,44(sp)
        lw      s0,40(sp)
        addi    sp,sp,48
        li a7, 10
        ecall