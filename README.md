# Kalkulator HPM Bijih Nikel 2026

Kalkulator interaktif untuk menghitung **Harga Patokan Mineral (HPM) Bijih Nikel** berdasarkan formula baru **Kepmen ESDM No. 144 Tahun 2026**.

🔗 **Live site:** [sandro-888.github.io/hpm-nikel-calculator](https://sandro-888.github.io/hpm-nikel-calculator/)

## Fitur

- Simulasi HPM untuk **Limonite** dan **Saprolite**
- Formula baru dengan komponen **mineral ikutan** (Besi, Kobalt, Krom)
- Corrective Factor otomatis sesuai ketentuan Kepmen 144/2026
- Perbandingan dengan HPM lama (Kepmen 268/2025)
- HMA **diperbarui otomatis** setiap hari via GitHub Actions dari [minerba.esdm.go.id](https://www.minerba.esdm.go.id/harga_acuan)
- **4 tab grafik interaktif:**
  - **HPM vs Market** — perbandingan HPM New/Old vs harga pasar, dari Limonite ke Saprolite dalam satu grafik
  - **Fe Sensitivity** — sensitivitas HPM terhadap kadar Fe (20%–40%), dengan highlight threshold Fe ≤ 35%
  - **Co Sensitivity** — sensitivitas HPM terhadap kadar Co (0.01%–0.10%), dengan highlight threshold Co ≥ 0.05%
- Tombol **Copy Result** untuk salin hasil kalkulasi
- Dark/Light mode toggle
- Responsive — bisa diakses di mobile

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

1. Pilih tipe ore: **Limonite** atau **Saprolite**
2. Input kadar mineral (Ni, Fe, Co, Cr) dan Moisture Content
3. Hasil HPM otomatis terhitung
4. Gunakan tab grafik untuk analisis sensitivitas

Tidak perlu install apapun — cukup buka di browser atau akses via link di atas.

## Auto-Update HMA

HMA diperbarui otomatis setiap hari pukul **08:00 WIB** via GitHub Actions. Script `update_hma.py` melakukan scraping dari halaman resmi minerba.esdm.go.id dan hanya melakukan commit jika ada perubahan data.

## Referensi

- [Harga Mineral Acuan (HMA)](https://www.minerba.esdm.go.id/harga_acuan)
- Kepmen ESDM No. 144 Tahun 2026
- Kepmen ESDM No. 268 Tahun 2025 (formula lama, untuk perbandingan)

## Disclaimer

Kalkulator ini dibuat untuk keperluan simulasi dan referensi. Untuk keperluan resmi, selalu gunakan data dan formula dari Direktorat Jenderal Mineral dan Batubara, Kementerian ESDM.

## Credits

Created by [Sandro Sirait](https://www.linkedin.com/in/sandrosirait/) with the help of AI tools.
