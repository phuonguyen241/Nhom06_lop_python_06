# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 13:15:01 2026

@author: baongan
"""

import re
class KhachHang:
    def __init__(self, ma_kh, ho_ten, sdt, email):
        self.ma_kh=ma_kh
        self.ho_ten = ho_ten
        self._sdt= sdt
        self.email= email
        
    @property
    def sdt(self):
        return self._sdt
    @sdt.setter
    def sdt(self, sdt): 
        if not re.match(r'^(03|05|07|08|09)[0-9]{8}$', sdt):
            raise ValueError("Số điện thoại phải có 10 chữ số và bắt đầu bằng các đầu số di động Việt Nam ")
        self._sdt = sdt
        
    @property 
    def email(self):
        return self._email
    @email.setter 
    def email(self, email):
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$', email):
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
        
    def to_dict(self):
        return {
            "ma_dv": self.ma_dv,
            "ten_dv": self.ten_dv,
            "don_gia": self.don_gia
        }
if __name__ == "__main__":
    try:
        kh = KhachHang("KH001", "Nguyen Van An", "0912345678","an@gmail.com")
        print("THONG TIN KHACH HANG")
        print(kh.to_dict())
        
        kh.sdt = "012345"
    except ValueError as e:
        print("loi:",e)
    dv = DichVu("DV001", "Khách sạn cao cấp", 1500000)
    print(dv.to_dict())
