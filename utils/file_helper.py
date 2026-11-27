# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:29:17 2026

@author: asus
"""

import json
import csv
import os
import sys
import shutil

sys.path.append("..")

from config import STATUS_CONFIRMED


# Lưu dữ liệu vào file JSON
def luu_json(duong_dan, du_lieu):
    file_tam = duong_dan + ".tmp"
    file_sao_luu = duong_dan + ".bak"

    try:
        # Kiểm tra file JSON cũ trước khi ghi đè
        if os.path.exists(duong_dan):
            doc_json(duong_dan)

        # Ghi dữ liệu mới vào file tạm
        with open(file_tam, 'w', encoding='utf-8') as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=4)

        # Sao lưu file cũ nếu đã tồn tại
        if os.path.exists(duong_dan):
            shutil.copyfile(duong_dan, file_sao_luu)

        # Thay thế file chính bằng file tạm
        os.replace(file_tam, duong_dan)

        return True

    except Exception as e:
        print("Lỗi khi lưu file:", e)
        return False


# Đọc dữ liệu từ file JSON
def doc_json(duong_dan, mac_dinh=None):
    try:
        with open(duong_dan, 'r', encoding='utf-8') as f:
            return json.load(f)

    except FileNotFoundError:
        print(f"Chưa có file {duong_dan}.")
        return mac_dinh

    except json.JSONDecodeError:
        print(f"File {duong_dan} bị trống hoặc sai định dạng JSON.")
        raise

    except OSError as e:
        print("Lỗi khi đọc file:", e)
        raise


# Xuất báo cáo thống kê tour ra file CSV
def xuat_bao_cao_csv(ds_tour, ds_phieu_dat, ten_file="data/bao_cao_tours.csv"):
    try:
        with open(ten_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f, delimiter=';')

            writer.writerow([
                "Mã tour",
                "Tên tour",
                "Điểm đến",
                "Ngày khởi hành",
                "Giá cơ bản",
                "Giá vé",
                "Số chỗ tối đa",
                "Số chỗ đã đặt",
                "Số chỗ còn lại",
                "Tỷ lệ lấp đầy (%)",
                "Doanh thu"
            ])

            for tour in ds_tour:
                gia_ve = tour.tinh_gia_ve()
                so_cho_con_lai = tour.so_cho_toi_da - tour.so_cho_da_dat

                if tour.so_cho_toi_da > 0:
                    ty_le = tour.so_cho_da_dat / tour.so_cho_toi_da * 100
                else:
                    ty_le = 0

                # Tính doanh thu từ các phiếu đã xác nhận
                doanh_thu = 0.0

                for phieu in ds_phieu_dat:
                    if phieu.tour.ma_tour == tour.ma_tour:
                        if phieu.trang_thai == STATUS_CONFIRMED:
                            doanh_thu += phieu.tong_tien

                dong = [
                    tour.ma_tour,
                    tour.ten_tour,
                    tour.diem_den,
                    tour.ngay_khoi_hanh,
                    tour.gia_co_ban,
                    gia_ve,
                    tour.so_cho_toi_da,
                    tour.so_cho_da_dat,
                    so_cho_con_lai,
                    round(ty_le, 2),
                    doanh_thu
                ]

                writer.writerow(dong)

        return True

    except Exception as e:
        print("Lỗi khi xuất file CSV:", e)
        return False


# Xuất thông tin lịch trình tour ra file TXT
def xuat_lich_trinh_text(tour, ten_file="data/lich_trinh_tour.txt"):
    try:
        with open(ten_file, 'w', encoding='utf-8') as f:
            f.write("========================================\n")
            f.write(f"      CHƯƠNG TRÌNH TOUR: {tour.ten_tour}\n")
            f.write("========================================\n")
            f.write(f"- Mã tour: {tour.ma_tour}\n")
            f.write(f"- Điểm đến: {tour.diem_den}\n")
            f.write(f"- Số ngày: {tour.so_ngay} ngày\n")
            f.write(f"- Khởi hành ngày: {tour.ngay_khoi_hanh}\n")
            f.write(f"- Giá vé: {tour.tinh_gia_ve()} VNĐ\n")
            f.write("----------------------------------------\n")
            # Xuất lịch trình chi tiết từng ngày
            f.write("LỊCH TRÌNH CHI TIẾT\n")

            ds_lich_trinh = tour.lay_lich_trinh()

            if len(ds_lich_trinh) == 0:
                f.write("Tour chưa có lịch trình chi tiết.\n")
            else:
                for lt in ds_lich_trinh:
                    f.write(f"\nNgày {lt.thu_tu_ngay}: {lt.tieu_de}\n")
                    f.write(f"- Buổi sáng: {lt.buoi_sang}\n")
                    f.write(f"- Buổi chiều: {lt.buoi_chieu}\n")
                    f.write(f"- Buổi tối: {lt.buoi_toi}\n")

            f.write("----------------------------------------\n")
            f.write("Lưu ý: Quý khách vui lòng có mặt trước 30 phút.\n")
            f.write("========================================\n")

        return True

    except Exception as e:
        print("Lỗi khi xuất file lịch trình:", e)
        return False


# KIỂM THỬ CHỨC NĂNG
if __name__ == "__main__":

    # ==================================================
    # CHUẨN BỊ KIỂM THỬ
    # ==================================================

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

    # Tên file dùng để kiểm thử
    ten_file_test = "test_sao_luu.json"
    ten_file_loi = "test_loi.json"
    ten_file_khong_ton_tai = "test_file_helper_khong_ton_tai.json"

    # Xóa các file kiểm thử cũ nếu tồn tại
    if os.path.exists(ten_file_test):
        os.remove(ten_file_test)

    if os.path.exists(ten_file_test + ".bak"):
        os.remove(ten_file_test + ".bak")

    if os.path.exists(ten_file_test + ".tmp"):
        os.remove(ten_file_test + ".tmp")

    if os.path.exists(ten_file_khong_ton_tai):
        os.remove(ten_file_khong_ton_tai)

    # Dữ liệu mẫu trước khi cập nhật
    du_lieu_cu = {
        "ma_tour": "ND01",
        "gia_co_ban": 3000000
    }

    # Dữ liệu mẫu sau khi cập nhật
    du_lieu_moi = {
        "ma_tour": "ND01",
        "gia_co_ban": 4000000
    }


    # ==================================================
    # 1. KIỂM THỬ ĐỌC VÀ GHI FILE JSON
    # ==================================================

    print("\n=== 1. KIỂM THỬ ĐỌC VÀ GHI FILE JSON ===")
    ket_qua_nhom = []

    # 1.1. Ghi dữ liệu vào JSON
    print("\n--- 1.1. Ghi dữ liệu ---")

    ket_qua = luu_json(ten_file_test, du_lieu_cu)

    kiem_tra("Ghi dữ liệu vào JSON", ket_qua)

    # 1.2. Đọc dữ liệu từ JSON
    print("\n--- 1.2. Đọc dữ liệu ---")

    du_lieu = doc_json(ten_file_test)

    kiem_tra("Đọc dữ liệu từ JSON", du_lieu, du_lieu_cu)

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 2. KIỂM THỬ XỬ LÝ LỖI ĐỌC FILE
    # ==================================================

    print("\n=== 2. KIỂM THỬ XỬ LÝ LỖI ĐỌC FILE ===")
    ket_qua_nhom = []

    # 2.1. Đọc file không tồn tại
    print("\n--- 2.1. File không tồn tại ---")

    du_lieu = doc_json(ten_file_khong_ton_tai, {})

    kiem_tra("Trả về dữ liệu mặc định", du_lieu, {})

    # 2.2. Đọc file sai định dạng JSON
    print("\n--- 2.2. File sai định dạng ---")

    # Cố ý tạo file không đúng định dạng JSON
    with open(ten_file_loi, "w", encoding="utf-8") as f:
        f.write("Du lieu loi")

    try:
        doc_json(ten_file_loi)

        kiem_tra("Phát hiện JSON sai định dạng", False)

    except json.JSONDecodeError:

        kiem_tra("Phát hiện JSON sai định dạng", True)

    # 2.3. Đọc file bị trống
    print("\n--- 2.3. File bị trống ---")

    with open(ten_file_loi, "w", encoding="utf-8") as f:
        f.write("")

    try:
        doc_json(ten_file_loi)

        kiem_tra("Phát hiện file JSON bị trống", False)

    except json.JSONDecodeError:

        kiem_tra("Phát hiện file JSON bị trống", True)

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 3. KIỂM THỬ SAO LƯU DỮ LIỆU
    # ==================================================

    print("\n=== 3. KIỂM THỬ SAO LƯU DỮ LIỆU ===")
    ket_qua_nhom = []

    # 3.1. Ghi dữ liệu mới
    print("\n--- 3.1. Ghi dữ liệu mới ---")

    ket_qua = luu_json(ten_file_test, du_lieu_moi)

    kiem_tra("Cập nhật dữ liệu JSON", ket_qua)

    # 3.2. Kiểm tra file chính chứa dữ liệu mới
    print("\n--- 3.2. Kiểm tra file chính ---")

    du_lieu = doc_json(ten_file_test)

    kiem_tra("File chính chứa dữ liệu mới", du_lieu, du_lieu_moi)

    # 3.3. Kiểm tra file sao lưu chứa dữ liệu cũ
    print("\n--- 3.3. Kiểm tra file sao lưu ---")

    du_lieu_sao_luu = doc_json(ten_file_test + ".bak")

    kiem_tra(
        "File sao lưu chứa dữ liệu cũ",
        du_lieu_sao_luu,
        du_lieu_cu
    )

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 4. KIỂM THỬ BẢO TOÀN VÀ KHÔI PHỤC DỮ LIỆU
    # ==================================================

    print("\n=== 4. KIỂM THỬ BẢO TOÀN VÀ KHÔI PHỤC DỮ LIỆU ===")
    ket_qua_nhom = []

    # 4.1. Ghi dữ liệu không hợp lệ
    print("\n--- 4.1. Ghi dữ liệu không hợp lệ ---")

    # JSON không hỗ trợ kiểu dữ liệu Set
    du_lieu_sai = {
        "gia_co_ban": {100, 200}
    }

    ket_qua = luu_json(ten_file_test, du_lieu_sai)

    kiem_tra("Từ chối ghi dữ liệu kiểu Set", ket_qua, False)

    # Kiểm tra file chính không bị thay đổi
    du_lieu = doc_json(ten_file_test)

    kiem_tra("Bảo toàn file chính", du_lieu, du_lieu_moi)

    # Kiểm tra bản sao lưu không bị thay đổi
    du_lieu_sao_luu = doc_json(ten_file_test + ".bak")

    kiem_tra("Bảo toàn bản sao lưu", du_lieu_sao_luu, du_lieu_cu)

    # 4.2. Ghi đè file JSON bị lỗi
    print("\n--- 4.2. Ghi đè file JSON bị lỗi ---")

    # Cố ý làm hỏng file kiểm thử
    with open(ten_file_test, "w", encoding="utf-8") as f:
        f.write("Du lieu loi")

    ket_qua = luu_json(ten_file_test, du_lieu_moi)

    kiem_tra("Từ chối ghi đè file JSON lỗi", ket_qua, False)

    # Kiểm tra file lỗi và bản sao lưu vẫn được giữ nguyên
    with open(ten_file_test, "r", encoding="utf-8") as f:
        noi_dung = f.read()

    du_lieu_sao_luu = doc_json(ten_file_test + ".bak")

    kiem_tra(
        "Bảo toàn file lỗi và bản sao lưu",
        noi_dung == "Du lieu loi"
        and du_lieu_sao_luu == du_lieu_cu
    )

    # 4.3. Khôi phục dữ liệu từ file sao lưu
    print("\n--- 4.3. Khôi phục từ bản sao lưu ---")

    # Sao chép bản sao lưu trở lại file chính
    shutil.copyfile(ten_file_test + ".bak", ten_file_test)

    du_lieu = doc_json(ten_file_test)

    kiem_tra("Khôi phục dữ liệu từ bản sao lưu", du_lieu, du_lieu_cu)

    tong_ket_nhom(ket_qua_nhom)


    # ==================================================
    # 5. KIỂM THỬ XUẤT TXT KHI TOUR CHƯA CÓ LỊCH TRÌNH
    # ==================================================

    print("\n=== 5. KIỂM THỬ XUẤT FILE TXT ===")
    ket_qua_nhom = []

    # 5.1. Tạo tour chưa có lịch trình
    from models.tour import TourNoiDia

    tour = TourNoiDia(
        "ND01",
        "Đà Nẵng - Hội An",
        "Đà Nẵng",
        3,
        "2026-12-15",
        3000000,
        25,
        200000
    )

    # 5.2. Xuất file TXT
    print("\n--- 5.2. Xuất file TXT ---")

    ten_file_txt = "test_lich_trinh_trong.txt"

    ket_qua = xuat_lich_trinh_text(tour, ten_file_txt)

    kiem_tra("Xuất lịch trình ra TXT", ket_qua)

    # 5.3. Kiểm tra nội dung TXT
    print("\n--- 5.3. Kiểm tra nội dung TXT ---")

    if ket_qua == True:

        with open(ten_file_txt, "r", encoding="utf-8") as f:
            noi_dung = f.read()

        kiem_tra(
            "Hiển thị thông báo chưa có lịch trình",
            "Tour chưa có lịch trình chi tiết." in noi_dung
        )

        kiem_tra(
            "Hiển thị đúng giá vé",
            "3200000.0 VNĐ" in noi_dung
        )

    tong_ket_nhom(ket_qua_nhom)

    # ==================================================
    # TỔNG KẾT KIỂM THỬ
    # ==================================================

    print("\n========================================")
    print("TỔNG KẾT KIỂM THỬ FILE_HELPER")
    print("========================================")

    tong_ket_nhom(ket_qua_test)

    print("Tổng số phép kiểm tra:", len(ket_qua_test))
