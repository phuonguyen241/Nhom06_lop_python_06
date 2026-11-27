# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 14:57:20 2026

@author: baongan
"""

import hashlib
import os

from config import ROLE_ADMIN, ROLE_USER, USERS_FILE
from utils.file_helper import doc_json, luu_json

class TaiKhoan:
    
    def __init__(self, ma_tai_khoan, ten_dang_nhap, mat_khau, ho_ten, vai_tro=ROLE_USER, ma_khach_hang=None):
        if not ten_dang_nhap or not ten_dang_nhap.strip():
            raise ValueError("Tên đăng nhập không được để trống")
            
        if not mat_khau or not mat_khau.strip():
            raise ValueError("Mật khẩu không được để trống")
        self.ma_tai_khoan = ma_tai_khoan
        self.ten_dang_nhap= ten_dang_nhap
        self.ho_ten= ho_ten
        self.vai_tro = vai_tro
        self.ma_khach_hang= ma_khach_hang
        
        salt= os.urandom(16)
        mat_khau_hash = hashlib.pbkdf2_hmac(
            'sha256',
            mat_khau.encode('utf-8'),
            salt,
            100000
        )
        self.mat_khau_hash = salt.hex() + ":" + mat_khau_hash.hex()
        
    def kiem_tra_mat_khau(self, mat_khau):
        salt_hex, hash_luu = self.mat_khau_hash.split(":")

        salt = bytes.fromhex(salt_hex)

        hash_kiem_tra = hashlib.pbkdf2_hmac(
            'sha256',
            mat_khau.encode('utf-8'),
            salt,
            100000
        )

        return hash_kiem_tra.hex() == hash_luu
    
    def doi_mat_khau(self, mat_khau_moi):
        if not mat_khau_moi or not mat_khau_moi.strip():
            raise ValueError("Mật khẩu không được để trống")
        salt = os.urandom(16)
        mat_khau_hash = hashlib.pbkdf2_hmac(
            'sha256',
            mat_khau_moi.encode('utf-8'),
            salt,
            100000
        )
        self.mat_khau_hash = salt.hex() + ":" + mat_khau_hash.hex()
        
    def to_dict(self):
        return {
            "ma_tai_khoan": self.ma_tai_khoan,
            "ten_dang_nhap": self.ten_dang_nhap,
            "mat_khau_hash": self.mat_khau_hash,
            "ho_ten": self.ho_ten,
            "vai_tro": self.vai_tro,
            "ma_khach_hang": self.ma_khach_hang
        }
    @classmethod
    def tu_dict(cls, du_lieu):
        tk = cls.__new__(cls)

        tk.ma_tai_khoan = du_lieu["ma_tai_khoan"]
        tk.ten_dang_nhap = du_lieu["ten_dang_nhap"]
        tk.mat_khau_hash = du_lieu["mat_khau_hash"]
        tk.ho_ten = du_lieu["ho_ten"]
        tk.vai_tro = du_lieu["vai_tro"]
        tk.ma_khach_hang = du_lieu["ma_khach_hang"]

        return tk
    
class QuanLyTaiKhoan:
    def __init__(self):
        self.ds_tai_khoan = []
        self.tai_khoan_hien_tai = None
        self.doc_danh_sach()

    
    def doc_danh_sach(self):
        du_lieu = doc_json(USERS_FILE, [])

        self.ds_tai_khoan = []

        for item in du_lieu:
            tk = TaiKhoan.tu_dict(item)
            self.ds_tai_khoan.append(tk)

    
    def luu_danh_sach(self):
        thu_muc = os.path.dirname(USERS_FILE)

        if thu_muc:
            os.makedirs(thu_muc, exist_ok=True)

        du_lieu = []

        for tk in self.ds_tai_khoan:
            du_lieu.append(tk.to_dict())

        return luu_json(USERS_FILE, du_lieu)

    
    def dang_ky(self, ma_tai_khoan, ten_dang_nhap,
                mat_khau, ho_ten, ma_khach_hang=None):

        for tk in self.ds_tai_khoan:
            if tk.ten_dang_nhap == ten_dang_nhap:
                raise ValueError("Tên đăng nhập đã tồn tại")

            if tk.ma_tai_khoan == ma_tai_khoan:
                raise ValueError("Mã tài khoản đã tồn tại")

        tk_moi = TaiKhoan(
            ma_tai_khoan,
            ten_dang_nhap,
            mat_khau,
            ho_ten,
            ROLE_USER,
            ma_khach_hang
        )

        self.ds_tai_khoan.append(tk_moi)

        if not self.luu_danh_sach():
            self.ds_tai_khoan.remove(tk_moi)
            raise ValueError("Không thể lưu tài khoản")

        return tk_moi
    
    def lay_khach_hang_hien_tai(self, ql_tour):
        if self.tai_khoan_hien_tai is None:
            return None

        ma_kh = self.tai_khoan_hien_tai.ma_khach_hang

        return ql_tour.lay_khach_hang_theo_ma(ma_kh)
    
    def kiem_tra_quyen_phieu_dat(self, phieu):
        if self.tai_khoan_hien_tai is None:
            return False

        if self.la_admin():
            return True

        ma_kh = self.tai_khoan_hien_tai.ma_khach_hang

        if ma_kh is None:
            return False

        return ma_kh == phieu.khach_hang.ma_kh
    
    def dang_nhap(self, ten_dang_nhap, mat_khau):
        self.tai_khoan_hien_tai = None

        for tk in self.ds_tai_khoan:
            if tk.ten_dang_nhap == ten_dang_nhap:
                if tk.kiem_tra_mat_khau(mat_khau):
                    self.tai_khoan_hien_tai = tk
                    return True

                return False

        return False

    
    def dang_xuat(self):
        self.tai_khoan_hien_tai = None

    
    def doi_mat_khau(self, mat_khau_cu, mat_khau_moi):
        if self.tai_khoan_hien_tai is None:
            raise ValueError("Bạn chưa đăng nhập")

        if not self.tai_khoan_hien_tai.kiem_tra_mat_khau(mat_khau_cu):
            raise ValueError("Mật khẩu cũ không chính xác")

        self.tai_khoan_hien_tai.doi_mat_khau(mat_khau_moi)

        if not self.luu_danh_sach():
            raise ValueError("Không thể lưu mật khẩu mới")

    
    def la_admin(self):
        if self.tai_khoan_hien_tai is None:
            return False

        return self.tai_khoan_hien_tai.vai_tro == ROLE_ADMIN

    def kiem_tra_quyen(self, vai_tro):
        if self.tai_khoan_hien_tai is None:
            return False

        return self.tai_khoan_hien_tai.vai_tro == vai_tro

    def tao_admin_mau(self):
        for tk in self.ds_tai_khoan:
            if tk.ten_dang_nhap == "admin":
                return tk

        tk_admin = TaiKhoan(
            "TK_ADMIN",
            "admin",
            "admin123",
            "Quan tri vien",
            ROLE_ADMIN
        )

        self.ds_tai_khoan.append(tk_admin)

        if not self.luu_danh_sach():
            self.ds_tai_khoan.remove(tk_admin)
            raise ValueError("Không thể tạo tài khoản Admin")

        return tk_admin    

    def da_dang_nhap(self):
        return self.tai_khoan_hien_tai is not None
    

if __name__ == "__main__":

    # ==========================================
    # 1. KIEM THU LOP TAI KHOAN
    # ==========================================
    print("\n========== KIEM THU LOP TAI KHOAN ==========")

    try:
        tk = TaiKhoan(
            "TK001",
            "baongan",
            "123456",
            "Nguyen Van An",
            ROLE_USER,
            "KH001"
        )

        print("\nThong tin tai khoan:")
        print(tk.to_dict())

        print("\nKiem tra mat khau dung:")
        print(tk.kiem_tra_mat_khau("123456"))

        print("\nKiem tra mat khau sai:")
        print(tk.kiem_tra_mat_khau("111111"))

        print("\nDoi mat khau:")
        tk.doi_mat_khau("abcdef")

        print("Kiem tra mat khau moi:")
        print(tk.kiem_tra_mat_khau("abcdef"))

    except ValueError as e:
        print("Loi:", e)


    # ==========================================
    # 2. KIEM THU QUAN LY TAI KHOAN
    # ==========================================
    print("\n========== KIEM THU QUAN LY TAI KHOAN ==========")

    ql = QuanLyTaiKhoan()

    print("Danh sach tai khoan:", ql.ds_tai_khoan)
    print("Trang thai dang nhap:", ql.da_dang_nhap())
    print("Kiem tra quyen Admin:", ql.la_admin())


    # ==========================================
    # 3. KIEM THU DANG KY TAI KHOAN USER
    # ==========================================
    print("\n========== KIEM THU DANG KY USER ==========")

    try:
        tk_moi = ql.dang_ky(
            "TK003",
            "ngan_test_02",
            "123456",
            "Nguyen Thi Ngoc",
            "KH002"
        )

        print("Dang ky thanh cong:")
        print(tk_moi.to_dict())

    except ValueError as e:
        print("Loi:", e)


    # ==========================================
    # 4. KIEM THU DANG NHAP
    # ==========================================
    print("\n========== KIEM THU DANG NHAP ==========")

    ket_qua = ql.dang_nhap("ngan_test_02", "123456")
    print("Dang nhap:", ket_qua)
    print("Trang thai dang nhap:", ql.da_dang_nhap())


    # ==========================================
    # 5. KIEM THU DANG XUAT
    # ==========================================
    print("\n========== KIEM THU DANG XUAT ==========")

    ql.dang_xuat()

    print("Trang thai sau dang xuat:", ql.da_dang_nhap())
    print("Kiem tra quyen Admin:", ql.la_admin())


    # ==========================================
    # 6. KIEM THU DOC DU LIEU VA DANG NHAP LAI
    # ==========================================
    print("\n========== KIEM THU DOC DU LIEU ==========")

    ql_moi = QuanLyTaiKhoan()

    print("So luong tai khoan da luu:", len(ql_moi.ds_tai_khoan))

    ket_qua = ql_moi.dang_nhap("ngan_test_02", "123456")
    print("Dang nhap tai khoan da luu:", ket_qua)

    ql_moi.dang_xuat()


    # ==========================================
    # 7. KIEM THU PHAN QUY ADMIN
    # ==========================================
    print("\n========== KIEM THU PHAN QUY ADMIN ==========")

    ql = QuanLyTaiKhoan()

    try:
        tk_admin = ql.tao_admin_mau()

        print("Thong tin tai khoan Admin:")
        print(tk_admin.to_dict())

        ket_qua = ql.dang_nhap("admin", "admin123")
        print("Dang nhap Admin:", ket_qua)

        print("Kiem tra quyen Admin:", ql.la_admin())

        ql.dang_xuat()
        print("Quyen Admin sau dang xuat:", ql.la_admin())

    except ValueError as e:
        print("Loi:", e)


    # ==========================================
    # 8. KIEM THU QUYEN USER
    # ==========================================
    print("\n========== KIEM THU QUYEN USER ==========")

    ql = QuanLyTaiKhoan()

    try:
        tk_user = ql.dang_ky(
            "TK004",
            "user_test",
            "123456",
            "Nguyen Van B",
            "KH004"
        )

        print("Thong tin tai khoan User:")
        print(tk_user.to_dict())

        print("Vai tro tai khoan moi:", tk_user.vai_tro)
        print("Co phai Admin khong:", tk_user.vai_tro == ROLE_ADMIN)

    except ValueError as e:
        print("Loi:", e)


    # ==========================================
    # KET THUC KIEM THU
    # ==========================================
    print("\n========== HOAN TAT KIEM THU ==========")
