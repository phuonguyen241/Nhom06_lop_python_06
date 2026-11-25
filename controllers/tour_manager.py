# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 21:43:53 2026

@author: asus
"""

import sys
sys.path.append("..")

from utils.file_helper import doc_json, luu_json, xuat_bao_cao_csv
from models.tour import TourNoiDia, TourQuocTe
from config import DATA_FILE

class QuanLyTour:
    # Khởi tạo đối tượng quản lý
    def __init__(self, file_path=DATA_FILE):
        self.file_path = file_path
        self.ds_tour = []
        self.ds_khach_hang = []
        self.ds_dich_vu = []
        self.ds_phieu_dat = []
        self.ds_diem_den = []
        self.tai_du_lieu()

    # Tải dữ liệu tour từ JSON
    def tai_du_lieu(self):
        du_lieu_tho = doc_json(self.file_path, {})
        self.ds_tour = []

        for item in du_lieu_tho.get("tours", []):
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

    # Lưu dữ liệu tour vào file JSON
    def luu_du_lieu(self):
        try:
            du_lieu = doc_json(self.file_path, {
                "tours": [],
                "customers": [],
                "services": [],
                "bookings": [],
                "destinations": []
            })

            du_lieu["tours"] = [tour.to_dict() for tour in self.ds_tour]

            return luu_json(self.file_path, du_lieu)

        except Exception as e:
            print("Lỗi khi lưu dữ liệu:", e)
            return False

    # Thêm tour
    def them_tour(self, tour):
        for t in self.ds_tour:
            if t.ma_tour == tour.ma_tour:
                print("Mã tour đã tồn tại!")
                return False

        self.ds_tour.append(tour)

        if self.luu_du_lieu():
            return True
        else:
            self.ds_tour.remove(tour)
            return False

    # Xóa tour
    def xoa_tour(self, ma_tour):
        for i, tour in enumerate(self.ds_tour):
            if tour.ma_tour == ma_tour:

                if tour.so_cho_da_dat > 0:
                    print("Không thể xóa tour đã có khách đặt!")
                    return False

                self.ds_tour.pop(i)

                try:
                    if self.luu_du_lieu():
                        return True
                except Exception as e:
                    print("Lỗi khi xóa tour:", e)

                self.ds_tour.insert(i, tour)
                return False

        print("Không tìm thấy tour cần xóa!")
        return False

    # Cập nhật thông tin tour theo mã
    def cap_nhat_tour(self, ma_tour, thong_tin_moi):
        for tour in self.ds_tour:
            if tour.ma_tour == ma_tour:

                thong_tin_cu = tour.to_dict()
                so_cho_moi = thong_tin_moi.get(
                    "so_cho_toi_da", tour.so_cho_toi_da
                )

                if type(so_cho_moi) != int:
                    print("Số chỗ tối đa phải là số nguyên!")
                    return False

                if so_cho_moi <= 0:
                    print("Số chỗ tối đa phải lớn hơn 0!")
                    return False

                if so_cho_moi < tour.so_cho_da_dat:
                    print("Số chỗ tối đa không được nhỏ hơn số chỗ đã đặt!")
                    return False

                try:
                    tour.ten_tour = thong_tin_moi.get("ten_tour", tour.ten_tour)
                    tour.diem_den = thong_tin_moi.get("diem_den", tour.diem_den)
                    tour.so_ngay = thong_tin_moi.get("so_ngay", tour.so_ngay)
                    tour.ngay_khoi_hanh = thong_tin_moi.get(
                        "ngay_khoi_hanh", tour.ngay_khoi_hanh
                    )
                    tour.gia_co_ban = thong_tin_moi.get(
                        "gia_co_ban", tour.gia_co_ban
                    )
                    tour.so_cho_toi_da = so_cho_moi

                    if self.luu_du_lieu():
                        return True

                except Exception as e:
                    print("Lỗi khi cập nhật tour:", e)

                tour.ten_tour = thong_tin_cu["ten_tour"]
                tour.diem_den = thong_tin_cu["diem_den"]
                tour.so_ngay = thong_tin_cu["so_ngay"]
                tour.ngay_khoi_hanh = thong_tin_cu["ngay_khoi_hanh"]
                tour.gia_co_ban = thong_tin_cu["gia_co_ban"]
                tour.so_cho_toi_da = thong_tin_cu["so_cho_toi_da"]

                return False

        print(f"Lỗi: Không tìm thấy tour có mã '{ma_tour}' để cập nhật!")
        return False

    # Tìm kiếm tour
    def tim_kiem(self, diem_den=None, gia_toi_da=None, ngay_khoi_hanh=None):
        ket_qua = []

        for tour in self.ds_tour:

            thoa_diem_den = True
            if diem_den:
                thoa_diem_den = diem_den.lower() in tour.diem_den.lower()

            thoa_gia = True
            if gia_toi_da is not None:
                thoa_gia = tour.tinh_gia_ve() <= gia_toi_da

            thoa_ngay = True
            if ngay_khoi_hanh:
                thoa_ngay = tour.ngay_khoi_hanh == ngay_khoi_hanh

            if thoa_diem_den and thoa_gia and thoa_ngay:
                ket_qua.append(tour)

        return ket_qua

    # Thống kê tỷ lệ lấp đầy
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

    # Thống kê doanh thu
    def thong_ke_doanh_thu(self):
        tong_doanh_thu = 0.0
        for tour in self.ds_tour:
            tong_doanh_thu += tour.so_cho_da_dat * tour.tinh_gia_ve()
        return tong_doanh_thu

    # Lấy danh sách tour
    def lay_danh_sach(self):
        return self.ds_tour

    # Tìm tour theo mã
    def lay_tour_theo_ma(self, ma_tour):
        for tour in self.ds_tour:
            if tour.ma_tour == ma_tour:
                return tour
        return None

if __name__ == "__main__":
    # 1. Kiểm thử đọc và lưu dữ liệu
    print("=== KIỂM THỬ ĐỌC VÀ LƯU DỮ LIỆU ===")

    du_lieu_mau = {
        "tours": [
            {
                "ma_tour": "ND01",
                "ten_tour": "Đà Nẵng - Hội An",
                "loai_tour": "NoiDia",
                "diem_den": "Đà Nẵng",
                "so_ngay": 3,
                "ngay_khoi_hanh": "2026-12-15",
                "gia_co_ban": 3000000,
                "so_cho_toi_da": 25,
                "so_cho_da_dat": 0,
                "phu_thu": 200000
            }
        ],
        "customers": [
            {"ma_khach_hang": "KH01"}
        ],
        "services": [],
        "bookings": [],
        "destinations": []
    }

    luu_json("test_data.json", du_lieu_mau)

    quan_ly = QuanLyTour("test_data.json")

    print("\n--- Kiểm thử tải dữ liệu ---")
    for tour in quan_ly.ds_tour:
        print(tour.ma_tour, tour.ten_tour)

    print("\n--- Kiểm thử lưu dữ liệu ---")
    print(quan_ly.luu_du_lieu())

    print("\n--- Dữ liệu sau khi lưu ---")
    du_lieu = doc_json("test_data.json", {})
    print(du_lieu)

    print("\n--- Kiểm tra dữ liệu khách hàng ---")
    print(du_lieu["customers"])

    # 2. Kiểm thử thêm tour
    print("\n=== KIỂM THỬ THÊM TOUR ===")

    tour_moi = TourNoiDia(
        ma_tour="ND02",
        ten_tour="Khám phá Đà Lạt",
        diem_den="Đà Lạt",
        so_ngay=3,
        ngay_khoi_hanh="2026-12-20",
        gia_co_ban=2500000,
        so_cho_toi_da=30,
        phu_thu=150000,
        so_cho_da_dat=0
    )

    print("Thêm tour mới:", quan_ly.them_tour(tour_moi))

    print("Thêm tour trùng:", quan_ly.them_tour(tour_moi))

    print("\nDanh sách tour:")
    for tour in quan_ly.ds_tour:
        print(tour.ma_tour, tour.ten_tour)

    # 3. Kiểm thử cập nhật tour
    print("\n=== KIỂM THỬ CẬP NHẬT TOUR ===")

    thong_tin_moi = {
        "ten_tour": "Khám phá Đà Lạt 4 ngày",
        "so_ngay": 4,
        "gia_co_ban": 3500000
    }

    print("Cập nhật tour ND02:",
          quan_ly.cap_nhat_tour("ND02", thong_tin_moi))

    tour = quan_ly.lay_tour_theo_ma("ND02")
    print(tour.to_dict())

    print("Cập nhật tour ND99:",
          quan_ly.cap_nhat_tour("ND99", thong_tin_moi))

    print("Cập nhật số chỗ tối đa:",
          quan_ly.cap_nhat_tour("ND02", {"so_cho_toi_da": -5}))

    print("Số chỗ tối đa hiện tại:", tour.so_cho_toi_da)

    # 4. Kiểm thử xóa tour
    print("\n=== KIỂM THỬ XÓA TOUR ===")

    tour = quan_ly.lay_tour_theo_ma("ND01")
    tour.so_cho_da_dat = 5

    print("Xóa tour đã có khách đặt:",
          quan_ly.xoa_tour("ND01"))

    tour.so_cho_da_dat = 0

    print("Xóa tour ND99:",
          quan_ly.xoa_tour("ND99"))

    print("Xóa tour ND02:",
          quan_ly.xoa_tour("ND02"))

    print("\nDanh sách tour còn lại:")
    for tour in quan_ly.ds_tour:
        print(tour.ma_tour, tour.ten_tour)

    print("\nDữ liệu JSON sau khi xóa:")
    print(doc_json("test_data.json", {}))

    # 5. Kiểm thử tìm kiếm tour
    print("\n=== KIỂM THỬ TÌM KIẾM TOUR ===")

    quan_ly.them_tour(tour_moi)

    print("\nTìm tour Đà Nẵng:")
    ket_qua = quan_ly.tim_kiem(diem_den="đà nẵng")

    for tour in ket_qua:
        print(tour.ma_tour, tour.ten_tour)

    print("\nTìm tour có giá tối đa 3500000:")
    ket_qua = quan_ly.tim_kiem(gia_toi_da=3500000)

    for tour in ket_qua:
        print(tour.ma_tour, tour.ten_tour, tour.tinh_gia_ve())

    print("\nTìm tour khởi hành ngày 2026-12-20:")
    ket_qua = quan_ly.tim_kiem(ngay_khoi_hanh="2026-12-20")

    for tour in ket_qua:
        print(tour.ma_tour, tour.ten_tour)

    print("\nTìm tour theo nhiều tiêu chí:")
    ket_qua = quan_ly.tim_kiem(
        diem_den="Đà Nẵng",
        gia_toi_da=3500000,
        ngay_khoi_hanh="2026-12-15"
    )

    for tour in ket_qua:
        print(tour.ma_tour, tour.ten_tour)

    print("\nTìm tour Phú Quốc:")
    ket_qua = quan_ly.tim_kiem(diem_den="Phú Quốc")
    print(ket_qua)

    # 6. Kiểm thử tỷ lệ lấp đầy
    print("\n=== KIỂM THỬ TỶ LỆ LẤP ĐẦY ===")

    tour1 = quan_ly.lay_tour_theo_ma("ND01")
    tour2 = quan_ly.lay_tour_theo_ma("ND02")

    print("Tỷ lệ khi chưa có khách:",
          quan_ly.thong_ke_ty_le_lap_day(), "%")

    tour1.so_cho_da_dat = 15
    tour2.so_cho_da_dat = 20

    print("Tỷ lệ khi có khách đặt:",
          quan_ly.thong_ke_ty_le_lap_day(), "%")

    tour1.so_cho_da_dat = 25
    tour2.so_cho_da_dat = 30

    print("Tỷ lệ khi đã hết chỗ:",
          quan_ly.thong_ke_ty_le_lap_day(), "%")

    tour1.so_cho_da_dat = 0
    tour2.so_cho_da_dat = 0

    # 7. Kiểm thử doanh thu
    print("\n=== KIỂM THỬ DOANH THU ===")

    tour1 = quan_ly.lay_tour_theo_ma("ND01")
    tour2 = quan_ly.lay_tour_theo_ma("ND02")

    print("Doanh thu khi chưa có khách:",
          quan_ly.thong_ke_doanh_thu())

    tour1.so_cho_da_dat = 15
    tour2.so_cho_da_dat = 20

    print("Doanh thu khi có khách:",
          quan_ly.thong_ke_doanh_thu())

    tour1.so_cho_da_dat = 25
    tour2.so_cho_da_dat = 30

    print("Doanh thu khi hết chỗ:",
          quan_ly.thong_ke_doanh_thu())

    tour1.so_cho_da_dat = 0
    tour2.so_cho_da_dat = 0

    # 8. Kiểm thử xuất báo cáo csv
    print("\n=== KIỂM THỬ XUẤT BÁO CÁO CSV ===")

    tour1.so_cho_da_dat = 15
    tour2.so_cho_da_dat = 20

    print("Xuất báo cáo:",
          xuat_bao_cao_csv(quan_ly.ds_tour, "test_bao_cao.csv"))

    tour1.so_cho_da_dat = 0
    tour2.so_cho_da_dat = 0
    
    
    # 9. Kiểm thử tour quốc tế
    print("\n=== KIỂM THỬ TOUR QUỐC TẾ ===")

    tour_qt = TourQuocTe(
        ma_tour="QT01",
        ten_tour="Bangkok - Pattaya",
        diem_den="Thái Lan",
        so_ngay=4,
        ngay_khoi_hanh="2026-12-25",
        gia_co_ban=6500000,
        so_cho_toi_da=30,
        phi_visa=1200000,
        so_cho_da_dat=0
    )

    print("Thêm tour quốc tế:", quan_ly.them_tour(tour_qt))
    print("Giá vé quốc tế:", tour_qt.tinh_gia_ve())

    ket_qua = quan_ly.tim_kiem(diem_den="Thái Lan")
    print("Kết quả tìm kiếm:")
    for tour in ket_qua:
        print(tour.ma_tour, tour.ten_tour)

    quan_ly.tai_du_lieu()
    tour_qt = quan_ly.lay_tour_theo_ma("QT01")

    print("Thông tin sau khi tải lại:")
    print(tour_qt.to_dict())
    print("Đúng loại tour quốc tế:", isinstance(tour_qt, TourQuocTe))
    
    # Kiểm thử cập nhật số chỗ không hợp lệ
    print("\n=== KIỂM THỬ KIỂU DỮ LIỆU ===")
    print("Số chỗ là chuỗi:",
      quan_ly.cap_nhat_tour("ND01", {"so_cho_toi_da": "abc"}))

    print("Số chỗ là số thực:",
      quan_ly.cap_nhat_tour("ND01", {"so_cho_toi_da": 2.5}))

    print("Số chỗ bằng 0:",
      quan_ly.cap_nhat_tour("ND01", {"so_cho_toi_da": 0}))
    
    # Kiểm thử xử lý lỗi lưu dữ liệu
    print("\n=== KIỂM THỬ LỖI LƯU DỮ LIỆU ===")

    luu_json("test_luu_loi.json", {})
    quan_ly_loi = QuanLyTour("test_luu_loi.json")

    with open("test_luu_loi.json", "w", encoding="utf-8") as f:
        f.write("Du lieu loi")

    print("Lưu dữ liệu:", quan_ly_loi.luu_du_lieu())
    print("Thêm tour khi file lỗi:", quan_ly_loi.them_tour(tour_qt))
    print("Danh sách sau khi thêm thất bại:", quan_ly_loi.ds_tour)
    print("Chương trình vẫn hoạt động")

