# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 13:17:30 2026

@author: baongan
"""


import re
class KhachHang:
    def __init__(self, ma_kh, ho_ten, sdt, email):
        self.ma_kh=ma_kh
        self.ho_ten = ho_ten
        self.sdt= sdt
        self.email= email
    
        
    @property 
    def ma_kh(self):
        return self._ma_kh
    @ma_kh.setter
    def ma_kh(self, ma_kh):
        if not isinstance(ma_kh, str) or not ma_kh.strip():
            raise ValueError("Mã khách hàng không được để trống")
        self._ma_kh = ma_kh.strip()
            
    
    @property 
    def ho_ten(self):
        return self._ho_ten
    @ho_ten.setter 
    def ho_ten(self, ho_ten):
        if not isinstance(ho_ten, str) or not ho_ten.strip():
            raise ValueError("Họ tên khách hàng không được để trống")
        self._ho_ten = ho_ten
    
    @property
    def sdt(self):
        return self._sdt
    
    @sdt.setter
    def sdt(self, sdt):
        if not isinstance(sdt, str) or not re.match(r'^(03|05|07|08|09)[0-9]{8}$', sdt):
            raise ValueError("Số điện thoại phải có 10 chữ số và bắt đầu bằng các đầu số di động Việt Nam")
        self._sdt = sdt
        
    @property 
    def email(self):
        return self._email
   
    @email.setter
    def email(self, email):
        if not isinstance(email, str) or not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
            raise ValueError("Email không đúng định dạng")
        self._email = email
        
    def to_dict(self):
        return{
            "ma_kh":self.ma_kh,
            "ho_ten":self.ho_ten,
            "sdt": self._sdt,
            "email":self._email
        }

class DichVu:
    def __init__(self, ma_dv, ten_dv, don_gia):
        self.ma_dv = ma_dv
        self.ten_dv = ten_dv
        self.don_gia = don_gia
        
    @property 
    def ma_dv(self):
        return self._ma_dv
    @ma_dv.setter 
    def ma_dv(self, ma_dv):
        if not isinstance(ma_dv, str) or not ma_dv.strip():
            raise ValueError("Mã dịch vụ không được để trống")
        self._ma_dv = ma_dv
        
    @property 
    def ten_dv(self):
        return self._ten_dv
    
    @ten_dv.setter 
    def ten_dv(self, ten_dv):
        if not ten_dv or not ten_dv.strip():
            raise ValueError("Tên dịch vụ không được để trống")
        self._ten_dv = ten_dv
    
    @property 
    def don_gia(self):
        return self._don_gia
    @don_gia.setter 
    def don_gia(self, don_gia):
        if isinstance(don_gia, bool) or not isinstance(don_gia, (int, float)) or don_gia < 0:
            raise ValueError("Đơn giá phải là số không âm")
        self._don_gia = don_gia
        
    
        
    def to_dict(self):
        return {
            "ma_dv": self.ma_dv,
            "ten_dv": self.ten_dv,
            "don_gia": self.don_gia
        }

if __name__ == "__main__":
    print("=== BAT DAU KIEM THU ===")

    # 1. Kiem thu khach hang hop le
    print("\n--- Khach hang hop le ---")
    try:
        kh = KhachHang("KH001", "Nguyen Van An",
                       "0912345678", "an@gmail.com")
        print(kh.to_dict())
    except ValueError as e:
        print("Loi:", e)

    # 2. Kiem thu so dien thoai sai
    print("\n--- So dien thoai sai ---")
    try:
        kh.sdt = "012345"
    except ValueError as e:
        print("Loi:", e)

    # 3. Kiem thu email sai
    print("\n--- Email sai ---")
    try:
        kh.email = "email_sai"
    except ValueError as e:
        print("Loi:", e)

    # 4. Kiem thu ma khach hang trong
    print("\n--- Ma khach hang trong ---")
    try:
        kh_loi = KhachHang(" ", "Nguyen Van B",
                           "0912345678", "b@gmail.com")
    except ValueError as e:
        print("Loi:", e)

    # 5. Kiem thu dich vu hop le
    print("\n--- Dich vu hop le ---")
    try:
        dv = DichVu("DV001", "Khach san cao cap", 1500000)
        print(dv.to_dict())
    except ValueError as e:
        print("Loi:", e)

    # 6. Kiem thu ten dich vu trong
    print("\n--- Ten dich vu trong ---")
    try:
        dv_loi = DichVu("DV002", "  ", 500000)
    except ValueError as e:
        print("Loi:", e)

    # 7. Kiem thu don gia am
    print("\n--- Don gia am ---")
    try:
        dv.don_gia = -1000
    except ValueError as e:
        print("Loi:", e)

    print("\n=== HOAN TAT KIEM THU ===")