# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 21:43:53 2026

@author: asus
"""

import sys
import os
from datetime import datetime
sys.path.append("..")

from utils.file_helper import doc_json, luu_json, xuat_bao_cao_csv, xuat_lich_trinh_text
from models.tour import TourNoiDia, TourQuocTe
from models.customer import KhachHang, DichVu
from models.booking import LichTrinhNgay, PhieuDatTour
from config import DATA_FILE, STATUS_PENDING, STATUS_CONFIRMED, STATUS_CANCELLED

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
            # Khôi phục lịch trình của tour
            for lt in item.get("ds_lich_trinh", []):
                lich_trinh = LichTrinhNgay(
                    thu_tu_ngay=lt.get("thu_tu_ngay"),
                    tieu_de=lt.get("tieu_de"),
                    buoi_sang=lt.get("buoi_sang"),
                    buoi_chieu=lt.get("buoi_chieu"),
                    buoi_toi=lt.get("buoi_toi")
                )
        
                tour.them_lich_trinh(lich_trinh)
            self.ds_tour.append(tour)
            
        # Khôi phục dữ liệu khách hàng
        self.ds_khach_hang = []
        
        for item in du_lieu_tho.get("customers", []):
            khach_hang = KhachHang(
                ma_kh=item.get("ma_kh"),
                ho_ten=item.get("ho_ten"),
                sdt=item.get("sdt"),
                email=item.get("email")
            )
        
            self.ds_khach_hang.append(khach_hang)
            
        # Khôi phục dữ liệu dịch vụ
        self.ds_dich_vu = []
    
        for item in du_lieu_tho.get("services", []):
            dich_vu = DichVu(
                ma_dv=item.get("ma_dv"),
                ten_dv=item.get("ten_dv"),
                don_gia=item.get("don_gia")
            )
    
            self.ds_dich_vu.append(dich_vu)
            
        # Khôi phục dữ liệu phiếu đặt tour
        self.ds_phieu_dat = []
        
        for item in du_lieu_tho.get("bookings", []):
            # Tìm tour và khách hàng theo mã
            tour = self.lay_tour_theo_ma(
                item.get("ma_tour")
            )
        
            khach_hang = self.lay_khach_hang_theo_ma(
                item.get("ma_khach_hang")
            )
        
            if tour is None or khach_hang is None:
                raise ValueError(
                    "Phiếu đặt có tour hoặc khách hàng không tồn tại!"
                )
        
            # Khôi phục danh sách dịch vụ
            ds_dich_vu = []
        
            for ma_dv in item.get("ds_ma_dich_vu", []):
                dich_vu = self.lay_dich_vu_theo_ma(ma_dv)
        
                if dich_vu is None:
                    raise ValueError(
                        "Phiếu đặt có dịch vụ không tồn tại!"
                    )
        
                ds_dich_vu.append(dich_vu)
        
            # Khôi phục đối tượng phiếu đặt
            phieu = PhieuDatTour(
                ma_dat_cho=item.get("ma_dat_cho"),
                khach_hang=khach_hang,
                tour=tour,
                so_luong_ve=item.get("so_luong_ve"),
                ds_dich_vu=ds_dich_vu,
                ngay_dat=item.get("ngay_dat")
            )
        
            # Khôi phục tổng tiền và trạng thái đã lưu
            phieu.tong_tien = item.get("tong_tien")
            phieu.trang_thai = item.get(
                "trang_thai", STATUS_PENDING
            )
        
            self.ds_phieu_dat.append(phieu)
            
        # Khôi phục danh sách điểm đến
        self.ds_diem_den = du_lieu_tho.get("destinations", [])

    # Lưu dữ liệu nghiệp vụ vào file JSON
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
            du_lieu["customers"] = [kh.to_dict() for kh in self.ds_khach_hang]
            du_lieu["services"] = [dv.to_dict() for dv in self.ds_dich_vu]
            du_lieu["bookings"] = [phieu.to_dict() for phieu in self.ds_phieu_dat]

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
                
                # Kiểm tra phiếu đặt liên quan đến tour
                for phieu in self.ds_phieu_dat:
                    if phieu.tour.ma_tour == ma_tour:
                        print("Không thể xóa tour có phiếu đặt liên quan!")
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

                # Kiểm tra số ngày mới của tour
                so_ngay_moi = thong_tin_moi.get(
                    "so_ngay", tour.so_ngay
                )

                if type(so_ngay_moi) != int:
                    print("Số ngày phải là số nguyên!")
                    return False

                if so_ngay_moi <= 0:
                    print("Số ngày phải lớn hơn 0!")
                    return False

                # Kiểm tra số ngày dựa trên lịch trình hiện có
                for lt in tour.ds_lich_trinh:
                    if lt.thu_tu_ngay > so_ngay_moi:
                        print("Số ngày mới không được nhỏ hơn ngày cuối trong lịch trình!")
                        return False
                
                if so_cho_moi < tour.so_cho_da_dat:
                    print("Số chỗ tối đa không được nhỏ hơn số chỗ đã đặt!")
                    return False
                
                # Lấy thông tin mới cần cập nhật
                ten_tour_moi = thong_tin_moi.get(
                    "ten_tour", tour.ten_tour
                )
                
                diem_den_moi = thong_tin_moi.get(
                    "diem_den", tour.diem_den
                )
                
                gia_moi = thong_tin_moi.get(
                    "gia_co_ban", tour.gia_co_ban
                )
                
                ngay_khoi_hanh_moi = thong_tin_moi.get(
                    "ngay_khoi_hanh", tour.ngay_khoi_hanh
                )
                
                # Kiểm tra tên tour
                if type(ten_tour_moi) != str or ten_tour_moi.strip() == "":
                    print("Tên tour không được để trống!")
                    return False
                
                # Kiểm tra điểm đến
                if type(diem_den_moi) != str or diem_den_moi.strip() == "":
                    print("Điểm đến không được để trống!")
                    return False
                
                # Kiểm tra kiểu dữ liệu của giá
                if type(gia_moi) != int and type(gia_moi) != float:
                    print("Giá cơ bản phải là số!")
                    return False
                
                # Kiểm tra giá cơ bản
                if gia_moi <= 0:
                    print("Giá cơ bản phải lớn hơn 0!")
                    return False
                
                # Kiểm tra ngày khởi hành
                if type(ngay_khoi_hanh_moi) != str:
                    print("Ngày khởi hành phải là chuỗi!")
                    return False
                
                try:
                    datetime.strptime(ngay_khoi_hanh_moi, "%Y-%m-%d")
                
                except ValueError:
                    try:
                        datetime.strptime(ngay_khoi_hanh_moi, "%d/%m/%Y")
                
                    except ValueError:
                        print("Ngày khởi hành không hợp lệ!")
                        return False

                try:
                    tour.ten_tour = ten_tour_moi.strip()
                    tour.diem_den = diem_den_moi.strip()
                    tour.so_ngay = so_ngay_moi
                    tour.ngay_khoi_hanh = ngay_khoi_hanh_moi
                    tour.gia_co_ban = gia_moi
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

        for phieu in self.ds_phieu_dat:
            if phieu.trang_thai == STATUS_CONFIRMED:
                tong_doanh_thu += phieu.tong_tien

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
    
    # Tìm khách hàng theo mã
    def lay_khach_hang_theo_ma(self, ma_kh):
        for kh in self.ds_khach_hang:
            if kh.ma_kh == ma_kh:
                return kh
        return None
    
    # Thêm khách hàng
    def them_khach_hang(self, khach_hang):
        if self.lay_khach_hang_theo_ma(khach_hang.ma_kh) is not None:
            print("Mã khách hàng đã tồn tại!")
            return False
    
        self.ds_khach_hang.append(khach_hang)
    
        if self.luu_du_lieu():
            return True
        else:
            self.ds_khach_hang.remove(khach_hang)
            return False
        
    # Tìm dịch vụ theo mã
    def lay_dich_vu_theo_ma(self, ma_dv):
        for dv in self.ds_dich_vu:
            if dv.ma_dv == ma_dv:
                return dv
        return None
    
    # Thêm dịch vụ
    def them_dich_vu(self, dich_vu):
        if self.lay_dich_vu_theo_ma(dich_vu.ma_dv) is not None:
            print("Mã dịch vụ đã tồn tại!")
            return False
    
        self.ds_dich_vu.append(dich_vu)
    
        if self.luu_du_lieu():
            return True
        else:
            self.ds_dich_vu.remove(dich_vu)
            return False
        
    # Lấy danh sách phiếu đặt tour
    def lay_ds_phieu_dat(self):
        return self.ds_phieu_dat
    
    # Tìm phiếu đặt theo mã
    def tim_phieu_dat(self, ma_phieu):
        for phieu in self.ds_phieu_dat:
            if phieu.ma_dat_cho == ma_phieu:
                return phieu
        return None

    # Tìm danh sách phiếu đặt theo mã khách hàng
    def tim_phieu_theo_khach(self, ma_khach):
        ket_qua = []

        for phieu in self.ds_phieu_dat:
            if phieu.khach_hang.ma_kh == ma_khach:
                ket_qua.append(phieu)

        return ket_qua
    
    # Thêm phiếu đặt tour
    def them_phieu_dat(self, phieu):
        # Kiểm tra trùng mã phiếu
        if self.tim_phieu_dat(phieu.ma_dat_cho) is not None:
            print("Mã phiếu đặt đã tồn tại!")
            return False
    
        # Kiểm tra tour
        tour = self.lay_tour_theo_ma(phieu.tour.ma_tour)
    
        if tour is None:
            print("Tour không tồn tại!")
            return False
    
        # Kiểm tra khách hàng
        khach_hang = self.lay_khach_hang_theo_ma(
            phieu.khach_hang.ma_kh
        )
    
        if khach_hang is None:
            print("Khách hàng không tồn tại!")
            return False
    
        # Kiểm tra danh sách dịch vụ
        ds_dich_vu = []
    
        for dv in phieu.ds_dich_vu:
            dich_vu = self.lay_dich_vu_theo_ma(dv.ma_dv)
    
            if dich_vu is None:
                print("Dịch vụ không tồn tại!")
                return False
    
            ds_dich_vu.append(dich_vu)
    
        # Kiểm tra trạng thái phiếu mới
        if phieu.trang_thai != STATUS_PENDING:
            print("Phiếu đặt mới phải ở trạng thái chờ xác nhận!")
            return False
    
        # Liên kết với các đối tượng đang được quản lý
        phieu.tour = tour
        phieu.khach_hang = khach_hang
        phieu.ds_dich_vu = ds_dich_vu
    
        self.ds_phieu_dat.append(phieu)
    
        if self.luu_du_lieu():
            return True
        else:
            self.ds_phieu_dat.remove(phieu)
            return False
        
    # Xác nhận phiếu đặt tour
    def xac_nhan_phieu_dat(self, ma_phieu):
        phieu = self.tim_phieu_dat(ma_phieu)

        if phieu is None:
            print("Không tìm thấy phiếu đặt!")
            return False

        # Lưu trạng thái trước khi xác nhận
        trang_thai_cu = phieu.trang_thai
        tong_tien_cu = phieu.tong_tien
        so_cho_cu = phieu.tour.so_cho_da_dat

        try:
            if phieu.xac_nhan_dat():
                if self.luu_du_lieu():
                    return True
            else:
                print("Không thể xác nhận phiếu đặt!")

        except Exception as e:
            print("Lỗi khi xác nhận phiếu đặt:", e)

        # Khôi phục dữ liệu nếu thất bại
        phieu.trang_thai = trang_thai_cu
        phieu.tong_tien = tong_tien_cu
        phieu.tour.so_cho_da_dat = so_cho_cu

        return False
    
    # Hủy phiếu đặt tour
    def huy_phieu_dat(self, ma_phieu):
        phieu = self.tim_phieu_dat(ma_phieu)
    
        if phieu is None:
            print("Không tìm thấy phiếu đặt!")
            return False
    
        # Lưu trạng thái trước khi hủy
        trang_thai_cu = phieu.trang_thai
        so_cho_cu = phieu.tour.so_cho_da_dat
    
        try:
            if phieu.huy_dat():
                if self.luu_du_lieu():
                    return True
            else:
                print("Không thể hủy phiếu đặt!")
    
        except Exception as e:
            print("Lỗi khi hủy phiếu đặt:", e)
    
        # Khôi phục dữ liệu nếu thất bại
        phieu.trang_thai = trang_thai_cu
        phieu.tour.so_cho_da_dat = so_cho_cu
    
        return False
    
    # Lấy danh sách điểm đến
    def lay_ds_diem_den(self):
        return self.ds_diem_den

if __name__ == "__main__":
    ket_qua_test = []
    ket_qua_nhom = []

    # Hàm kiểm tra kết quả
    def kiem_tra(ten, thuc_te, mong_doi=True):
        if thuc_te == mong_doi:
            print(ten, ": Đạt")
            ket_qua_test.append(True)
            ket_qua_nhom.append(True)
            return True
        else:
            print(ten, ": Không đạt")
            ket_qua_test.append(False)
            ket_qua_nhom.append(False)
            return False

    # Hàm tổng kết kiểm thử
    def tong_ket_nhom(ds_ket_qua):
        so_dat = 0
        so_khong_dat = 0

        for ket_qua in ds_ket_qua:
            if ket_qua == True:
                so_dat += 1
            else:
                so_khong_dat += 1

        print("Đạt:", so_dat, "| Không đạt:", so_khong_dat)

    # Hàm tạo dữ liệu kiểm thử mới
    def tao_quan_ly(ten_file, du_lieu):

        if os.path.exists(ten_file):
            os.remove(ten_file)

        if os.path.exists(ten_file + ".bak"):
            os.remove(ten_file + ".bak")

        if os.path.exists(ten_file + ".tmp"):
            os.remove(ten_file + ".tmp")

        ket_qua = luu_json(ten_file, du_lieu)

        kiem_tra("Tạo " + ten_file, ket_qua)

        if ket_qua == False:
            raise ValueError("Không tạo được dữ liệu kiểm thử")

        return QuanLyTour(ten_file)

    # Hàm lấy danh sách mã tour
    def ma_tour(ds_tour):
        ds_ma = []

        for tour in ds_tour:
            ds_ma.append(tour.ma_tour)

        return ds_ma

    # Hàm chuyển dữ liệu đang quản lý thành Dictionary
    def du_lieu_quan_ly(ql):
        ds_tour = []
        ds_khach_hang = []
        ds_dich_vu = []
        ds_phieu_dat = []

        for tour in ql.ds_tour:
            ds_tour.append(tour.to_dict())

        for khach_hang in ql.ds_khach_hang:
            ds_khach_hang.append(khach_hang.to_dict())

        for dich_vu in ql.ds_dich_vu:
            ds_dich_vu.append(dich_vu.to_dict())

        for phieu in ql.ds_phieu_dat:
            ds_phieu_dat.append(phieu.to_dict())

        return {
            "tours": ds_tour,
            "customers": ds_khach_hang,
            "services": ds_dich_vu,
            "bookings": ds_phieu_dat,
            "destinations": ql.ds_diem_den
        }

    # Dữ liệu đầu vào phục vụ kiểm thử
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
            {
                "ma_kh": "KH01",
                "ho_ten": "Nguyen Van An",
                "sdt": "0912345678",
                "email": "an@example.com"
            }
        ],

        "services": [
            {
                "ma_dv": "DV01",
                "ten_dv": "Bảo hiểm du lịch",
                "don_gia": 150000
            },
            {
                "ma_dv": "DV02",
                "ten_dv": "Đưa đón sân bay",
                "don_gia": 300000
            }
        ],

        "bookings": [],
        "destinations": []
    }

    # Dữ liệu điểm đến giả lập, chưa gọi API thật
    ds_diem_den_mau = [
        {
            "tu_khoa": "Đà Lạt",
            "ten_dia_diem": "Đà Lạt",
            "dia_chi": "Lâm Đồng, Việt Nam",
            "toa_do": {
                "lat": 11.94,
                "lon": 108.43
            },
            "nguon": "OpenStreetMap Nominatim API"
        }
    ]


    # ==================================================
    # 1. KIỂM THỬ ĐỌC VÀ LƯU DỮ LIỆU
    # ==================================================

    print("\n=== 1. KIỂM THỬ ĐỌC VÀ LƯU DỮ LIỆU ===")
    ket_qua_nhom = []

    # 1.1. Đọc dữ liệu từ JSON
    print("\n--- 1.1. Đọc dữ liệu từ JSON ---")

    ql = tao_quan_ly("test_data.json", du_lieu_mau)

    kiem_tra("Khôi phục tour", ma_tour(ql.ds_tour), ["ND01"])

    du_lieu_thuc_te = du_lieu_quan_ly(ql)

    kiem_tra(
        "Khôi phục khách hàng",
        du_lieu_thuc_te["customers"],
        du_lieu_mau["customers"]
    )

    kiem_tra(
        "Khôi phục dịch vụ",
        du_lieu_thuc_te["services"],
        du_lieu_mau["services"]
    )

    # 1.2. Lưu dữ liệu vào JSON
    print("\n--- 1.2. Lưu dữ liệu vào JSON ---")

    ket_qua = ql.luu_du_lieu()
    kiem_tra("Lưu dữ liệu", ket_qua)

    du_lieu_json = doc_json(ql.file_path)

    kiem_tra(
        "Kiểm tra nội dung JSON",
        du_lieu_json,
        du_lieu_quan_ly(ql)
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 2. KIỂM THỬ QUẢN LÝ TOUR
    # ==================================================

    print("\n=== 2. KIỂM THỬ QUẢN LÝ TOUR ===")
    ket_qua_nhom = []

    # 2.1. Thêm tour
    print("\n--- 2.1. Thêm tour ---")

    nd02 = TourNoiDia(
        "ND02", "Khám phá Đà Lạt", "Đà Lạt",
        3, "2026-12-20", 2500000, 30, 150000
    )

    ket_qua = ql.them_tour(nd02)
    kiem_tra("Thêm tour nội địa", ket_qua)

    ket_qua = ql.them_tour(nd02)
    kiem_tra("Từ chối thêm tour trùng mã", ket_qua, False)

    qt = TourQuocTe(
        "QT01", "Bangkok - Pattaya", "Thái Lan",
        4, "2026-12-25", 6500000, 30, 1200000
    )

    ket_qua = ql.them_tour(qt)
    kiem_tra("Thêm tour quốc tế", ket_qua)

    kiem_tra("Tính giá tour quốc tế", qt.tinh_gia_ve(), 7700000)

    # 2.2. Cập nhật tour
    print("\n--- 2.2. Cập nhật tour ---")

    thong_tin_moi = {
        "ten_tour": "Khám phá Đà Lạt 4 ngày",
        "so_ngay": 4,
        "gia_co_ban": 3500000
    }

    ket_qua = ql.cap_nhat_tour("ND02", thong_tin_moi)
    kiem_tra("Cập nhật tour hợp lệ", ket_qua)

    kiem_tra(
        "Kiểm tra thông tin sau cập nhật",
        [nd02.ten_tour, nd02.so_ngay, nd02.gia_co_ban],
        ["Khám phá Đà Lạt 4 ngày", 4, 3500000]
    )

    ket_qua = ql.cap_nhat_tour("ND99", thong_tin_moi)
    kiem_tra("Cập nhật tour không tồn tại", ket_qua, False)

    ket_qua = ql.cap_nhat_tour(
        "ND02", {"so_cho_toi_da": 0}
    )

    kiem_tra("Từ chối số chỗ không hợp lệ", ket_qua, False)
    
    # Kiểm tra tên tour rỗng
    ket_qua = ql.cap_nhat_tour("ND02", {"ten_tour": ""})
    kiem_tra("Từ chối tên tour rỗng", ket_qua, False)
    
    # Kiểm tra điểm đến rỗng
    ket_qua = ql.cap_nhat_tour("ND02", {"diem_den": ""})
    kiem_tra("Từ chối điểm đến rỗng", ket_qua, False)
    
    # Kiểm tra giá cơ bản âm
    ket_qua = ql.cap_nhat_tour("ND02", {"gia_co_ban": -500000})
    kiem_tra("Từ chối giá cơ bản âm", ket_qua, False)
    
    # Kiểm tra ngày khởi hành không hợp lệ
    ket_qua = ql.cap_nhat_tour(
        "ND02", {"ngay_khoi_hanh": "2026-02-30"}
    )
    kiem_tra("Từ chối ngày khởi hành không hợp lệ", ket_qua, False)

    # 2.3. Kiểm tra ràng buộc số chỗ
    print("\n--- 2.3. Kiểm tra ràng buộc số chỗ ---")

    nd01 = ql.lay_tour_theo_ma("ND01")

    # Giả lập tour đã có 5 khách
    nd01.so_cho_da_dat = 5

    ket_qua = ql.cap_nhat_tour(
        "ND01", {"so_cho_toi_da": 4}
    )

    kiem_tra("Không giảm chỗ dưới số đã đặt", ket_qua, False)

    ket_qua = ql.xoa_tour("ND01")
    kiem_tra("Không xóa tour đã có khách", ket_qua, False)

    nd01.so_cho_da_dat = 0

    # 2.4. Xóa tour
    print("\n--- 2.4. Xóa tour ---")

    ket_qua = ql.xoa_tour("ND02")
    kiem_tra("Xóa tour hợp lệ", ket_qua)

    ket_qua = ql.xoa_tour("ND99")
    kiem_tra("Xóa tour không tồn tại", ket_qua, False)

    # Thêm lại tour để kiểm thử tìm kiếm
    ql.them_tour(nd02)

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 3. KIỂM THỬ TÌM KIẾM TOUR
    # ==================================================

    print("\n=== 3. KIỂM THỬ TÌM KIẾM TOUR ===")
    ket_qua_nhom = []

    # 3.1. Tìm theo điểm đến
    ds_tim_kiem = ql.tim_kiem(diem_den="đà nẵng")

    kiem_tra(
        "Tìm theo điểm đến",
        ma_tour(ds_tim_kiem),
        ["ND01"]
    )

    # 3.2. Tìm theo giá vé
    ds_tim_kiem = ql.tim_kiem(gia_toi_da=3500000)

    kiem_tra(
        "Tìm theo giá vé",
        ma_tour(ds_tim_kiem),
        ["ND01"]
    )

    # 3.3. Tìm theo ngày khởi hành
    ds_tim_kiem = ql.tim_kiem(
        ngay_khoi_hanh="2026-12-20"
    )

    kiem_tra(
        "Tìm theo ngày khởi hành",
        ma_tour(ds_tim_kiem),
        ["ND02"]
    )

    # 3.4. Tìm theo nhiều tiêu chí
    ds_tim_kiem = ql.tim_kiem(
        diem_den="Đà Nẵng",
        gia_toi_da=3500000,
        ngay_khoi_hanh="2026-12-15"
    )

    kiem_tra(
        "Tìm theo nhiều tiêu chí",
        ma_tour(ds_tim_kiem),
        ["ND01"]
    )

    # 3.5. Tìm kiếm không có kết quả
    ds_tim_kiem = ql.tim_kiem(diem_den="Phú Quốc")

    kiem_tra("Tìm tour không tồn tại", ds_tim_kiem, [])

    # 3.6. Tìm tour quốc tế
    ds_tim_kiem = ql.tim_kiem(diem_den="Thái Lan")

    kiem_tra(
        "Tìm tour quốc tế",
        ma_tour(ds_tim_kiem),
        ["QT01"]
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 4. KIỂM THỬ QUẢN LÝ KHÁCH HÀNG
    # ==================================================

    print("\n=== 4. KIỂM THỬ QUẢN LÝ KHÁCH HÀNG ===")
    ket_qua_nhom = []

    # 4.1. Thêm khách hàng
    print("\n--- 4.1. Thêm khách hàng ---")

    kh = KhachHang(
        "KH02", "Tran Van Binh",
        "0987654321", "binh@example.com"
    )

    ket_qua = ql.them_khach_hang(kh)
    kiem_tra("Thêm khách hàng", ket_qua)

    ket_qua = ql.them_khach_hang(kh)
    kiem_tra("Từ chối trùng mã khách hàng", ket_qua, False)

    # 4.2. Tìm khách hàng
    print("\n--- 4.2. Tìm khách hàng ---")

    kh_tim_duoc = ql.lay_khach_hang_theo_ma("KH02")

    kiem_tra(
        "Tìm khách hàng KH02",
        kh_tim_duoc.to_dict(),
        kh.to_dict()
    )

    kh_tim_duoc = ql.lay_khach_hang_theo_ma("KH99")

    kiem_tra("Tìm khách hàng không tồn tại", kh_tim_duoc, None)

    # 4.3. Khôi phục khách hàng
    print("\n--- 4.3. Khôi phục khách hàng ---")

    ql.tai_du_lieu()

    kh_khoi_phuc = ql.lay_khach_hang_theo_ma("KH02")

    kiem_tra(
        "Khôi phục khách hàng từ JSON",
        kh_khoi_phuc.to_dict(),
        kh.to_dict()
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 5. KIỂM THỬ QUẢN LÝ DỊCH VỤ
    # ==================================================

    print("\n=== 5. KIỂM THỬ QUẢN LÝ DỊCH VỤ ===")
    ket_qua_nhom = []

    # 5.1. Thêm dịch vụ
    print("\n--- 5.1. Thêm dịch vụ ---")

    dv = DichVu("DV03", "Dịch vụ ăn uống", 200000)

    ket_qua = ql.them_dich_vu(dv)
    kiem_tra("Thêm dịch vụ", ket_qua)

    ket_qua = ql.them_dich_vu(dv)
    kiem_tra("Từ chối trùng mã dịch vụ", ket_qua, False)

    # 5.2. Tìm dịch vụ
    print("\n--- 5.2. Tìm dịch vụ ---")

    dv_tim_duoc = ql.lay_dich_vu_theo_ma("DV03")

    kiem_tra(
        "Tìm dịch vụ DV03",
        dv_tim_duoc.to_dict(),
        dv.to_dict()
    )

    dv_tim_duoc = ql.lay_dich_vu_theo_ma("DV99")

    kiem_tra("Tìm dịch vụ không tồn tại", dv_tim_duoc, None)

    # 5.3. Khôi phục dịch vụ
    print("\n--- 5.3. Khôi phục dịch vụ ---")

    ql.tai_du_lieu()

    dv_khoi_phuc = ql.lay_dich_vu_theo_ma("DV03")

    kiem_tra(
        "Khôi phục dịch vụ từ JSON",
        dv_khoi_phuc.to_dict(),
        dv.to_dict()
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 6. KIỂM THỬ QUẢN LÝ LỊCH TRÌNH
    # ==================================================

    print("\n=== 6. KIỂM THỬ QUẢN LÝ LỊCH TRÌNH ===")
    ket_qua_nhom = []

    # 6.1. Chuẩn bị dữ liệu
    ql_lt = tao_quan_ly(
        "test_lich_trinh.json", du_lieu_mau
    )

    tour_lt = ql_lt.lay_tour_theo_ma("ND01")

    ngay1 = LichTrinhNgay(
        1, "Khám phá Đà Nẵng",
        "Đón khách", "Tham quan Sơn Trà", "Dạo biển"
    )

    ngay2 = LichTrinhNgay(
        2, "Tham quan Hội An",
        "Tham quan phố cổ", "Ăn đặc sản", "Ngắm đèn lồng"
    )

    # 6.2. Thêm và sắp xếp lịch trình
    print("\n--- 6.2. Thêm lịch trình ---")

    tour_lt.them_lich_trinh(ngay2)
    tour_lt.them_lich_trinh(ngay1)

    ds_ngay = []

    for lich_trinh in tour_lt.lay_lich_trinh():
        ds_ngay.append(lich_trinh.thu_tu_ngay)

    kiem_tra("Thêm và sắp xếp lịch trình", ds_ngay, [1, 2])

    # 6.3. Thêm lịch trình trùng ngày
    print("\n--- 6.3. Thêm lịch trình không hợp lệ ---")

    try:
        tour_lt.them_lich_trinh(ngay1)
        kiem_tra("Từ chối thêm ngày trùng", False)

    except ValueError:
        kiem_tra("Từ chối thêm ngày trùng", True)

    ngay4 = LichTrinhNgay(
        4, "Tham quan",
        "Ăn sáng", "Tham quan thành phố", "Nghỉ ngơi"
    )

    try:
        tour_lt.them_lich_trinh(ngay4)
        kiem_tra("Từ chối ngày vượt giới hạn", False)

    except ValueError:
        kiem_tra("Từ chối ngày vượt giới hạn", True)

    # 6.4. Sửa lịch trình
    print("\n--- 6.4. Sửa lịch trình ---")

    ket_qua = tour_lt.sua_lich_trinh(
        1, tieu_de="Khám phá thành phố Đà Nẵng"
    )

    kiem_tra("Sửa lịch trình ngày 1", ket_qua)

    try:
        tour_lt.sua_lich_trinh(1, tieu_de="")
        kiem_tra("Từ chối tiêu đề rỗng", False)

    except ValueError:
        kiem_tra("Từ chối tiêu đề rỗng", True)

    # 6.5. Kiểm tra số ngày của tour
    print("\n--- 6.5. Ràng buộc số ngày ---")

    ket_qua = ql_lt.cap_nhat_tour(
        "ND01", {"so_ngay": 1}
    )

    kiem_tra(
        "Không giảm số ngày dưới lịch trình hiện có",
        ket_qua,
        False
    )

    # 6.6. Lưu lịch trình
    print("\n--- 6.6. Lưu lịch trình ---")

    ket_qua = ql_lt.luu_du_lieu()
    kiem_tra("Lưu lịch trình vào JSON", ket_qua)

    # Giữ tour có hai ngày để kiểm thử xuất TXT
    ql_txt = QuanLyTour(ql_lt.file_path)
    tour_txt = ql_txt.lay_tour_theo_ma("ND01")

    # 6.7. Xóa lịch trình
    print("\n--- 6.7. Xóa lịch trình ---")

    ket_qua = tour_lt.xoa_lich_trinh(2)
    kiem_tra("Xóa lịch trình ngày 2", ket_qua)

    try:
        tour_lt.xoa_lich_trinh(99)
        kiem_tra("Từ chối xóa ngày không tồn tại", False)

    except ValueError:
        kiem_tra("Từ chối xóa ngày không tồn tại", True)

    # 6.8. Khôi phục lịch trình
    print("\n--- 6.8. Khôi phục lịch trình ---")

    ket_qua = ql_lt.luu_du_lieu()
    kiem_tra("Lưu lịch trình sau khi xóa", ket_qua)

    ql_lt.tai_du_lieu()

    tour_lt = ql_lt.lay_tour_theo_ma("ND01")

    lt_mong_doi = {
        "thu_tu_ngay": 1,
        "tieu_de": "Khám phá thành phố Đà Nẵng",
        "buoi_sang": "Đón khách",
        "buoi_chieu": "Tham quan Sơn Trà",
        "buoi_toi": "Dạo biển"
    }

    kiem_tra(
        "Khôi phục lịch trình sau khi sửa và xóa",
        len(tour_lt.ds_lich_trinh) == 1
        and tour_lt.ds_lich_trinh[0].to_dict() == lt_mong_doi
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 7. KIỂM THỬ QUẢN LÝ PHIẾU ĐẶT TOUR
    # ==================================================

    print("\n=== 7. KIỂM THỬ QUẢN LÝ PHIẾU ĐẶT TOUR ===")
    ket_qua_nhom = []

    # 7.1. Chuẩn bị dữ liệu
    ql_pd = tao_quan_ly(
        "test_phieu_dat.json", du_lieu_mau
    )

    tour_pd = ql_pd.lay_tour_theo_ma("ND01")
    khach_pd = ql_pd.lay_khach_hang_theo_ma("KH01")
    dich_vu_pd = ql_pd.lay_dich_vu_theo_ma("DV01")

    # 7.2. Thêm phiếu đặt
    print("\n--- 7.2. Thêm phiếu đặt ---")

    p1 = PhieuDatTour(
        "PD01", khach_pd, tour_pd, 2, [dich_vu_pd]
    )

    ket_qua = ql_pd.them_phieu_dat(p1)
    kiem_tra("Thêm phiếu đặt hợp lệ", ket_qua)

    ket_qua = ql_pd.them_phieu_dat(p1)
    kiem_tra("Từ chối phiếu trùng mã", ket_qua, False)

    # Kiểm tra phiếu có tour không tồn tại
    tour_sai = TourNoiDia(
        "ND99", "Tour mẫu", "Đà Lạt",
        3, "2026-12-20", 2000000, 20, 0
    )

    p_sai = PhieuDatTour(
        "PD99", khach_pd, tour_sai, 1
    )

    ket_qua = ql_pd.them_phieu_dat(p_sai)
    kiem_tra("Từ chối phiếu có tour không tồn tại", ket_qua, False)

    # Kiểm tra phiếu có khách hàng không tồn tại
    kh_sai = KhachHang(
        "KH99", "Nguyen Van Nam",
        "0912345678", "nam@example.com"
    )

    p_sai = PhieuDatTour(
        "PD98", kh_sai, tour_pd, 1
    )

    ket_qua = ql_pd.them_phieu_dat(p_sai)
    kiem_tra("Từ chối khách hàng không tồn tại", ket_qua, False)

    # Kiểm tra phiếu có dịch vụ không tồn tại
    dv_sai = DichVu("DV99", "Dịch vụ mẫu", 100000)

    p_sai = PhieuDatTour(
        "PD97", khach_pd, tour_pd, 1, [dv_sai]
    )

    ket_qua = ql_pd.them_phieu_dat(p_sai)
    kiem_tra("Từ chối dịch vụ không tồn tại", ket_qua, False)

    # 7.3. Tìm phiếu đặt
    print("\n--- 7.3. Tìm phiếu đặt ---")

    phieu = ql_pd.tim_phieu_dat("PD01")
    kiem_tra("Tìm phiếu theo mã", phieu, p1)

    ds_phieu = ql_pd.tim_phieu_theo_khach("KH01")
    kiem_tra("Tìm phiếu theo khách hàng", ds_phieu, [p1])

    # 7.4. Xác nhận phiếu đặt
    print("\n--- 7.4. Xác nhận phiếu đặt ---")

    ket_qua = ql_pd.xac_nhan_phieu_dat("PD01")
    kiem_tra("Xác nhận phiếu đặt", ket_qua)

    # Kiểm tra trạng thái, tổng tiền và số chỗ
    kiem_tra(
        "Dữ liệu sau xác nhận",
        [p1.trang_thai, p1.tong_tien, tour_pd.so_cho_da_dat],
        [STATUS_CONFIRMED, 6700000, 2]
    )

    ket_qua = ql_pd.xac_nhan_phieu_dat("PD01")
    kiem_tra("Từ chối xác nhận hai lần", ket_qua, False)

    # 7.5. Xác nhận khi không đủ chỗ
    print("\n--- 7.5. Xác nhận khi không đủ chỗ ---")

    p2 = PhieuDatTour(
        "PD02", khach_pd, tour_pd, 24
    )

    ket_qua = ql_pd.them_phieu_dat(p2)
    kiem_tra("Thêm phiếu chờ PD02", ket_qua)

    ket_qua = ql_pd.xac_nhan_phieu_dat("PD02")
    kiem_tra("Từ chối xác nhận khi không đủ chỗ", ket_qua, False)

    # 7.6. Hủy phiếu đặt
    print("\n--- 7.6. Hủy phiếu đặt ---")

    ket_qua = ql_pd.huy_phieu_dat("PD02")

    kiem_tra(
        "Hủy phiếu chờ không làm giảm chỗ",
        [ket_qua, p2.trang_thai, tour_pd.so_cho_da_dat],
        [True, STATUS_CANCELLED, 2]
    )

    ket_qua = ql_pd.huy_phieu_dat("PD01")

    kiem_tra(
        "Hủy phiếu xác nhận và trả chỗ",
        [ket_qua, p1.trang_thai, tour_pd.so_cho_da_dat],
        [True, STATUS_CANCELLED, 0]
    )

    ket_qua = ql_pd.huy_phieu_dat("PD01")
    kiem_tra("Từ chối hủy phiếu lần hai", ket_qua, False)

    # 7.7. Không xóa tour có phiếu liên quan
    print("\n--- 7.7. Ràng buộc xóa tour ---")

    ket_qua = ql_pd.xoa_tour("ND01")
    kiem_tra("Không xóa tour có phiếu liên quan", ket_qua, False)

    # 7.8. Khôi phục phiếu đặt
    print("\n--- 7.8. Khôi phục phiếu đặt ---")

    du_lieu_truoc = du_lieu_quan_ly(ql_pd)

    ql_pd.tai_du_lieu()

    du_lieu_sau = du_lieu_quan_ly(ql_pd)

    kiem_tra(
        "Khôi phục phiếu và dữ liệu liên quan",
        du_lieu_sau,
        du_lieu_truoc
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 8. KIỂM THỬ THỐNG KÊ DOANH THU
    # ==================================================

    print("\n=== 8. KIỂM THỬ THỐNG KÊ DOANH THU ===")
    ket_qua_nhom = []

    # 8.1. Doanh thu ban đầu
    ql_tk = tao_quan_ly(
        "test_thong_ke.json", du_lieu_mau
    )

    tour_tk = ql_tk.lay_tour_theo_ma("ND01")
    khach_tk = ql_tk.lay_khach_hang_theo_ma("KH01")
    dich_vu_tk = ql_tk.lay_dich_vu_theo_ma("DV01")

    doanh_thu = ql_tk.thong_ke_doanh_thu()
    kiem_tra("Doanh thu ban đầu", doanh_thu, 0)

    # 8.2. Doanh thu của phiếu chờ
    tk01 = PhieuDatTour(
        "TK01", khach_tk, tour_tk, 2, [dich_vu_tk]
    )

    ql_tk.them_phieu_dat(tk01)

    doanh_thu = ql_tk.thong_ke_doanh_thu()
    kiem_tra("Không tính doanh thu phiếu chờ", doanh_thu, 0)

    # 8.3. Doanh thu sau xác nhận
    ql_tk.xac_nhan_phieu_dat("TK01")

    doanh_thu = ql_tk.thong_ke_doanh_thu()
    kiem_tra("Doanh thu sau xác nhận", doanh_thu, 6700000)

    # 8.4. Doanh thu khi thay đổi giá tour
    ql_tk.cap_nhat_tour(
        "ND01", {"gia_co_ban": 4000000}
    )

    doanh_thu = ql_tk.thong_ke_doanh_thu()
    kiem_tra("Tiền đã chốt không thay đổi", doanh_thu, 6700000)

    # 8.5. Doanh thu sau hủy
    ql_tk.huy_phieu_dat("TK01")

    doanh_thu = ql_tk.thong_ke_doanh_thu()
    kiem_tra("Doanh thu sau hủy phiếu", doanh_thu, 0)

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 9. KIỂM THỬ THỐNG KÊ TỶ LỆ LẤP ĐẦY
    # ==================================================

    print("\n=== 9. KIỂM THỬ TỶ LỆ LẤP ĐẦY ===")
    ket_qua_nhom = []

    # 9.1. Tour chưa có khách
    ty_le = ql_tk.thong_ke_ty_le_lap_day()
    kiem_tra("Tỷ lệ khi chưa có khách", ty_le, 0)

    # 9.2. Tour có khách đặt
    tk02 = PhieuDatTour(
        "TK02", khach_tk, tour_tk, 5
    )

    ql_tk.them_phieu_dat(tk02)

    ty_le = ql_tk.thong_ke_ty_le_lap_day()
    kiem_tra("Phiếu chờ chưa giữ chỗ", ty_le, 0)

    ql_tk.xac_nhan_phieu_dat("TK02")

    ty_le = ql_tk.thong_ke_ty_le_lap_day()
    kiem_tra("Tỷ lệ sau khi đặt 5 chỗ", ty_le, 20)

    # 9.3. Tour hết chỗ
    tk03 = PhieuDatTour(
        "TK03", khach_tk, tour_tk, 20
    )

    ql_tk.them_phieu_dat(tk03)
    ql_tk.xac_nhan_phieu_dat("TK03")

    ty_le = ql_tk.thong_ke_ty_le_lap_day()
    kiem_tra("Tỷ lệ khi hết chỗ", ty_le, 100)

    # 9.4. Tỷ lệ sau hủy
    ql_tk.huy_phieu_dat("TK02")

    ty_le = ql_tk.thong_ke_ty_le_lap_day()
    kiem_tra("Tỷ lệ sau khi trả 5 chỗ", ty_le, 80)

    # 9.5. Kiểm tra tỷ lệ khi có nhiều tour
    tour_tk2 = TourNoiDia(
        "ND02", "Khám phá Đà Lạt", "Đà Lạt",
        3, "2026-12-20", 2500000, 30, 150000
    )

    ql_tk.them_tour(tour_tk2)

    # 20 chỗ đã đặt trên tổng 55 chỗ
    ty_le = ql_tk.thong_ke_ty_le_lap_day()
    kiem_tra("Tỷ lệ lấp đầy nhiều tour", ty_le, 36.36)

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 10. KIỂM THỬ XUẤT BÁO CÁO CSV
    # ==================================================

    print("\n=== 10. KIỂM THỬ XUẤT BÁO CÁO CSV ===")
    ket_qua_nhom = []

    # 10.1. Xuất báo cáo
    print("\n--- 10.1. Xuất báo cáo CSV ---")

    ten_file_csv = "test_bao_cao.csv"

    ket_qua = xuat_bao_cao_csv(
        ql_tk.ds_tour,
        ql_tk.ds_phieu_dat,
        ten_file_csv
    )

    kiem_tra("Xuất báo cáo CSV", ket_qua)

    # 10.2. Kiểm tra nội dung báo cáo
    print("\n--- 10.2. Kiểm tra nội dung báo cáo ---")

    if ket_qua == True:

        with open(ten_file_csv, encoding="utf-8-sig") as f:
            ds_dong = f.read().splitlines()

        kiem_tra("CSV có tiêu đề và hai tour", len(ds_dong), 3)

        if len(ds_dong) == 3:

            dong_nd01 = ds_dong[1].split(";")
            dong_nd02 = ds_dong[2].split(";")

            kiem_tra(
                "Thông tin thống kê tour ND01",
                dong_nd01[6:],
                ["25", "20", "5", "80.0", "84000000.0"]
            )

            kiem_tra(
                "Thông tin thống kê tour ND02",
                dong_nd02[6:],
                ["30", "0", "30", "0.0", "0.0"]
            )

    # 10.3. Xuất file với đường dẫn không hợp lệ
    ket_qua = xuat_bao_cao_csv(
        ql_tk.ds_tour,
        ql_tk.ds_phieu_dat,
        "thu_muc_khong_ton_tai/bao_cao.csv"
    )

    kiem_tra("Từ chối đường dẫn CSV không hợp lệ", ket_qua, False)

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 11. KIỂM THỬ XUẤT LỊCH TRÌNH TXT
    # ==================================================

    print("\n=== 11. KIỂM THỬ XUẤT LỊCH TRÌNH TXT ===")
    ket_qua_nhom = []

    # 11.1. Xuất lịch trình
    ten_file_txt = "test_lich_trinh.txt"

    ket_qua = xuat_lich_trinh_text(
        tour_txt, ten_file_txt
    )

    kiem_tra("Xuất lịch trình TXT", ket_qua)

    # 11.2. Kiểm tra nội dung lịch trình
    if ket_qua == True:

        with open(ten_file_txt, encoding="utf-8") as f:
            noi_dung = f.read()

        kiem_tra(
            "TXT có lịch trình ngày 1",
            "Khám phá thành phố Đà Nẵng" in noi_dung
        )

        kiem_tra(
            "TXT có lịch trình ngày 2",
            "Tham quan Hội An" in noi_dung
        )

        kiem_tra(
            "TXT có hoạt động sáng, chiều và tối",
            "Đón khách" in noi_dung
            and "Tham quan Sơn Trà" in noi_dung
            and "Dạo biển" in noi_dung
        )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 12. KIỂM THỬ QUẢN LÝ DỮ LIỆU ĐIỂM ĐẾN
    # ==================================================

    print("\n=== 12. KIỂM THỬ DỮ LIỆU ĐIỂM ĐẾN ===")
    ket_qua_nhom = []

    # 12.1. Đọc dữ liệu điểm đến giả lập
    du_lieu_dd = du_lieu_mau.copy()

    du_lieu_dd["destinations"] = ds_diem_den_mau

    ql_dd = tao_quan_ly(
        "test_diem_den.json", du_lieu_dd
    )

    kiem_tra(
        "Đọc dữ liệu điểm đến",
        ql_dd.lay_ds_diem_den(),
        ds_diem_den_mau
    )

    # 12.2. Bảo toàn điểm đến khi cập nhật tour
    ql_dd.cap_nhat_tour(
        "ND01", {"gia_co_ban": 3500000}
    )

    du_lieu_json = doc_json(ql_dd.file_path)

    kiem_tra(
        "Điểm đến không bị mất khi lưu tour",
        du_lieu_json["destinations"],
        ds_diem_den_mau
    )

    # 12.3. Khôi phục dữ liệu điểm đến
    ql_dd.tai_du_lieu()

    kiem_tra(
        "Khôi phục điểm đến",
        ql_dd.lay_ds_diem_den(),
        ds_diem_den_mau
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 13. KIỂM THỬ XỬ LÝ LỖI VÀ BẢO TOÀN DỮ LIỆU
    # ==================================================

    print("\n=== 13. KIỂM THỬ XỬ LÝ LỖI ===")
    ket_qua_nhom = []

    # 13.1. Chuẩn bị file kiểm thử
    ql_loi = tao_quan_ly(
        "test_luu_loi.json", du_lieu_mau
    )

    tour_loi = ql_loi.lay_tour_theo_ma("ND01")
    khach_loi = ql_loi.lay_khach_hang_theo_ma("KH01")

    phieu_loi = PhieuDatTour(
        "PD_LOI", khach_loi, tour_loi, 2
    )

    ql_loi.them_phieu_dat(phieu_loi)

    du_lieu_truoc = du_lieu_quan_ly(ql_loi)

    # Cố ý tạo lỗi trên file kiểm thử
    with open(ql_loi.file_path, "w", encoding="utf-8") as f:
        f.write("Du lieu loi")

    # 13.2. Kiểm tra lỗi lưu dữ liệu
    print("\n--- 13.2. Kiểm tra lỗi lưu dữ liệu ---")

    ket_qua = ql_loi.luu_du_lieu()
    kiem_tra("Không lưu đè file JSON lỗi", ket_qua, False)

    # 13.3. Kiểm tra thêm dữ liệu khi file lỗi
    print("\n--- 13.3. Thêm dữ liệu khi file lỗi ---")

    ket_qua = ql_loi.them_tour(qt)
    kiem_tra("Thêm tour khi lưu thất bại", ket_qua, False)

    ket_qua = ql_loi.them_khach_hang(kh)
    kiem_tra("Thêm khách hàng khi lưu thất bại", ket_qua, False)

    ket_qua = ql_loi.them_dich_vu(dv)
    kiem_tra("Thêm dịch vụ khi lưu thất bại", ket_qua, False)

    # 13.4. Xác nhận và hủy phiếu khi file lỗi
    print("\n--- 13.4. Xử lý lỗi phiếu đặt ---")

    ket_qua = ql_loi.xac_nhan_phieu_dat("PD_LOI")
    kiem_tra("Xác nhận khi lưu thất bại", ket_qua, False)

    ket_qua = ql_loi.huy_phieu_dat("PD_LOI")
    kiem_tra("Hủy phiếu khi lưu thất bại", ket_qua, False)

    # 13.5. Kiểm tra dữ liệu có bị thay đổi không
    du_lieu_sau = du_lieu_quan_ly(ql_loi)

    kiem_tra(
        "Bảo toàn dữ liệu sau khi lưu thất bại",
        du_lieu_sau,
        du_lieu_truoc
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 14. KIỂM THỬ KHÔI PHỤC TOÀN BỘ DỮ LIỆU
    # ==================================================

    print("\n=== 14. KIỂM THỬ KHÔI PHỤC TOÀN BỘ DỮ LIỆU ===")
    ket_qua_nhom = []

    # 14.1. Chuẩn bị dữ liệu từ phần thống kê
    du_lieu_kp = doc_json(ql_tk.file_path)

    du_lieu_kp["destinations"] = ds_diem_den_mau

    ql_kp = tao_quan_ly(
        "test_khoi_phuc.json", du_lieu_kp
    )

    # Bổ sung lịch trình
    tour_kp = ql_kp.lay_tour_theo_ma("ND01")

    lich_trinh_mau = LichTrinhNgay(
        1, "Khám phá Đà Nẵng",
        "Đón khách", "Tham quan Sơn Trà", "Dạo biển"
    )

    tour_kp.them_lich_trinh(lich_trinh_mau)

    # 14.2. Lưu toàn bộ dữ liệu
    ket_qua = ql_kp.luu_du_lieu()
    kiem_tra("Lưu toàn bộ dữ liệu", ket_qua)

    du_lieu_truoc = du_lieu_quan_ly(ql_kp)

    # 14.3. Tạo đối tượng quản lý mới
    ql_moi = QuanLyTour(ql_kp.file_path)

    du_lieu_sau = du_lieu_quan_ly(ql_moi)

    kiem_tra(
        "Khôi phục toàn bộ dữ liệu",
        du_lieu_sau,
        du_lieu_truoc
    )

    # 14.4. Kiểm tra doanh thu sau khôi phục
    doanh_thu = ql_moi.thong_ke_doanh_thu()
    kiem_tra("Doanh thu sau khôi phục", doanh_thu, 84000000)

    # 14.5. Kiểm tra số chỗ sau khôi phục
    ty_le = ql_moi.thong_ke_ty_le_lap_day()
    kiem_tra("Tỷ lệ lấp đầy sau khôi phục", ty_le, 36.36)

    # 14.6. Kiểm tra đúng loại đối tượng tour
    tour_khoi_phuc = ql_moi.lay_tour_theo_ma("ND01")

    kiem_tra(
        "Khôi phục đúng lớp tour nội địa",
        isinstance(tour_khoi_phuc, TourNoiDia)
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # TỔNG KẾT KIỂM THỬ
    # ==================================================

    print("\n========================================")
    print("TỔNG KẾT 14 NHÓM KIỂM THỬ")
    print("========================================")

    tong_ket_nhom(ket_qua_test)

    print("Tổng số phép kiểm tra:", len(ket_qua_test))