# -*- coding: utf-8 -*-
"""
Created on Tue Oct 27 14:48:19 2026

@author: GBC
"""

class Tour:
    """Lớp cha (Base class) đại diện cho một Tour du lịch chung."""
    def __init__(self, ma_tour, ten_tour, diem_den, so_ngay, ngay_khoi_hanh, gia_co_ban, so_cho_toi_da, so_cho_da_dat=0):
        self.ma_tour = ma_tour
        self.ten_tour = ten_tour
        self.diem_den = diem_den
        self.so_ngay = so_ngay
        self.ngay_khoi_hanh = ngay_khoi_hanh
        self.gia_co_ban = float(gia_co_ban)
        self.so_cho_toi_da = int(so_cho_toi_da)
        self.so_cho_da_dat = int(so_cho_da_dat)

    def kiem_tra_con_cho(self, so_ve):
        """Kiểm tra xem tour còn đủ chỗ trống hay không."""
        if so_ve <= 0:
            return False
        return (self.so_cho_da_dat + so_ve) <= self.so_cho_toi_da

    def dat_cho(self, so_ve):
        """Tăng số chỗ đã đặt khi giao dịch thành công."""
        if self.kiem_tra_con_cho(so_ve):
            self.so_cho_da_dat += so_ve
            return True
        return False

    def huy_cho(self, so_ve):
        """Giảm số chỗ đã đặt khi có khách hủy vé."""
        if 0 < so_ve <= self.so_cho_da_dat:
            self.so_cho_da_dat -= so_ve
            return True
        return False

    def tinh_gia_ve(self):
        """Phương thức mẫu của lớp cha, trả về giá vé cơ bản."""
        return self.gia_co_ban

    def to_dict(self):
        """Chuyển đối tượng thành từ điển (dict) để phục vụ ghi file JSON."""
        return {
            "loai_tour": "CoBan",
            "ma_tour": self.ma_tour,
            "ten_tour": self.ten_tour,
            "diem_den": self.diem_den,
            "so_ngay": self.so_ngay,
            "ngay_khoi_hanh": self.ngay_khoi_hanh,
            "gia_co_ban": self.gia_co_ban,
            "so_cho_toi_da": self.so_cho_toi_da,
            "so_cho_da_dat": self.so_cho_da_dat
        }


class TourNoiDia(Tour):
    """Lớp con kế thừa từ Tour, áp dụng cho Tour Nội Địa."""
    def __init__(self, ma_tour, ten_tour, diem_den, so_ngay, ngay_khoi_hanh, gia_co_ban, so_cho_toi_da, phu_thu, so_cho_da_dat=0):
        super().__init__(ma_tour, ten_tour, diem_den, so_ngay, ngay_khoi_hanh, gia_co_ban, so_cho_toi_da, so_cho_da_dat)
        self.phu_thu = float(phu_thu)

    def tinh_gia_ve(self):
        """Ghi đè (override) phương thức tính giá vé: Giá cơ bản + Phụ thu."""
        return self.gia_co_ban + self.phu_thu

    def to_dict(self):
        """Bổ sung thông tin riêng của tour nội địa vào dict để ghi JSON."""
        data = super().to_dict()
        data["loai_tour"] = "NoiDia"
        data["phu_thu"] = self.phu_thu
        return data


class TourQuocTe(Tour):
    """Lớp con kế thừa từ Tour, áp dụng cho Tour Quốc Tế."""
    def __init__(self, ma_tour, ten_tour, diem_den, so_ngay, ngay_khoi_hanh, gia_co_ban, so_cho_toi_da, phi_visa, so_cho_da_dat=0):
        super().__init__(ma_tour, ten_tour, diem_den, so_ngay, ngay_khoi_hanh, gia_co_ban, so_cho_toi_da, so_cho_da_dat)
        self.phi_visa = float(phi_visa)

    def tinh_gia_ve(self):
        """Ghi đè (override) phương thức tính giá vé: Giá cơ bản + Phí visa."""
        return self.gia_co_ban + self.phi_visa

    def to_dict(self):
        """Bổ sung thông tin riêng của tour quốc tế vào dict để ghi JSON."""
        data = super().to_dict()
        data["loai_tour"] = "QuocTe"
        data["phi_visa"] = self.phi_visa
        return data


if __name__ == '__main__':
    print("=== KIỂM THỬ ĐỘC LẬP FILE TOUR.PY ===")
    
    # Test Tour Nội Địa
    t_nd = TourNoiDia("ND01", "Đà Nẵng - Hội An", "Đà Nẵng", 3, "2026-06-15", 3000000, 25, 500000)
    print("Tên tour:", t_nd.ten_tour, "| Loại: Nội Địa")
    print("Giá vé thực tế (Đa hình):", t_nd.tinh_gia_ve(), "VNĐ")
    print("Kiểm tra còn 5 chỗ:", t_nd.kiem_tra_con_cho(5))
    print("Đặt 2 chỗ thành công:", t_nd.dat_cho(2), "| Số chỗ đã đặt:", t_nd.so_cho_da_dat)
    print("Dữ liệu dict để ghi JSON:", t_nd.to_dict())
    
    print("-" * 40)
    
    # Test Tour Quốc Tế
    t_qt = TourQuocTe("QT01", "Bangkok - Pattaya", "Thái Lan", 4, "2026-07-20", 6000000, 20, 1200000)
    print("Tên tour:", t_qt.ten_tour, "| Loại: Quốc Tế")
    print("Giá vé thực tế (Đa hình):", t_qt.tinh_gia_ve(), "VNĐ")
    print("Dữ liệu dict để ghi JSON:", t_qt.to_dict())