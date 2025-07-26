# 📦 NATConfigurator
NATConfigurator adalah aplikasi GUI berbasis Linux yang dirancang untuk mempermudah konfigurasi NAT (Network Address Translation) secara otomatis, khususnya untuk keperluan integrasi dengan GNS3 dan VirtualBox. Aplikasi ini ditujukan bagi pengguna yang sering membangun lab jaringan virtual di Linux.

🚀 Fitur Utama

    ✅ Deteksi koneksi internet secara otomatis
    ✅ Pemilihan interface sumber internet yang akurat (bukan asal ambil eth0 atau wlan0)
    ✅ Mode otomatis dan mode kustom jika terdapat lebih dari satu koneksi
    ✅ Kompatibel dengan tap0 untuk GNS3
    ✅ Bisa digunakan dengan VirtualBox (bridging, NAT, dan tap)
🧭 Cara Menggunakan NATConfigurator

Jalankan aplikasi:

    ./launch.sh

Pilih mode kerja:

    Klik GNS3 untuk mengaktifkan NAT bagi lab jaringan GNS3 (dengan interface tap0).

    Klik VirtualBox jika hanya menggunakan mesin virtual VirtualBox.

Pilih sumber koneksi internet:

    NATConfigurator akan mendeteksi interface yang terhubung ke internet (misalnya wlan0, eth0, enpXsY, dll).

    Pilih interface yang benar sesuai dengan koneksi aktif.

Klik tombol ACTIVATE:

    NAT akan diaktifkan secara otomatis.

    GNS3/VirtualBox akan langsung bisa terhubung ke internet via interface yang dipilih.

Untuk membatalkan konfigurasi NAT:

    Klik tombol DEACTIVATE atau RESTORE.

    Ini akan menghapus aturan NAT dan mengembalikan pengaturan sistem ke kondisi awal.

⚠️ Catatan

    Tidak perlu menjalankan dengan sudo, karena launch.sh sudah menangani perizinan otomatis.

    Konfigurasi NAT tidak akan mengganggu jaringan utama sistem operasi.

    Sangat cocok digunakan untuk keperluan simulasi jaringan secara praktis di Linux.
