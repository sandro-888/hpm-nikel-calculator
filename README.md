# Kalkulator HPM Bijih Nikel 2026

Kalkulator interaktif untuk menghitung **Harga Patokan Mineral (HPM) Bijih Nikel** berdasarkan formula baru **Kepmen ESDM No. 144 Tahun 2026**.

## Fitur

- Simulasi HPM untuk **Saprolite** dan **Limonite**
- Formula baru dengan komponen **mineral ikutan** (Besi, Kobalt, Krom)
- Corrective Factor otomatis sesuai ketentuan Kepmen 144/2026
- Perbandingan dengan HPM lama (Kepmen 268/2025)
- HMA mengacu pada data resmi [minerba.esdm.go.id](https://www.minerba.esdm.go.id/harga_acuan)
- Dark/Light mode toggle

## Formula (Kepmen 144/2026)

```
HPM = [(%Ni × CF Bijih Nikel × HMA Nikel)
     + (%Fe × CF Besi Ikutan × HMA Bijih Besi × 100)
     + (%Co × CF Kobalt Ikutan × HMA Kobalt)
     + (%Cr × CF Krom Ikutan × HMA Bijih Krom × 100)]
     × (1 − MC)
```

Satuan: **USD/WMT** (Wet Metric Ton). Berlaku sejak **15 April 2026**.

## Corrective Factors

| Component | CF | Ketentuan |
|---|---|---|
| Bijih Nikel | Variabel | Base 30% pada 1.6% Ni, ±1% per 0.1% Ni |
| Besi Ikutan | 30% | Berlaku jika Fe ≤ 35% |
| Kobalt Ikutan | 30% | Berlaku jika Co ≥ 0.05% |
| Krom Ikutan | 10% | Selalu berlaku |

## Cara Pakai

1. Pilih tipe ore: **Saprolite** atau **Limonite**
2. Input kadar mineral (Ni, Fe, Co, Cr) dan Moisture Content
3. Hasil HPM otomatis terhitung

Tidak perlu install apapun — cukup buka file `index.html` di browser.

## Referensi

- [PPT Sosialisasi Kepmen ESDM 144 Tahun 2026](https://www.minerba.esdm.go.id/)
- [Harga Mineral Acuan (HMA)](https://www.minerba.esdm.go.id/harga_acuan)
- Kepmen ESDM No. 268 Tahun 2025 (formula lama, untuk perbandingan)

## Disclaimer

Kalkulator ini dibuat untuk keperluan simulasi dan referensi. Untuk keperluan resmi, selalu gunakan data dan formula dari Direktorat Jenderal Mineral dan Batubara, Kementerian ESDM.

## Credits

Created by [Sandro Sirait](https://www.linkedin.com/in/sandrosirait/) with the help of AI tools.
