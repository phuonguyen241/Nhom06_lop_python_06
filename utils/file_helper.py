# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:29:17 2026

@author: asus
"""

import json
import csv
import os


def luu_json(duong_dan, du_lieu):
    file_tam = duong_dan + ".tmp"

    try:
        with open(file_tam, 'w', encoding='utf-8') as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent=4)

        os.replace(file_tam, duong_dan)
        return True

    except Exception as e:
        print("Lỗi khi lưu file:", e)
        return False

    

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

    
def xuat_bao_cao_csv(ds_tour, ten_file="data/bao_cao_tours.csv"):
    try:
        # Mở file ghi với newline='' và utf-8-sig để Excel trên Windows hiển thị đúng tiếng Việt
        with open(ten_file, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.writer(f)
            
            # Ghi dòng tiêu đề cột
            writer.writerow(["Mã Tour", "Tên Tour", "Điểm Đến", "Giá Cơ Bản", "Số Chỗ"])
            
            # Ghi từng dòng dữ liệu của từng tour
            for tour in ds_tour:
                if isinstance(tour, dict):
                    dong = [tour.get("ma_tour"), tour.get("ten_tour"), tour.get("diem_den"), tour.get("gia_co_ban"), tour.get("so_cho_toi_da")]
                else:
                    dong = [tour.ma_tour, tour.ten_tour, tour.diem_den, tour.gia_co_ban, tour.so_cho_toi_da]
                writer.writerow(dong)
                
        return True
    except Exception as e:
        print("Lỗi khi xuất file CSV:", e)
        return False
        
    
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
            f.write(f"- Giá vé niêm yết: {tour.gia_co_ban} VNĐ\n")
            f.write("----------------------------------------\n")
            f.write("Lưu ý: Quý khách vui lòng có mặt trước 30 phút.\n")
            f.write("========================================\n")
        return True

    except Exception as e:
        print("Lỗi khi xuất file lịch trình:", e)
        return False
            
    

if __name__ == "__main__":
    print("=== BẮT ĐẦU KIỂM THỬ ===")

    # Dữ liệu tour mẫu
    tour_mau = {
        "ma_tour": "ND01",
        "ten_tour": "Đà Nẵng - Hội An",
        "diem_den": "Đà Nẵng",
        "so_ngay": 3,
        "ngay_khoi_hanh": "2026-12-15",
        "gia_co_ban": 3000000,
        "so_cho_toi_da": 25,
        "so_cho_da_dat": 0
    }

    # 1. Kiểm thử ghi JSON
    print("\n--- Kiểm thử ghi JSON ---")
    ket_qua = luu_json("test_data.json", tour_mau)
    print("Ghi dữ liệu:", ket_qua)

    # 2. Kiểm thử đọc JSON
    print("\n--- Kiểm thử đọc JSON ---")
    du_lieu = doc_json("test_data.json", {})
    print(du_lieu)

    # 3. Kiểm thử file không tồn tại
    print("\n--- Kiểm thử file không tồn tại ---")
    print(doc_json("file_khong_ton_tai.json", []))
    print(doc_json("file_khong_ton_tai.json", {}))

    # 4. Kiểm thử file sai định dạng
    print("\n--- Kiểm thử file sai định dạng ---")
    with open("test_loi.json", "w", encoding="utf-8") as f:
        f.write("Du lieu loi")

    try:
        doc_json("test_loi.json", {})
    except json.JSONDecodeError:
        print("Đã xử lý lỗi JSON")

    # 5. Kiểm thử ghi dữ liệu thất bại
    print("\n--- Kiểm thử ghi dữ liệu thất bại ---")
    du_lieu_loi = {"ND01", "ND02"}
    print(luu_json("test_data.json", du_lieu_loi))

    # Đọc lại để kiểm tra dữ liệu cũ
    print(doc_json("test_data.json", {}))

    # 6. Kiểm thử xuất CSV
    print("\n--- Kiểm thử xuất CSV ---")
    print(xuat_bao_cao_csv([tour_mau], "test_bao_cao.csv"))

    # 7. Kiểm thử xuất TXT
    print("\n--- Kiểm thử xuất TXT ---")

    class TourTest:
        def __init__(self):
            self.ma_tour = "ND01"
            self.ten_tour = "Đà Nẵng - Hội An"
            self.diem_den = "Đà Nẵng"
            self.so_ngay = 3
            self.ngay_khoi_hanh = "2026-12-15"
            self.gia_co_ban = 3000000

    tour = TourTest()
    print(xuat_lich_trinh_text(tour, "test_lich_trinh.txt"))

    print("\n=== HOÀN TẤT KIỂM THỬ ===")
