from flask import Flask, render_template, request, redirect, url_for, session, flash
from models import db, Obat, User
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
from models import db, Obat, User, ObatMasuk, ObatKeluar


app = Flask(__name__)
app.secret_key = 'secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///obat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            return redirect(url_for('dashboard'))
        else:
            return redirect(url_for('login', error='Username atau password salah.'))

    return render_template('login.html')

@app.route('/bantuan')
def bantuan():
    return render_template('bantuan.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username sudah digunakan.')
        else:
            new_user = User(username=username, password=generate_password_hash(password))
            db.session.add(new_user)
            db.session.commit()
            flash('Registrasi berhasil. Silakan login.')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        flash("Anda belum login!")
        return redirect(url_for('login'))

    data_obat = Obat.query.all()
    return render_template('dashboard.html', data_obat=data_obat)

@app.route('/obat_masuk', methods=['GET', 'POST'])
def obat_masuk():
    if 'user' not in session:
        flash("Anda belum login.")
        return redirect(url_for('login'))

    daftar_obat = Obat.query.all()

    if request.method == 'POST':
        nama = request.form['obat']
        jumlah = int(request.form['jumlah'])

        obat = Obat.query.filter_by(nama=nama).first()
        if obat:
            obat.masuk += jumlah
        else:
            obat = Obat(nama=nama, masuk=jumlah, keluar=0)
            db.session.add(obat)

       
        riwayat = ObatMasuk(nama_obat=nama, jumlah=jumlah, tanggal=date.today())
        db.session.add(riwayat)

        db.session.commit()
        flash("Obat masuk berhasil dicatat.")
        return redirect(url_for('data_obat'))

    return render_template('obat_masuk.html', daftar_obat=daftar_obat)


@app.route('/obat_keluar', methods=['GET', 'POST'])
def obat_keluar():
    if 'user' not in session:
        flash("Anda belum login.")
        return redirect(url_for('login'))

    daftar_obat = Obat.query.all()

    if request.method == 'POST':
        nama = request.form['obat']
        jumlah = int(request.form['jumlah'])

        obat = Obat.query.filter_by(nama=nama).first()
        if obat:
            if obat.masuk - obat.keluar >= jumlah:
                obat.keluar += jumlah

                riwayat = ObatKeluar(nama_obat=nama, jumlah=jumlah, tanggal=date.today())
                db.session.add(riwayat)

                db.session.commit()
                flash("Obat keluar berhasil dicatat.")
            else:
                flash("Stok tidak cukup.")
        else:
            flash("Obat tidak ditemukan.")

        return redirect(url_for('data_obat'))

    return render_template('obat_keluar.html', daftar_obat=daftar_obat)


  

@app.route('/data_obat')
def data_obat():
    if 'user' not in session:
        flash("Anda belum login.")
        return redirect(url_for('login'))

    data = Obat.query.all()
    return render_template('data_obat.html', data=data)
@app.route('/riwayat_masuk')
def riwayat_masuk():
    if 'user' not in session:
        flash("Anda belum login.")
        return redirect(url_for('login'))
    
    riwayat = ObatMasuk.query.order_by(ObatMasuk.tanggal.desc()).all()
    return render_template('riwayat_masuk.html', riwayat=riwayat)

@app.route('/riwayat_keluar')
def riwayat_keluar():
    if 'user' not in session:
        flash("Anda belum login.")
        return redirect(url_for('login'))

    riwayat = ObatKeluar.query.order_by(ObatKeluar.tanggal.desc()).all()
    return render_template('riwayat_keluar.html', riwayat=riwayat)

# Untuk menjalankan secara lokal
if __name__ == '__main__':
    app.run(debug=True)

# Untuk Railway / gunicorn
# Railway akan mencari objek `app` secara langsung
