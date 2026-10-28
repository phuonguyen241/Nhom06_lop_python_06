# -*- coding: utf-8 -*-
# Phan cong: Lich trinh chi tiet va phieu dat tour


class LichTrinhNgay:
    def __init__(self, thu_tu_ngay, tieu_de, buoi_sang, buoi_chieu, buoi_toi):
        if thu_tu_ngay <= 0:
            raise ValueError("Thu tu ngay phai lon hon 0")
        if tieu_de.strip() == "":
            raise ValueError("Tieu de khong duoc de trong")

        self.thu_tu_ngay = thu_tu_ngay
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
    def __init__(self, ma_dat_cho, khach_hang, tour, so_luong_ve, ds_dich_vu):
        if ma_dat_cho.strip() == "":
            raise ValueError("Ma dat cho khong duoc de trong")
        if so_luong_ve <= 0:
            raise ValueError("So luong ve phai lon hon 0")

        self.ma_dat_cho = ma_dat_cho
        self.khach_hang = khach_hang
        self.tour = tour
        self.so_luong_ve = so_luong_ve
        self.ds_dich_vu = ds_dich_vu
        self.da_xac_nhan = False

    def xac_nhan_dat(self):
        # Khong dat trung cho neu da xac nhan truoc do.
        if self.da_xac_nhan:
            return False

        if self.tour.kiem_tra_con_cho(self.so_luong_ve):
            if self.tour.dat_cho(self.so_luong_ve):
                self.da_xac_nhan = True
                return True
        return False

    def tinh_tong_tien(self):
        tong_tien = self.tour.tinh_gia_ve() * self.so_luong_ve
        for dich_vu in self.ds_dich_vu:
            tong_tien += dich_vu.don_gia
        return tong_tien

    def to_dict(self):
        ds_dv = []
        for dich_vu in self.ds_dich_vu:
            ds_dv.append(dich_vu.to_dict())

        return {
            "ma_dat_cho": self.ma_dat_cho,
            "khach_hang": self.khach_hang.to_dict(),
            "tour": self.tour.to_dict(),
            "so_luong_ve": self.so_luong_ve,
            "ds_dich_vu": ds_dv,
            "tong_tien": self.tinh_tong_tien(),
            "da_xac_nhan": self.da_xac_nhan
        }


if __name__ == "__main__":
    # Hai import nay chi de chay thu file booking.py.
    # Khi ghep vao chuong trinh chinh, cac doi tuong duoc truyen tu ben ngoai.
    from tour import TourNoiDia, TourQuocTe
    from customer import KhachHang, DichVu

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

    print("Tong tien:", phieu.tinh_tong_tien())
    print("Dat tour thanh cong:", phieu.xac_nhan_dat())
    print("So cho da dat:", tour_nd.so_cho_da_dat)
    print("Xac nhan lan hai:", phieu.xac_nhan_dat())
    print("Thong tin phieu:", phieu.to_dict())

    print("\n=== THU TRUONG HOP KHONG DU CHO ===")
    phieu_2 = PhieuDatTour("PD02", kh, tour_nd, 4, [])
    print("Dat 4 ve khi chi con 3 cho:", phieu_2.xac_nhan_dat())
    print("So cho da dat:", tour_nd.so_cho_da_dat)

    print("\n=== THU PHIEU DAT TOUR QUOC TE ===")
    tour_qt = TourQuocTe("QT01", "Bangkok 4 ngay", "Thai Lan", 4, "2026-12-20", 5000000, 10, 1000000)
    phieu_3 = PhieuDatTour("PD03", kh, tour_qt, 1, [])
    print("Tong tien tour quoc te:", phieu_3.tinh_tong_tien())

    print("\n=== THU NHAP SO VE KHONG HOP LE ===")
    try:
        phieu_sai = PhieuDatTour("PD04", kh, tour_nd, 0, [])
    except ValueError as e:
        print("Loi:", e)
