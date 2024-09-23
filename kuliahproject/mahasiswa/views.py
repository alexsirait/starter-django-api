import json
from django.db import connection
from kuliahproject.response import Response
from django.views.decorators.csrf import csrf_exempt
from kuliahproject.middleware import jwtRequired
import datetime
import jwt

import os
import environ

env = environ.Env(
    DEBUG=(bool, False)
)
environ.Env.read_env()

def index(request):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tbl_mahasiswa")
                rows = cursor.fetchall()
                mahasiswa_list = [
                    {
                        "nim": row[1],
                        "nama_mahasiswa": row[2],
                        "jurusan": row[3],
                        "tahun_angkatan": row[4],
                        "alamat": row[5],
                        "nomor_telepon": row[6],
                        "nilai_bindo": row[7],
                        "nilai_eng": row[8]
                    }
                    for row in rows
                ]
            return Response.ok(values=mahasiswa_list, message="List data telah tampil", messagetype="S")
        except Exception as e:
            return Response.badRequest(message=str(e), messagetype="E")

@csrf_exempt
def insert(request):
    if request.method == 'POST':
        try:
            json_data = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute(
                    "INSERT INTO tbl_mahasiswa (nim, nama_mahasiswa, jurusan, tahun_angkatan, alamat, nomor_telepon, nilai_bindo, nilai_eng) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                    (json_data['nim'], json_data['nama_mahasiswa'], json_data['jurusan'], json_data['tahun_angkatan'],
                     json_data['alamat'], json_data['nomor_telepon'], json_data['nilai_bindo'], json_data['nilai_eng'])
                )
                
                cursor.execute("SELECT LAST_INSERT_ID()")
                new_id = cursor.fetchone()[0]
                
            return Response.ok(values={"id": new_id}, message="Added!", messagetype="S")
        except Exception as e:
            return Response.badRequest(message=str(e), messagetype="E")

@jwtRequired
def show(request, id):
    if request.method == 'GET':
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tbl_mahasiswa WHERE id = %s", [id])
                row = cursor.fetchone()

            if not row:
                return Response.badRequest(message='Data mahasiswa tidak ditemukan!', messagetype="E")

            mahasiswa_data = {
                "id": row[0],
                "nim": row[1],
                "nama_mahasiswa": row[2],
                "jurusan": row[3],
                "tahun_angkatan": row[4],
                "alamat": row[5],
                "nomor_telepon": row[6],
                "nilai_bindo": row[7],
                "nilai_eng": row[8]
            }
            return Response.ok(values=mahasiswa_data, message='List data telah tampil', messagetype="S")
        except Exception as e:
            return Response.badRequest(message=str(e), messagetype="E")

@csrf_exempt
def update(request, id):
    if request.method == 'PUT':
        try:
            json_data = json.loads(request.body)
            with connection.cursor() as cursor:
                cursor.execute(
                    "UPDATE tbl_mahasiswa SET nama_mahasiswa = %s, jurusan = %s, tahun_angkatan = %s, alamat = %s, nomor_telepon = %s, nilai_bindo = %s, nilai_eng = %s WHERE id = %s",
                    (json_data['nama_mahasiswa'], json_data['jurusan'], json_data['tahun_angkatan'],
                    json_data['alamat'], json_data['nomor_telepon'], json_data['nilai_bindo'], json_data['nilai_eng'], id)
                )
                update_id = id
            return Response.ok(values={"id": update_id}, message="Updated!", messagetype="S")
        except Exception as e:
            return Response.badRequest(message=str(e), messagetype="E")

@csrf_exempt
def destroy(request, id):
    if request.method == 'DELETE':
        try:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM tbl_mahasiswa WHERE id = %s", [id])
            return Response.ok(values={"id": id}, message="Deleted!", messagetype="S")
        except Exception as e:
            return Response.badRequest(message=str(e), messagetype="E")

@csrf_exempt
def auth(request):
    if request.method == 'POST':
        json_data = json.loads(request.body)
        nim = json_data['nim']
        nomor_telepon = json_data['nomor_telepon']

        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT * FROM tbl_mahasiswa WHERE nim = %s AND nomor_telepon = %s", [nim, nomor_telepon])
                row = cursor.fetchone()

            if not row:
                return Response.badRequest(message='Pengguna tidak ditemukan!', messagetype='E')

            payload = {
                'id': row[0],
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)
            }
            token = jwt.encode(payload, env('JWT_SECRET'), algorithm='HS256')

            user_data = {
                "id": row[0],
                "nim": row[1],
                "nama_mahasiswa": row[2],
                "jurusan": row[3],
                "tahun_angkatan": row[4],
                "alamat": row[5],
                "nomor_telepon": row[6],
                "nilai_bindo": row[7],
                "nilai_eng": row[8],
                "token": token
            }

            return Response.ok(values=user_data, message="Berhasil masuk!", messagetype='S')
        except Exception as e:
            return Response.badRequest(message=f'Terjadi kesalahan: {str(e)}')