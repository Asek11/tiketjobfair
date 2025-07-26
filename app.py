from flask import Flask, render_template, request, redirect, url_for
import csv
import random
import string
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# Fungsi untuk membuat nomor tiket unik
def generate_ticket_number():
    random_digits = ''.join(random.choices(string.digits, k=8))
    return f"JF{random_digits}"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/daftar', methods=['POST'])
def daftar():
    if request.method == 'POST':
        nama = request.form['nama']
        alamat = request.form['alamat']
        kontak = request.form['kontak']
        usia = request.form['usia']
        rencana_kunjung = request.form['rencana_kunjung']
        
        nomor_tiket = generate_ticket_number()
        
        # --- Bagian Baru: Membuat Kode QR ---
        # Data yang akan dimasukkan ke dalam kode QR
        qr_data = f"Nomor Tiket: {nomor_tiket}\nNama: {nama}\nAlamat: {alamat}\nKontak: {kontak}\nUsia: {usia}\nRencana Kunjung: {rencana_kunjung}"

        # Membuat objek QR Code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        
        # Mengubah gambar QR menjadi format Base64
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, "PNG")
        qr_code_base64 = base64.b64encode(buffer.getvalue()).decode()
        # --- Akhir Bagian Baru ---
        
        # Simpan data ke file CSV
        with open('pendaftar.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([nomor_tiket, nama, alamat, kontak, usia, rencana_kunjung])
            
        # Kirim data ke halaman tiket, termasuk kode QR
        return render_template('tiket.html', 
                               nama=nama, 
                               alamat=alamat, 
                               kontak=kontak, 
                               usia=usia, 
                               rencana_kunjung=rencana_kunjung, 
                               nomor_tiket=nomor_tiket,
                               qr_code=qr_code_base64) # Variabel qr_code dikirim ke template
        
if __name__ == '__main__':
    app.run(debug=True)