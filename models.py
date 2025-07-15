from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Obat(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False, unique=True)
    masuk = db.Column(db.Integer, default=0)
    keluar = db.Column(db.Integer, default=0)


class ObatMasuk(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_obat = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal = db.Column(db.Date, nullable=False)


class ObatKeluar(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_obat = db.Column(db.String(100), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    tanggal = db.Column(db.Date, nullable=False)
