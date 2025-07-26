# butoh module
import socket
import subprocess
import sys
import os
from PySide6.QtCore import Qt, QEvent
from PySide6.QtWidgets import QApplication, QLabel, QDialog, QMessageBox
from PySide6.QtWidgets import QMessageBox
from qt_material import apply_stylesheet
from form import Ui_Dialog  # file .ui yang dikompilasi jadi Python

app = QApplication(sys.argv)
apply_stylesheet(app, theme='dark_teal.xml')

# iki tampilan dialogmu duduk main 
class MyDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.setFixedSize(self.size())  # kunci ukuran sesuai desain UI
        self.setWindowModality(Qt.ApplicationModal)
        self.ui.btnActivate.clicked.connect(self.handle_activate)
        self.ui.btnRestore.clicked.connect(self.on_restore_clicked)
        # self.ui.btnRestore.clicked.connect(self.handle_restore)
            
         # status default
        self.status = None

        # koneksi radio button ke handler
        self.ui.rdbVbox.toggled.connect(self.handle_radio)
        self.ui.rdbGns.toggled.connect(self.handle_radio) 

        # Siapkan label supaya kelihatan bisa diklik
        self.ui.lbAbout.setCursor(Qt.PointingHandCursor)
        # Pasang event filter ke label lbAbout
        self.ui.lbAbout.installEventFilter(self)

    def on_restore_clicked(self):
        self.handle_restore()
        self.reset_radio_buttons()
        
    def reset_radio_buttons(self):
        self.ui.rdbVbox.setAutoExclusive(False)
        self.ui.rdbGns.setAutoExclusive(False)

        self.ui.rdbVbox.setChecked(False)
        self.ui.rdbGns.setChecked(False)

        self.ui.rdbVbox.setAutoExclusive(True)
        self.ui.rdbGns.setAutoExclusive(True)


    #fungsi label untuk menampilkan text
    def eventFilter(self, obj, event):
        if obj == self.ui.lbAbout and event.type() == QEvent.MouseButtonRelease:
            self.about_text = """🐧 DISTRIBUSI LINUX YANG KOMPATIBEL

✅ Rekomendasi Distribusi:
- Ubuntu (Server & Desktop)
- Debian
- CentOS Stream
- Rocky Linux
- AlmaLinux
- Fedora
- Arch Linux
- Manjaro
- OpenSUSE
- Kali Linux (untuk keperluan eksperimen jaringan)

🔧 Distribusi Spesialis (Router/Gateway/Firewall):
- OpenWRT
- VyOS
- pfSense (berbasis FreeBSD, namun dengan fungsi serupa)

📌 Catatan:
Pastikan kernel mendukung modul TUN/TAP, serta memiliki iptables atau nftables yang aktif. 
Beberapa distro mungkin membutuhkan penyesuaian tambahan pada firewalld, ufw, atau 
network manager lainnya."""
            self.ui.txbDescription.setPlainText(self.about_text)
            return True
        return super().eventFilter(obj, event)

    # pengaturan window mode
    def setup_window_flags(self):
            self.setWindowFlag(Qt.WindowStaysOnTopHint)
            self.setWindowFlag(Qt.WindowMaximizeButtonHint, False)

    # cek ping gunakan socket bawaan python dari pada shell
    def check_internet(self, host="8.8.8.8", port=53, timeout=1):
        try:
            socket.setdefaulttimeout(timeout)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((host, port))
            sock.close()
            return True
        except OSError:
            return False
    
    def buka_btn_restore(self):
        self.ui.btnRestore.setEnabled(True)

    def tutup_btn_restore(self):
        self.ui.btnRestore.setEnabled(False)


    def showEvent(self, event):
        super(MyDialog, self).showEvent(event)

        if self.check_internet():
            self.ui.txbDescription.setPlainText("An internet connection is currently available on your device.\nPlease select the NAT configuration for the GNS/VirtualBox Host Adapter.")
        else:
            self.ui.txbDescription.setPlainText("No internet connection detected. Please check your connection.")

        script10 = "iptables-save -t nat | grep -- '-j MASQUERADE'"
        result10 = subprocess.run(script10, shell=True, capture_output=True, text=True)
        if result10.stdout.strip():
            self.ui.txbDescription.append("The application has detected a NAT configuration on your device.")
            self.buka_btn_restore()
        else:
            self.ui.txbDescription.append("No persistent NAT configuration found. You may proceed with the setup.")
        # radia action 
    
    def check_vboxnet0_exists(self):
        try:
            result = subprocess.run(
                ["VBoxManage", "list", "hostonlyifs"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )

            # Simpan output untuk digunakan di tempat lain (tampilan UI)
            self.last_hostonly_output = result.stdout.strip()
            interfaces = result.stdout.split("\n\n")
            for interface in interfaces:
                lines = interface.strip().splitlines()
                for line in lines:
                    if line.startswith("Name:") and "vboxnet0" in line:
                        return True
            return False

        except subprocess.CalledProcessError as e:
            self.last_hostonly_output = f"Unable to run VBoxManage:\n{e.stderr.strip()}"
            return False

    # fungsi update status dan deskripsi bersamaan
    def update_status_and_description(self):
        guideText = []  # <-- inisialisasi awal, penting!
        if self.ui.rdbGns.isChecked() or self.ui.rdbVbox.isChecked():
            self.status = 1 if self.ui.rdbGns.isChecked() else 2
            self.load_interfaces()

            # status 1 langsung load interface dan tampilkan pesan
            if self.status == 1:
                target = "GNS3"
                guideText = [
                    f"You have selected the NAT configuration for connecting to {target}.",
                    "Please select an interface in the bottom-left corner.",
                    "Choose the interface that provides internet access on your device."

                ]
            else:  # self.status == 2 cek dulu vboxnet cegah sebelum error
                if not self.check_vboxnet0_exists():  # Panggil fungsi pengecekan
                    guideText = [
                        "Interface 'vboxnet0' was not found.",
                        "Please create it first using VBoxManage or through the VirtualBox GUI.",
                        "Once created, reselect the configuration type above."
                    ]
                else: #jika tidak ada error tampilkan seperti text seperti status 1
                    target = "Vboxnet"
                    guideText = [
                        f"You have selected the NAT configuration to connect to {target}.",
                        "Please select the interface located in the bottom-left corner.",
                        "This should be the interface that provides internet access on your device."

                    ]
        else:
            guideText = ["Please select either GNS3 or VBox mode first."]

        self.ui.txbDescription.setText("\n".join(guideText))

    def handle_radio(self):
        self.update_status_and_description()


    # fungsi cek internet aktif
    def inetInterface(self):
        script1 = """
        ip route | grep '^default' | awk '{print $5}' | xargs -I {} sh -c 'ping -c 1 -W 1 -I {} 8.8.8.8 &> /dev/null && echo "{}"'
        """
        result = subprocess.run(script1, shell=True, capture_output=True, text=True)
        interfaces = result.stdout.strip().splitlines()
        interfaces.sort()

        # Isi combo box
        self.ui.cbxInterface.clear()
        self.ui.cbxInterface.addItems(interfaces) 

    def load_interfaces(self):
        self.inetInterface()

    def handle_cancel(self):
        self.status = 0
        self.ui.txbDescription.clear()
        QMessageBox.information(self, "Reset", "Configuration aborted.")

    def tampilkan_status_vboxnet(self):
        try:
            result = subprocess.run(
                ["VBoxManage", "list", "hostonlyifs"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            interfaces = result.stdout.strip().split("\n\n")

            vboxnet0_name = None
            vboxnet0_ip = None

            for interface in interfaces:
                lines = interface.strip().splitlines()
                name = None
                ip = None
                for line in lines:
                    if line.startswith("Name:"):
                        name = line.split(":", 1)[1].strip()
                    elif line.startswith("IPAddress:"):
                        ip = line.split(":", 1)[1].strip()
                if name == "vboxnet0":
                    vboxnet0_name = name
                    vboxnet0_ip = ip
                    break

            if vboxnet0_name and vboxnet0_ip:
                pesan = f"Interface: {vboxnet0_name}\nGateway IP: {vboxnet0_ip}"
            elif vboxnet0_name:
                pesan = f"Interface: {vboxnet0_name}\nGateway IP: Not Found"
            else:
                pesan = "Interface vboxnet0 Not Found."

        except subprocess.CalledProcessError as e:
            pesan = f"Unable to run VBoxManage:\n{e.stderr.strip()}"

        vboxnetStatus = [
            pesan,
            "--------------------------------------------------------",
            "Ensure the gateway and DNS settings in your VirtualBox Guest OS are properly configured."
        ]

        # Tampilkan langsung ke widget txbDescription
        self.ui.txbDescription.setPlainText("\n".join(vboxnetStatus))

    # Method ini dihubungkan ke tombol Activate
    def handle_activate(self):
        if not self.ui.rdbVbox.isChecked() and not self.ui.rdbGns.isChecked():
            QMessageBox.warning(self, "Warning", "Please select either GNS or VBox option before proceeding.")
            return
        elif self.status == 3 :
            QMessageBox.warning(self, "Warning", "(GNS or VBox) is already configured. Please click 'RESTORE' to reset the configuration.")
            return
        else:
            # Ambil string dari ComboBox
            selected_interface = self.ui.cbxInterface.currentText()  
            # Tampilkan ke TextBrowser (atau QTextEdit, tergantung widget kamu)
            # self.ui.txbDescription.setText(f"Interface yang dipilih: {selected_interface}")
            # Bersihkan aturan NAT sebelumnya
            script0 = """iptables-save -t nat | grep -- '-j MASQUERADE' | sed 's/^-A /iptables -t nat -D /' | while read line; do eval "$line"; done"""
            result0 = subprocess.run(script0, shell=True, capture_output=True, text=True )
            # Gunakan variabel yang sudah ada, jangan buat baru dengan nama lain
            script2 = f"iptables -t nat -A POSTROUTING -o {selected_interface} -j MASQUERADE"
            # error karena izin sudo dan gui cress
            result2 = subprocess.run(script2, shell=True, capture_output=True, text=True)
            # self.ui.txbDescription.setPlainText(script2)

            script4 = "sysctl -w net.ipv4.ip_forward=1"
            result4 = subprocess.run(script4, shell=True, capture_output=True, text=True)

            if self.status == 1:
                script5 = """
                ip tuntap add dev tap0 mode tap
                ip link set tap0 up
                ip addr add 192.168.100.1/24 dev tap0
                """
                subprocess.run(script5, shell=True, capture_output=True, text=True)
                script7 = """ip addr show tap0 | awk '/inet / {print "Interface: tap0, IP Address:", $2}' | cut -d/ -f1"""
                result7 = subprocess.run(script7, shell=True, capture_output=True, text=True)
                lines = [
                    result7.stdout.strip(),
                    "The IP address above is your gateway on the Cloud Interface Tap0 in GNS3.",
                    "Please configure your router in GNS3 to use the Tap0 interface to enable internet access."
                ]

                self.status = 3
                self.buka_btn_restore()
                self.ui.txbDescription.setPlainText("\n".join(lines))

            elif self.status == 2:
                self.tampilkan_status_vboxnet()
                # script8 = "VBoxManage list hostonlyifs"
                # result8 = subprocess.run(script8, shell=True, capture_output=True, text=True)
                # vboxnetStatus = [
                #     result8.stdout.strip(),
                #     "--------------------------------------------------------",
                #     "IP address di atas adalah Gateway kamu 192.168.56.1",
                #     "Jangan lupa cek konfigurasi gateway dan dns di OS Guest VirtualBoxmu"
                # ]

                self.status = 3
                self.buka_btn_restore()
                # self.ui.txbDescription.setPlainText("\n".join(vboxnetStatus))

    
    def handle_restore(self):
        # Bersihkan aturan NAT sebelumnya
        script0 = """iptables-save -t nat | grep -- '-j MASQUERADE' | sed 's/^-A /iptables -t nat -D /' | while read line; do eval "$line"; done"""
        result0 = subprocess.run(script0, shell=True, capture_output=True, text=True )
        script9 ="""sysctl -w net.ipv4.ip_forward=0 
        ip link set tap0 down
        ip tuntap del dev tap0 mode tap
        """
        result9 = subprocess.run(script9, shell=True, capture_output=True, text=True)
        self.ui.txbDescription.setText("Configuration status restored to DEFAULT.")
        self.reset_radio_buttons()
        self.tutup_btn_restore()
        self.status = 0

# tampelno dialogmu nek nduwor
if __name__ == "__main__":
    if not QApplication.instance():
        app = QApplication(sys.argv)
    else:
        app = QApplication.instance()

    dlg = MyDialog()
    dlg.show()
    sys.exit(app.exec())