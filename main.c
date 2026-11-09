// Ad Soyad: Metehan Bayrak | SID: 5001240044 | Görev: G3 Mesaj Şifreleme ve Bütünlük

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
    }
    checksum = c;

    for (int i = 0; i < N; i++) {
        v[i] = v[i] ^ K;
        
        if (v[i] != orig_v[i]) {
            decrypt_ok = 0;
        }
    }

    return 0;
}