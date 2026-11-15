import csv
import os
import matplotlib.pyplot as plt

def generate_trace_O0():
    """asm_O0.s dosyasinin birebir bellek veri erisim izini (load/store) uretir."""
    trace = []
    sira = 1

    def add_ref(rw, addr, size, c_line, is_stack):
        nonlocal sira
        trace.append((sira, rw, f"0x{addr:08x}", size, c_line, is_stack))
        sira += 1

    # Part 1: main prologue ve baslangic atamalari (s0 = 0x7ffffff0, sp = 0x7fffffc0)
    add_ref("W", 0x7fffffec, 4, 14, 1)  # sw ra, 44(sp)
    add_ref("W", 0x7fffffe8, 4, 14, 1)  # sw s0, 40(sp)
    add_ref("W", 0x7fffffdc, 4, 15, 1)  # sw a5, -20(s0) -> x = SID
    add_ref("W", 0x7fffffc4, 4, 16, 1)  # sw a5, -44(s0) -> N = 43
    add_ref("W", 0x7fffffd8, 4, 18, 1)  # sw a5, -24(s0) -> K = SID % 256
    add_ref("R", 0x7fffffd8, 4, 19, 1)  # lw a5, -24(s0) -> if (K == 0)
    add_ref("W", 0x7fffffd4, 4, 23, 1)  # sw zero, -28(s0) -> i = 0 (Loop 1)

    # Part 2: Loop 1 (.L5 ve .L6, i = 0..42)
    for i in range(43):
        add_ref("R", 0x7fffffd4, 4, 23, 1)              # .L5: lw a4, -28(s0) (i)
        add_ref("R", 0x7fffffc4, 4, 23, 1)              # .L5: lw a5, -44(s0) (N)
        add_ref("R", 0x7fffffdc, 4, 24, 1)              # .L6: lw a4, -20(s0) (x)
        add_ref("W", 0x7fffffdc, 4, 24, 1)              # .L6: sw a5, -20(s0) (x)
        add_ref("R", 0x7fffffdc, 4, 25, 1)              # .L6: lw a5, -20(s0) (x)
        add_ref("W", 0x7fffffc0, 4, 25, 1)              # .L6: sw a5, -48(s0) (val)
        add_ref("R", 0x7fffffd4, 4, 26, 1)              # .L6: lw a5, -28(s0) (i)
        add_ref("R", 0x7fffffc0, 4, 26, 1)              # .L6: lw a4, -48(s0) (val)
        add_ref("W", 0x10000000 + 4 * i, 4, 26, 0)      # .L6: sw a4, 0(a5) (v[i])
        add_ref("R", 0x7fffffd4, 4, 27, 1)              # .L6: lw a5, -28(s0) (i)
        add_ref("R", 0x7fffffc0, 4, 27, 1)              # .L6: lw a4, -48(s0) (val)
        add_ref("W", 0x100000ac + 4 * i, 4, 27, 0)      # .L6: sw a4, 0(a5) (orig_v[i])
        add_ref("R", 0x7fffffd4, 4, 23, 1)              # .L6: lw a5, -28(s0) (i)
        add_ref("W", 0x7fffffd4, 4, 23, 1)              # .L6: sw a5, -28(s0) (i++)
    # Loop 1 bitis kontrolu (i = 43)
    add_ref("R", 0x7fffffd4, 4, 23, 1)
    add_ref("R", 0x7fffffc4, 4, 23, 1)

    # Part 3: Loop 2 oncesi c = 0, i = 0
    add_ref("W", 0x7fffffd0, 4, 30, 1)  # sw zero, -32(s0) (c = 0)
    add_ref("W", 0x7fffffcc, 4, 31, 1)  # sw zero, -36(s0) (i = 0)

    # Part 4: Loop 2 (.L7, .L8 ve rotl, i = 0..42)
    for i in range(43):
        add_ref("R", 0x7fffffcc, 4, 31, 1)              # .L7: lw a4, -36(s0) (i)
        add_ref("R", 0x7fffffc4, 4, 31, 1)              # .L7: lw a5, -44(s0) (N)
        add_ref("R", 0x7fffffcc, 4, 32, 1)              # .L8: lw a5, -36(s0) (i)
        add_ref("R", 0x10000000 + 4 * i, 4, 32, 0)      # .L8: lw a4, 0(a5) (v[i])
        add_ref("R", 0x7fffffd8, 4, 32, 1)              # .L8: lw a5, -24(s0) (K)
        add_ref("R", 0x7fffffcc, 4, 32, 1)              # .L8: lw a5, -36(s0) (i)
        add_ref("W", 0x10000000 + 4 * i, 4, 32, 0)      # .L8: sw a4, 0(a5) (v[i])
        add_ref("R", 0x7fffffd0, 4, 33, 1)              # .L8: lw a0, -32(s0) (c)
        # rotl fonksiyon cagrisi
        add_ref("W", 0x7fffffbc, 4, 10, 1)              # rotl: sw s0, 28(sp)
        add_ref("W", 0x7fffffac, 4, 10, 1)              # rotl: sw a0, -20(s0)
        add_ref("W", 0x7fffffa8, 4, 10, 1)              # rotl: sw a1, -24(s0)
        add_ref("R", 0x7fffffac, 4, 11, 1)              # rotl: lw a5, -20(s0)
        add_ref("R", 0x7fffffa8, 4, 11, 1)              # rotl: lw a4, -24(s0)
        add_ref("R", 0x7fffffa8, 4, 11, 1)              # rotl: lw a3, -24(s0)
        add_ref("R", 0x7fffffbc, 4, 12, 1)              # rotl: lw s0, 28(sp)
        # rotl donusu (.L8 devam)
        add_ref("R", 0x7fffffcc, 4, 33, 1)              # .L8: lw a5, -36(s0) (i)
        add_ref("R", 0x10000000 + 4 * i, 4, 33, 0)      # .L8: lw a5, 0(a5) (v[i])
        add_ref("W", 0x7fffffd0, 4, 33, 1)              # .L8: sw a5, -32(s0) (c)
        add_ref("R", 0x7fffffcc, 4, 31, 1)              # .L8: lw a5, -36(s0) (i)
        add_ref("W", 0x7fffffcc, 4, 31, 1)              # .L8: sw a5, -36(s0) (i++)
    # Loop 2 bitis kontrolu (i = 43)
    add_ref("R", 0x7fffffcc, 4, 31, 1)
    add_ref("R", 0x7fffffc4, 4, 31, 1)

    # Part 5: checksum = c ve Loop 3 oncesi i = 0
    add_ref("R", 0x7fffffd0, 4, 35, 1)  # lw a4, -32(s0) (c)
    add_ref("W", 0x10000158, 4, 35, 0)  # sw a4, 344(a5) (checksum)
    add_ref("W", 0x7fffffc8, 4, 37, 1)  # sw zero, -40(s0) (i = 0)

    # Part 6: Loop 3 (.L9, .L11, .L10, i = 0..42)
    for i in range(43):
        add_ref("R", 0x7fffffc8, 4, 37, 1)              # .L9: lw a4, -40(s0) (i)
        add_ref("R", 0x7fffffc4, 4, 37, 1)              # .L9: lw a5, -44(s0) (N)
        add_ref("R", 0x7fffffc8, 4, 38, 1)              # .L11: lw a5, -40(s0) (i)
        add_ref("R", 0x10000000 + 4 * i, 4, 38, 0)      # .L11: lw a4, 0(a5) (v[i])
        add_ref("R", 0x7fffffd8, 4, 38, 1)              # .L11: lw a5, -24(s0) (K)
        add_ref("R", 0x7fffffc8, 4, 38, 1)              # .L11: lw a5, -40(s0) (i)
        add_ref("W", 0x10000000 + 4 * i, 4, 38, 0)      # .L11: sw a4, 0(a5) (v[i])
        add_ref("R", 0x7fffffc8, 4, 40, 1)              # .L11: lw a5, -40(s0) (i)
        add_ref("R", 0x10000000 + 4 * i, 4, 40, 0)      # .L11: lw a4, 0(a5) (v[i])
        add_ref("R", 0x7fffffc8, 4, 40, 1)              # .L11: lw a5, -40(s0) (i)
        add_ref("R", 0x100000ac + 4 * i, 4, 40, 0)      # .L11: lw a5, 0(a5) (orig_v[i])
        add_ref("R", 0x7fffffc8, 4, 37, 1)              # .L10: lw a5, -40(s0) (i)
        add_ref("W", 0x7fffffc8, 4, 37, 1)              # .L10: sw a5, -40(s0) (i++)
    # Loop 3 bitis kontrolu (i = 43)
    add_ref("R", 0x7fffffc8, 4, 37, 1)
    add_ref("R", 0x7fffffc4, 4, 37, 1)

    # Part 7: main epilogue
    add_ref("R", 0x7fffffec, 4, 46, 1)  # lw ra, 44(sp)
    add_ref("R", 0x7fffffe8, 4, 46, 1)  # lw s0, 40(sp)

    return trace

def simulate_cache(trace, cache_size=128, line_size=8, ways=4):
    num_lines = cache_size // line_size
    num_sets = num_lines // ways
    offset_bits = line_size.bit_length() - 1
    set_bits = num_sets.bit_length() - 1

    sets = [[] for _ in range(num_sets)]
    seen_blocks = set()
    hits = 0
    misses = 0
    writebacks = 0
    first_30_log = []

    for idx, (sira, rw, addr_str, size, c_line, is_stack) in enumerate(trace):
        addr = int(addr_str, 16)
        word_off = addr & ((1 << offset_bits) - 1)
        set_idx = (addr >> offset_bits) & ((1 << set_bits) - 1) if set_bits > 0 else 0
        tag = addr >> (offset_bits + set_bits)
        block_id = addr >> offset_bits

        was_seen_before = block_id in seen_blocks
        seen_blocks.add(block_id)

        cache_set = sets[set_idx]
        hit_entry = None
        for entry in cache_set:
            if entry["tag"] == tag:
                hit_entry = entry
                break

        evicted_str = "Yok"
        if hit_entry is not None:
            hits += 1
            hm = "Hit"
            if rw == "W":
                hit_entry["dirty"] = 1
            cache_set.remove(hit_entry)
            cache_set.insert(0, hit_entry)
        else:
            misses += 1
            hm = "Miss"
            if len(cache_set) == ways:
                lru_entry = cache_set.pop()
                evicted_str = f"Tag 0x{lru_entry['tag']:07x} (D={lru_entry['dirty']})"
                if lru_entry["dirty"] == 1:
                    writebacks += 1
            new_entry = {"tag": tag, "dirty": 1 if rw == "W" else 0}
            cache_set.insert(0, new_entry)

        if idx < 30:
            first_30_log.append({
                "sira": sira, "rw": rw, "addr": addr_str,
                "tag": f"0x{tag:07x}", "set": set_idx, "word": word_off,
                "hm": hm, "evicted": evicted_str,
                "seen": "Evet" if was_seen_before else "Hayır"
            })

    return {
        "hits": hits, "misses": misses,
        "H": hits / len(trace),
        "writebacks": writebacks,
        "first_30": first_30_log
    }

if __name__ == "__main__":
    trace = generate_trace_O0()

    # 1. trace.csv kaydet
    with open("trace.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["sira", "RW", "adres_hex", "boyut", "c_satiri", "stack_mi"])
        writer.writerows(trace)

    # 2. main_v2.c kaydet (Adim 4g: Loop 2 ve Loop 3 birlestirilmis surum)
    main_v2_code = """// Ad Soyad: Metehan Bayrak | SID: 5001240044 | Görev: G3 (4g Loop Fusion Sürümü)

const int SID = 1240044;

unsigned int v[43];
unsigned int orig_v[43];
unsigned int checksum = 0;
int decrypt_ok = 1;

unsigned int rotl(unsigned int val, int shift) {
    return (val << shift) | (val >> (32 - shift));
}

int main() {
    unsigned int x = SID;
    int N = 43;
    
    unsigned int K = SID % 256;
    if (K == 0) {
        K = 0xA5;
    }

    for (int i = 0; i < N; i++) {
        x = 1664525 * x + 1013904223;
        unsigned int val = ((x >> 16) % 26) + 65;
        v[i] = val;
        orig_v[i] = val;
    }

    unsigned int c = 0;
    for (int i = 0; i < N; i++) {
        v[i] = v[i] ^ K;
        c = rotl(c, 1) + v[i];
        v[i] = v[i] ^ K;
        if (v[i] != orig_v[i]) {
            decrypt_ok = 0;
        }
    }
    checksum = c;

    return 0;
}
"""
    with open("main_v2.c", "w", encoding="utf-8") as f:
        f.write(main_v2_code)

    # 3. Simulasyonlari calistir ve cache_sim_output.txt kaydet
    res_full = simulate_cache(trace, 128, 8, 4)
    res_30 = simulate_cache(trace[:30], 128, 8, 4)

    mappings = [("Direct", 1), ("2-way", 2), ("4-way", 4), ("Fully Assoc", 16)]
    map_results = [(name, simulate_cache(trace, 128, 8, w)) for name, w in mappings]

    line_sizes = [(8, 4), (16, 4), (32, 4), (64, 2)]
    line_results = [(ls, simulate_cache(trace, 128, ls, w)) for ls, w in line_sizes]

    with open("cache_sim_output.txt", "w", encoding="utf-8") as f:
        f.write(f"Toplam Referans: {len(trace)}\n")
        f.write(f"Ilk 30 -> Hit: {res_30['hits']}, Miss: {res_30['misses']}, H: {res_30['H']:.4f}, WB: {res_30['writebacks']}\n")
        f.write(f"Tum Iz -> Hit: {res_full['hits']}, Miss: {res_full['misses']}, H: {res_full['H']:.4f}, WB: {res_full['writebacks']}\n")

    # 4. 4e Grafigini uret (SS/M4_4e_grafik.png)
    os.makedirs("SS", exist_ok=True)
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11, 4.5))

    m_names = [m[0] for m in map_results]
    m_h = [m[1]["H"] * 100 for m in map_results]
    ax1.plot(m_names, m_h, marker="o", linewidth=2, color="#1f77b4")
    ax1.set_title("Sabit Boyut (128B) & Line (8B) - Mapping vs Hit Ratio")
    ax1.set_ylabel("Hit Ratio H (%)")
    ax1.set_ylim(85, 100)
    ax1.grid(True, linestyle="--", alpha=0.6)
    for i, val in enumerate(m_h):
        ax1.annotate(f"%{val:.2f}", (m_names[i], val), textcoords="offset points", xytext=(0, 8), ha="center")

    l_names = [f"{ls[0]} B" for ls in line_results]
    l_h = [ls[1]["H"] * 100 for ls in line_results]
    ax2.plot(l_names, l_h, marker="s", linewidth=2, color="#d62728")
    ax2.set_title("Sabit Boyut (128B) & 4-Way - Line Boyutu vs Hit Ratio")
    ax2.set_ylabel("Hit Ratio H (%)")
    ax2.set_ylim(80, 100)
    ax2.grid(True, linestyle="--", alpha=0.6)
    for i, val in enumerate(l_h):
        ax2.annotate(f"%{val:.2f}", (l_names[i], val), textcoords="offset points", xytext=(0, 8), ha="center")

    plt.tight_layout()
    plt.savefig("SS/M4_4e_grafik.png", dpi=200)
    print("Tum dosyalar (trace.csv, main_v2.c, cache_sim_output.txt, SS/M4_4e_grafik.png) basariyla uretildi!")