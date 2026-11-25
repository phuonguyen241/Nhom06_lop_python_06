# -*- coding: utf-8 -*-
"""
Created on Wed Nov 25 17:20:31 2026

@author: GBC
"""


from datetime import datetime

try:
    from models.booking import LichTrinhNgay
except ImportError:
    class LichTrinhNgay:
        """Lớp dự phòng khi chạy độc lập nếu chưa import được từ models.booking."""

        def __init__(self, ngay_thu, tieu_de="", hoat_dong=None, mo_ta=""):
            self.ngay_thu = int(ngay_thu)
            self.tieu_de = tieu_de
            self.hoat_dong = list(hoat_dong) if hoat_dong is not None else []
            self.mo_ta = mo_ta

        def to_dict(self):
            return {
                "ngay_thu": self.ngay_thu,
                "tieu_de": self.tieu_de,
                "hoat_dong": self.hoat_dong,
                "mo_ta": self.mo_ta,
            }


def _lay_ngay_thu(lich_trinh):
    for attr in ("ngay_thu", "so_ngay", "ngay"):
        if hasattr(lich_trinh, attr):
            val = getattr(lich_trinh, attr)
            if not isinstance(val, bool) and isinstance(val, int):
                return val
    raise ValueError("Đối tượng lịch trình không có số thứ tự ngày hợp lệ.")


class Tour:
    """Lớp cha (Base class) đại diện cho một Tour du lịch chung."""

    def __init__(
        self,
        ma_tour,
        ten_tour,
        diem_den,
        so_ngay,
        ngay_khoi_hanh,
        gia_co_ban,
        so_cho_toi_da,
        so_cho_da_dat=0,
        ds_lich_trinh=None,
    ):
        if not isinstance(ma_tour, str) or not ma_tour.strip():
            raise ValueError("Mã tour không được bỏ trống.")
        if not isinstance(ten_tour, str) or not ten_tour.strip():
            raise ValueError("Tên tour không được bỏ trống.")
        if not isinstance(diem_den, str) or not diem_den.strip():
            raise ValueError("Điểm đến không được bỏ trống.")

        if isinstance(so_ngay, bool) or not isinstance(so_ngay, int) or so_ngay <= 0:
            raise ValueError("Số ngày phải là số nguyên dương.")
        if isinstance(so_cho_toi_da, bool) or not isinstance(so_cho_toi_da, int) or so_cho_toi_da <= 0:
            raise ValueError("Số chỗ tối đa phải là số nguyên dương.")
        if isinstance(so_cho_da_dat, bool) or not isinstance(so_cho_da_dat, int) or so_cho_da_dat < 0:
            raise ValueError("Số chỗ đã đặt phải là số nguyên không âm.")
        if so_cho_da_dat > so_cho_toi_da:
            raise ValueError("Số chỗ đã đặt không được vượt quá số chỗ tối đa.")

        if isinstance(gia_co_ban, bool) or not isinstance(gia_co_ban, (int, float)) or float(gia_co_ban) <= 0:
            raise ValueError("Giá vé (giá cơ bản) phải lớn hơn 0.")

        if not isinstance(ngay_khoi_hanh, str) or not ngay_khoi_hanh.strip():
            raise ValueError("Ngày khởi hành không được bỏ trống.")
        ngay_hop_le = False
        for dinh_dang in ("%Y-%m-%d", "%d/%m/%Y"):
            try:
                datetime.strptime(ngay_khoi_hanh.strip(), dinh_dang)
                ngay_hop_le = True
                break
            except ValueError:
                continue
        if not ngay_hop_le:
            raise ValueError("Ngày khởi hành không đúng định dạng hoặc không phải ngày hợp lệ.")

        self.ma_tour = ma_tour.strip()
        self.ten_tour = ten_tour.strip()
        self.diem_den = diem_den.strip()
        self.so_ngay = so_ngay
        self.ngay_khoi_hanh = ngay_khoi_hanh.strip()
        self.gia_co_ban = float(gia_co_ban)
        self.so_cho_toi_da = so_cho_toi_da
        self.so_cho_da_dat = so_cho_da_dat
        self.ds_lich_trinh = []

        if ds_lich_trinh is not None:
            if not isinstance(ds_lich_trinh, list):
                raise ValueError("ds_lich_trinh phải là kiểu list.")
            for lt in ds_lich_trinh:
                self.them_lich_trinh(lt)

    def kiem_tra_con_cho(self, so_ve):
        """Kiểm tra xem tour còn đủ chỗ trống hay không."""
        if isinstance(so_ve, bool) or not isinstance(so_ve, int) or so_ve <= 0:
            raise ValueError("Số vé phải là số nguyên dương.")
        return (self.so_cho_da_dat + so_ve) <= self.so_cho_toi_da

    def dat_cho(self, so_ve):
        """Tăng số chỗ đã đặt khi giao dịch thành công."""
        if isinstance(so_ve, bool) or not isinstance(so_ve, int) or so_ve <= 0:
            raise ValueError("Số vé đặt phải là số nguyên dương.")
        if not self.kiem_tra_con_cho(so_ve):
            raise ValueError("Không thể đặt vượt quá số chỗ còn lại của tour.")
        self.so_cho_da_dat += so_ve
        return True

    def huy_cho(self, so_ve):
        """Giảm số chỗ đã đặt khi có khách hủy vé."""
        if isinstance(so_ve, bool) or not isinstance(so_ve, int) or so_ve <= 0:
            raise ValueError("Số vé hủy phải là số nguyên dương.")
        if so_ve > self.so_cho_da_dat:
            raise ValueError("Không thể hủy nhiều hơn số chỗ đã đặt.")
        self.so_cho_da_dat -= so_ve
        return True

    def them_lich_trinh(self, lich_trinh):
        """Thêm lịch trình của một ngày vào tour, kiểm tra không trùng ngày và không vượt quá số ngày."""
        if lich_trinh is None:
            raise ValueError("Lịch trình không được để trống.")
        ngay_thu = _lay_ngay_thu(lich_trinh)
        if ngay_thu < 1 or ngay_thu > self.so_ngay:
            raise ValueError(f"Ngày thứ {ngay_thu} vượt quá số ngày của tour ({self.so_ngay} ngày).")
        for item in self.ds_lich_trinh:
            if _lay_ngay_thu(item) == ngay_thu:
                raise ValueError(f"Lịch trình ngày thứ {ngay_thu} đã bị trùng.")
        self.ds_lich_trinh.append(lich_trinh)

    def sua_lich_trinh(self, ngay_thu, hoat_dong=None, tieu_de=None, mo_ta=None):
        """Tìm lịch trình theo số thứ tự ngày bằng vòng lặp và cập nhật nội dung hoạt động."""
        for item in self.ds_lich_trinh:
            if _lay_ngay_thu(item) == ngay_thu:
                if hoat_dong is not None:
                    if hasattr(item, "hoat_dong"):
                        item.hoat_dong = list(hoat_dong) if isinstance(hoat_dong, list) else hoat_dong
                    elif hasattr(item, "mo_ta"):
                        item.mo_ta = hoat_dong
                if tieu_de is not None and hasattr(item, "tieu_de"):
                    item.tieu_de = tieu_de
                if mo_ta is not None and hasattr(item, "mo_ta"):
                    item.mo_ta = mo_ta
                return True
        raise ValueError(f"Không tìm thấy lịch trình của ngày thứ {ngay_thu}.")

    def xoa_lich_trinh(self, ngay_thu):
        """Tìm và xóa lịch trình của ngày tương ứng."""
        for i in range(len(self.ds_lich_trinh)):
            if _lay_ngay_thu(self.ds_lich_trinh[i]) == ngay_thu:
                del self.ds_lich_trinh[i]
                return True
        raise ValueError(f"Không tìm thấy lịch trình của ngày thứ {ngay_thu} để xóa.")

    def lay_lich_trinh(self):
        """Trả về danh sách lịch trình của tour theo thứ tự ngày."""
        return sorted(self.ds_lich_trinh, key=_lay_ngay_thu)

    def tinh_gia_ve(self):
        """Phương thức mẫu của lớp cha, trả về giá vé cơ bản."""
        return self.gia_co_ban

    def to_dict(self):
        """Chuyển đối tượng thành từ điển (dict) để phục vụ ghi file JSON."""
        lich_trinh_dict = []
        for lt in self.lay_lich_trinh():
            if hasattr(lt, "to_dict") and callable(lt.to_dict):
                lich_trinh_dict.append(lt.to_dict())
            else:
                lich_trinh_dict.append(vars(lt))

        return {
            "loai_tour": "CoBan",
            "ma_tour": self.ma_tour,
            "ten_tour": self.ten_tour,
            "diem_den": self.diem_den,
            "so_ngay": self.so_ngay,
            "ngay_khoi_hanh": self.ngay_khoi_hanh,
            "gia_co_ban": self.gia_co_ban,
            "so_cho_toi_da": self.so_cho_toi_da,
            "so_cho_da_dat": self.so_cho_da_dat,
            "ds_lich_trinh": lich_trinh_dict,
        }


class TourNoiDia(Tour):
    """Lớp con kế thừa từ Tour, áp dụng cho Tour Nội Địa."""

    def __init__(
        self,
        ma_tour,
        ten_tour,
        diem_den,
        so_ngay,
        ngay_khoi_hanh,
        gia_co_ban,
        so_cho_toi_da,
        phu_thu,
        so_cho_da_dat=0,
        ds_lich_trinh=None,
    ):
        if isinstance(phu_thu, bool) or not isinstance(phu_thu, (int, float)) or float(phu_thu) < 0:
            raise ValueError("Phụ thu không được âm.")
        super().__init__(
            ma_tour,
            ten_tour,
            diem_den,
            so_ngay,
            ngay_khoi_hanh,
            gia_co_ban,
            so_cho_toi_da,
            so_cho_da_dat,
            ds_lich_trinh,
        )
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

    def __init__(
        self,
        ma_tour,
        ten_tour,
        diem_den,
        so_ngay,
        ngay_khoi_hanh,
        gia_co_ban,
        so_cho_toi_da,
        phi_visa,
        so_cho_da_dat=0,
        ds_lich_trinh=None,
    ):
        if isinstance(phi_visa, bool) or not isinstance(phi_visa, (int, float)) or float(phi_visa) < 0:
            raise ValueError("Phí visa không được âm.")
        super().__init__(
            ma_tour,
            ten_tour,
            diem_den,
            so_ngay,
            ngay_khoi_hanh,
            gia_co_ban,
            so_cho_toi_da,
            so_cho_da_dat,
            ds_lich_trinh,
        )
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


if __name__ == "__main__":
    print("=== KIỂM THỬ ĐỘC LẬP FILE TOUR.PY ===")

    # Test Tour Nội Địa
    t_nd = TourNoiDia("ND01", "Đà Nẵng - Hội An", "Đà Nẵng", 3, "2026-06-15", 3000000, 25, 500000)
    t_nd.them_lich_trinh(LichTrinhNgay(1, "Ngày 1", ["Đón khách", "Bán đảo Sơn Trà"]))
    t_nd.them_lich_trinh(LichTrinhNgay(3, "Ngày 3", ["Chợ Hàn", "Tiễn sân bay"]))
    t_nd.them_lich_trinh(LichTrinhNgay(2, "Ngày 2", ["Phố cổ Hội An"]))
    print("Tên tour:", t_nd.ten_tour, "| Loại: Nội Địa")
    print("Giá vé thực tế (Đa hình):", t_nd.tinh_gia_ve(), "VNĐ")
    print("Thứ tự ngày lịch trình:", [lt.ngay_thu for lt in t_nd.lay_lich_trinh()])
    print("Kiểm tra còn 5 chỗ:", t_nd.kiem_tra_con_cho(5))
    print("Đặt 2 chỗ thành công:", t_nd.dat_cho(2), "| Số chỗ đã đặt:", t_nd.so_cho_da_dat)
    print("Dữ liệu dict để ghi JSON:", t_nd.to_dict())

    print("-" * 40)

    # Test Tour Quốc Tế
    t_qt = TourQuocTe("QT01", "Bangkok - Pattaya", "Thái Lan", 4, "2026-07-20", 6000000, 20, 1200000)
    print("Tên tour:", t_qt.ten_tour, "| Loại: Quốc Tế")
    print("Giá vé thực tế (Đa hình):", t_qt.tinh_gia_ve(), "VNĐ")
    print("Dữ liệu dict để ghi JSON:", t_qt.to_dict())