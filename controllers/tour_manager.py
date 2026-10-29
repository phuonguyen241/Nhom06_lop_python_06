# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 21:43:53 2026

@author: asus
"""

import sys
sys.path.append("..")

from utils.file_helper import doc_json, luu_json
from models.tour import TourNoiDia, TourQuocTe

class QuanLyTour:
    def __init__(self, file_path="data/tours.json"):
        self.file_path = file_path
        self.ds_tour = []
        self.tai_du_lieu()
        
    def tai_du_lieu(self):
        du_lieu_tho = doc_json(self.file_path)
        self.ds_tour = []

        for item in du_lieu_tho:
            loai = item.get("loai_tour", "NoiDia")
            if loai in ["NoiDia", "Nội địa", "TourNoiDia"]:
                tour = TourNoiDia(
                    ma_tour=item.get("ma_tour"),
                    ten_tour=item.get("ten_tour"),
                    diem_den=item.get("diem_den"),
                    so_ngay=item.get("so_ngay"),
                    ngay_khoi_hanh=item.get("ngay_khoi_hanh"),
                    gia_co_ban=item.get("gia_co_ban"),
                    so_cho_toi_da=item.get("so_cho_toi_da"),
                    phu_thu=item.get("phu_thu", 0),
                    so_cho_da_dat=item.get("so_cho_da_dat", 0)
                )
            else:
                tour = TourQuocTe(
                    ma_tour=item.get("ma_tour"),
                    ten_tour=item.get("ten_tour"),
                    diem_den=item.get("diem_den"),
                    so_ngay=item.get("so_ngay"),
                    ngay_khoi_hanh=item.get("ngay_khoi_hanh"),
                    gia_co_ban=item.get("gia_co_ban"),
                    so_cho_toi_da=item.get("so_cho_toi_da"),
                    phi_visa=item.get("phi_visa", 0),
                    so_cho_da_dat=item.get("so_cho_da_dat", 0)
                )
            self.ds_tour.append(tour)
        
    def luu_du_lieu(self):
        du_lieu_ghi = []
        for tour in self.ds_tour:
            du_lieu_ghi.append(tour.to_dict())
        return luu_json(self.file_path, du_lieu_ghi)
            
    def them_tour(self, tour):
        for t in self.ds_tour:
            if t.ma_tour == tour.ma_tour:
                print(f"Lỗi: Mã tour '{tour.ma_tour}' đã tồn tại!")
                return False
                
        self.ds_tour.append(tour)
        self.luu_du_lieu()
        return True
        
    def xoa_tour(self, ma_tour):
        for tour in self.ds_tour:
            if tour.ma_tour == ma_tour:
                self.ds_tour.remove(tour)
                self.luu_du_lieu()
                return True

        print(f"Lỗi: Không tìm thấy tour có mã '{ma_tour}' để xóa!")
        return False
        
    def cap_nhat_tour(self, ma_tour, thong_tin_moi):
        for tour in self.ds_tour:
            if tour.ma_tour == ma_tour:
                tour.ten_tour = thong_tin_moi.get("ten_tour", tour.ten_tour)
                tour.diem_den = thong_tin_moi.get("diem_den", tour.diem_den)
                tour.so_ngay = thong_tin_moi.get("so_ngay", tour.so_ngay)
                tour.ngay_khoi_hanh = thong_tin_moi.get("ngay_khoi_hanh", tour.ngay_khoi_hanh)
                tour.gia_co_ban = thong_tin_moi.get("gia_co_ban", tour.gia_co_ban)
                tour.so_cho_toi_da = thong_tin_moi.get("so_cho_toi_da", tour.so_cho_toi_da)

                self.luu_du_lieu()
                return True

        print(f"Lỗi: Không tìm thấy tour có mã '{ma_tour}' để cập nhật!")
        return False
        
    def tim_kiem(self, diem_den=None, gia_toi_da=None):
        ket_qua = []
        for tour in self.ds_tour:
            # Kiểm tra tiêu chí điểm đến
            thoa_diem_den = True
            if diem_den:
                thoa_diem_den = diem_den.lower() in tour.diem_den.lower()

            # Kiểm tra tiêu chí giá tối đa
            thoa_gia = True
            if gia_toi_da is not None:
                thoa_gia = tour.gia_co_ban <= gia_toi_da

            # Thỏa mãn đồng thời cả 2 tiêu chí thì đưa vào danh sách kết quả
            if thoa_diem_den and thoa_gia:
                ket_qua.append(tour)
                
        return ket_qua
        
    def thong_ke_ty_le_lap_day(self):
        tong_cho = 0
        tong_da_dat = 0

        for tour in self.ds_tour:
            tong_cho += tour.so_cho_toi_da
            tong_da_dat += tour.so_cho_da_dat

        if tong_cho == 0:
            return 0.0

        ty_le = (tong_da_dat / tong_cho) * 100
        return round(ty_le, 2)
        
    def thong_ke_doanh_thu(self):
        tong_doanh_thu = 0.0
        for tour in self.ds_tour:
            tong_doanh_thu += tour.so_cho_da_dat * tour.tinh_gia_ve()
        return tong_doanh_thu
        
    def lay_danh_sach(self):
        return self.ds_tour

    def lay_tour_theo_ma(self, ma_tour):
        for tour in self.ds_tour:
            if tour.ma_tour == ma_tour:
                return tour
        return None
        
    
            
if __name__ == "__main__":
    print("=== BẮT ĐẦU KIỂM THỬ ===")

    # 1. Khởi tạo đối tượng quản lý với file test riêng
    ql = QuanLyTour("test_tours.json")

    # 2. Khởi tạo 2 đối tượng tour mẫu chuẩn theo đúng models/tour.py
    tour1 = TourNoiDia(
        ma_tour="ND01",
        ten_tour="Đà Nẵng - Bà Nà Hills",
        diem_den="Đà Nẵng",
        so_ngay=3,
        ngay_khoi_hanh="2026-06-15",
        gia_co_ban=3200000,
        so_cho_toi_da=20,
        phu_thu=300000,
        so_cho_da_dat=10
    )

    tour2 = TourQuocTe(
        ma_tour="QT01",
        ten_tour="Bangkok - Pattaya",
        diem_den="Thái Lan",
        so_ngay=4,
        ngay_khoi_hanh="2026-07-20",
        gia_co_ban=6500000,
        so_cho_toi_da=30,
        phi_visa=1200000,
        so_cho_da_dat=15
    )

    # 3. Kiểm thử thêm tour mới
    print("\n--- 1. Kiểm thử thêm tour ---")
    kq_them1 = ql.them_tour(tour1)
    kq_them2 = ql.them_tour(tour2)
    print("Thêm tour 1:", "Thành công" if kq_them1 else "Thất bại")
    print("Thêm tour 2:", "Thành công" if kq_them2 else "Thất bại")

    # 4. Kiểm thử chống trùng mã
    print("\n--- 2. Kiểm thử kiểm tra trùng mã ---")
    kq_trung = ql.them_tour(tour1)
    print("Thử thêm lại mã trùng:", "Đã chặn thành công" if not kq_trung else "Lỗi (vẫn bị thêm)")

    # 5. Kiểm thử tìm kiếm đa tiêu chí
    print("\n--- 3. Kiểm thử tìm kiếm ---")
    ds_tim = ql.tim_kiem(diem_den="Đà Nẵng", gia_toi_da=4000000)
    print(f"Số tour tìm thấy: {len(ds_tim)}")
    for t in ds_tim:
        print(f"+ {t.ma_tour} - {t.ten_tour} - Giá: {t.gia_co_ban} VNĐ")

    # 6. Kiểm thử thống kê doanh thu
    print("\n--- 4. Kiểm thử thống kê doanh thu ---")
    doanh_thu = ql.thong_ke_doanh_thu()
    print(f"Tổng doanh thu dự kiến: {doanh_thu:,.0f} VNĐ")

    # 7. Kiểm thử thống kê tỷ lệ lấp đầy
    print("\n--- 5. Kiểm thử thống kê tỷ lệ lấp đầy ---")
    ty_le = ql.thong_ke_ty_le_lap_day()
    print(f"Tỷ lệ lấp đầy phòng/ghế: {ty_le}%")

    # 8. Kiểm thử cập nhật thông tin
    print("\n--- 6. Kiểm thử cập nhật thông tin ---")
    thong_tin_sua = {"gia_co_ban": 3500000, "so_cho_toi_da": 25}
    kq_sua = ql.cap_nhat_tour("ND01", thong_tin_sua)
    print("Cập nhật tour ND01:", "Thành công" if kq_sua else "Thất bại")

    # 9. Kiểm thử xóa tour
    print("\n--- 7. Kiểm thử xóa tour ---")
    kq_xoa = ql.xoa_tour("QT01")
    print("Xóa tour QT01:", "Thành công" if kq_xoa else "Thất bại")

