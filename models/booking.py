# -*- coding: utf-8 -*-
# Phan cong: Lich trinh chi tiet va phieu dat tour

from datetime import date
from config import STATUS_PENDING, STATUS_CONFIRMED, STATUS_CANCELLED


class LichTrinhNgay:
    def __init__(self, thu_tu_ngay, tieu_de, buoi_sang, buoi_chieu, buoi_toi):
        # Kiem tra thu tu ngay
        if isinstance(thu_tu_ngay, bool) or not isinstance(thu_tu_ngay, int) or thu_tu_ngay <= 0:
            raise ValueError("Thu tu ngay phai la so nguyen duong")

        # Kiem tra tieu de
        if not isinstance(tieu_de, str) or tieu_de.strip() == "":
            raise ValueError("Tieu de khong duoc de trong")

        # Kiem tra noi dung cac buoi
        if not isinstance(buoi_sang, str) or not isinstance(buoi_chieu, str) or not isinstance(buoi_toi, str):
            raise ValueError("Noi dung lich trinh phai la chuoi")

        if buoi_sang.strip() == "" and buoi_chieu.strip() == "" and buoi_toi.strip() == "":
            raise ValueError("Noi dung lich trinh khong duoc de trong")

        self.thu_tu_ngay = thu_tu_ngay

        # Them thuoc tinh ngay_thu de tuong thich voi models/tour.py
        self.ngay_thu = thu_tu_ngay

        self.tieu_de = tieu_de
        self.buoi_sang = buoi_sang
        self.buoi_chieu = buoi_chieu
        self.buoi_toi = buoi_toi

    def to_dict(self):
        return {
            "thu_tu_ngay": self.thu_tu_ngay,
            "tieu_de": self.tieu_de,
            "buoi_sang": self.buoi_sang,
            "buoi_chieu": self.buoi_chieu,
            "buoi_toi": self.buoi_toi
        }


class PhieuDatTour:
    def __init__(self, ma_dat_cho, khach_hang, tour, so_luong_ve, ds_dich_vu=None, ngay_dat=None):
        # Kiem tra ma dat cho
        if not isinstance(ma_dat_cho, str) or ma_dat_cho.strip() == "":
            raise ValueError("Ma dat cho khong duoc de trong")

        # Kiem tra so luong ve
        if isinstance(so_luong_ve, bool) or not isinstance(so_luong_ve, int) or so_luong_ve <= 0:
            raise ValueError("So luong ve phai la so nguyen duong")

        # Kiem tra khach hang va tour
        if khach_hang is None:
            raise ValueError("Khach hang khong duoc de trong")

        if tour is None:
            raise ValueError("Tour khong duoc de trong")

        # Kiem tra danh sach dich vu
        if ds_dich_vu is None:
            ds_dich_vu = []

        if not isinstance(ds_dich_vu, list):
            raise ValueError("Danh sach dich vu phai la list")

        self.ma_dat_cho = ma_dat_cho
        self.khach_hang = khach_hang
        self.tour = tour
        self.so_luong_ve = so_luong_ve
        self.ds_dich_vu = ds_dich_vu

        # Luu ngay dat tour
        if ngay_dat is None:
            self.ngay_dat = date.today().isoformat()
        else:
            self.ngay_dat = ngay_dat

        # Tong tien chi duoc chot khi xac nhan dat thanh cong
        self.tong_tien = None

        # Trang thai ban dau
        self.trang_thai = STATUS_PENDING

    def _tinh_tong_tien_moi(self):
        # Tinh tong gia cac dich vu
        tong_tien_dich_vu = 0

        for dich_vu in self.ds_dich_vu:
            if not isinstance(dich_vu.don_gia, (int, float)) or isinstance(dich_vu.don_gia, bool) or dich_vu.don_gia < 0:
                raise ValueError("Don gia dich vu khong hop le")

            tong_tien_dich_vu += dich_vu.don_gia

        # Tinh tong tien tour va dich vu theo so luong ve
        gia_ve = self.tour.tinh_gia_ve()

        if not isinstance(gia_ve, (int, float)) or isinstance(gia_ve, bool) or gia_ve < 0:
            raise ValueError("Gia ve tour khong hop le")

        tong_tien = (gia_ve * self.so_luong_ve) + (tong_tien_dich_vu * self.so_luong_ve)

        return tong_tien

    def tinh_tong_tien(self):
        # Neu da xac nhan thi su dung tong tien da chot
        if self.tong_tien is not None:
            return self.tong_tien

        # Neu chua xac nhan thi tinh theo gia hien tai
        return self._tinh_tong_tien_moi()

    def xac_nhan_dat(self):
        # Chi cho phep xac nhan phieu dang cho
        if self.trang_thai != STATUS_PENDING:
            return False

        # Kiem tra tour con du cho hay khong
        if not self.tour.kiem_tra_con_cho(self.so_luong_ve):
            return False

        # Tinh tien truoc khi dat cho
        tong_tien_moi = self._tinh_tong_tien_moi()

        # Dat cho thanh cong
        if self.tour.dat_cho(self.so_luong_ve):
            self.tong_tien = tong_tien_moi
            self.trang_thai = STATUS_CONFIRMED
            return True

        return False

    def huy_dat(self):
        # Khong cho phep huy phieu da huy
        if self.trang_thai == STATUS_CANCELLED:
            return False

        # Huy phieu dang cho xac nhan
        if self.trang_thai == STATUS_PENDING:
            self.trang_thai = STATUS_CANCELLED
            return True

        # Huy phieu da xac nhan va tra lai so cho
        if self.trang_thai == STATUS_CONFIRMED:
            if self.tour.huy_cho(self.so_luong_ve):
                self.trang_thai = STATUS_CANCELLED
                return True

        return False

    def to_dict(self):
        # Lay ma dich vu
        ds_ma_dich_vu = []

        for dich_vu in self.ds_dich_vu:
            ds_ma_dich_vu.append(dich_vu.ma_dv)

        # Chuyen thong tin phieu dat sang dictionary
        return {
            "ma_dat_cho": self.ma_dat_cho,
            "ma_khach_hang": self.khach_hang.ma_kh,
            "ma_tour": self.tour.ma_tour,
            "ds_ma_dich_vu": ds_ma_dich_vu,
            "so_luong_ve": self.so_luong_ve,
            "ngay_dat": self.ngay_dat,
            "tong_tien": self.tong_tien,
            "trang_thai": self.trang_thai
        }


if __name__ == "__main__":
    from models.tour import TourNoiDia, TourQuocTe
    from models.customer import KhachHang, DichVu

    print("=== THU LICH TRINH NGAY ===")

    ngay_1 = LichTrinhNgay(1, "Tham quan Da Lat", "Vuon hoa", "Ho Xuan Huong", "Cho dem")
    ngay_2 = LichTrinhNgay(2, "Kham pha Da Lat", "Thac Datanla", "Doi che Cau Dat", "Nghi ngoi")
    ngay_3 = LichTrinhNgay(3, "Ket thuc hanh trinh", "Mua dac san", "Tra phong va tro ve", "")

    ds_lich_trinh = [ngay_1, ngay_2, ngay_3]

    for ngay in ds_lich_trinh:
        print(ngay.to_dict())

    print("\n=== THU PHIEU DAT TOUR NOI DIA ===")

    kh = KhachHang("KH01", "Nguyen Van An", "0912345678", "an@gmail.com")

    tour_nd = TourNoiDia("ND01", "Da Lat 3 ngay", "Da Lat", 3, "2026-12-10", 2000000, 5, 200000)

    dv = DichVu("DV01", "An uong", 150000)

    phieu = PhieuDatTour("PD01", kh, tour_nd, 2, [dv])

    print("Tong tien truoc khi dat:", phieu.tinh_tong_tien())
    print("Dat tour thanh cong:", phieu.xac_nhan_dat())
    print("So cho da dat:", tour_nd.so_cho_da_dat)
    print("Trang thai:", phieu.trang_thai)
    print("Tong tien da chot:", phieu.tinh_tong_tien())

    print("\n=== THU XAC NHAN LAN HAI ===")

    print("Xac nhan lan hai:", phieu.xac_nhan_dat())
    print("So cho da dat:", tour_nd.so_cho_da_dat)

    print("\n=== THU HUY TOUR DA XAC NHAN ===")

    print("Huy tour:", phieu.huy_dat())
    print("Trang thai:", phieu.trang_thai)
    print("So cho sau khi huy:", tour_nd.so_cho_da_dat)

    print("Huy lan hai:", phieu.huy_dat())
    print("So cho sau khi huy lan hai:", tour_nd.so_cho_da_dat)

    print("\n=== THU DAT TOUR KHI KHONG DU CHO ===")

    phieu_2 = PhieuDatTour("PD02", kh, tour_nd, 6, [])

    print("Dat 6 ve:", phieu_2.xac_nhan_dat())
    print("Trang thai:", phieu_2.trang_thai)
    print("So cho da dat:", tour_nd.so_cho_da_dat)

    print("\n=== THU HUY PHIEU CHUA XAC NHAN ===")

    phieu_3 = PhieuDatTour("PD03", kh, tour_nd, 1, [])

    print("Huy phieu:", phieu_3.huy_dat())
    print("Trang thai:", phieu_3.trang_thai)
    print("So cho da dat:", tour_nd.so_cho_da_dat)

    print("\n=== THU TOUR QUOC TE ===")

    tour_qt = TourQuocTe("QT01", "Bangkok 4 ngay", "Thai Lan", 4, "2026-12-20", 5000000, 10, 1000000)

    phieu_4 = PhieuDatTour("PD04", kh, tour_qt, 1, [])

    print("Tong tien tour quoc te:", phieu_4.tinh_tong_tien())

    print("\n=== THU SO VE KHONG HOP LE ===")

    try:
        phieu_sai = PhieuDatTour("PD05", kh, tour_nd, 0, [])
    except ValueError as e:
        print("Loi:", e)
