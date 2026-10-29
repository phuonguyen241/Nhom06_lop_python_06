# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 15:29:17 2026

@author: asus
"""

import json
import csv

def luu_json(duong_dan, du_lieu): # Ghi dữ liệu ra file JSON, trả về True nếu thành công
    try:
        with open(duong_dan, 'w', encoding = 'utf-8') as f:
            json.dump(du_lieu, f, ensure_ascii=False, indent = 4) # ensure_ascii=False để giữ tiếng Việt, indent=4 để thụt lề đẹp
        return True
    except Exception as e:
        print("Lỗi khi lưu file: ", e)
        return False
    
def doc_json(duong_dan): # Đọc dữ liệu từ file JSON, trả về [] nếu chưa có file hoặc file lỗi
    try:
        with open(duong_dan, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Chưa có file {duong_dan}, trả về danh sách rỗng.") # Chưa có file thì trả về danh sách rỗng, không để app bị văng
        return []
    except json.JSONDecodeError:
        print(f"File {duong_dan} bị trống hoặc sai định dạng JSON.") # File rỗng hoặc sai cú pháp JSON
        return []
    
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
            
    
# =====================================================================
# KIỂM THỬ ĐỘC LẬP TẤT CẢ CÁC HÀM
# =====================================================================

if __name__ == "__main__":
    print("=== BẮT ĐẦU KIỂM THỬ MODULE FILE_HELPER ===")

    # 1. Dữ liệu từ điển để test JSON và CSV
    tour_mau_dict = [
        {
            "ma_tour": "ND01",
            "ten_tour": "Đà Nẵng - Hội An",
            "diem_den": "Đà Nẵng",
            "so_ngay": 3,
            "ngay_khoi_hanh": "2026-06-15",
            "gia_co_ban": 3000000,
            "so_cho_toi_da": 25,
            "so_cho_da_dat": 2
        }
    ]

    # Đọc & Ghi JSON
    luu_json("test_tour.json", tour_mau_dict)
    kq_doc = doc_json("test_tour.json")
    print("1. Đọc JSON:", "Thành công" if len(kq_doc) > 0 else "Thất bại")

    # Xuất CSV
    kq_csv = xuat_bao_cao_csv(tour_mau_dict, "test_bao_cao.csv")
    print("2. Xuất CSV:", "Thành công" if kq_csv else "Thất bại")

    # 2. Tạo một đối tượng mẫu để test xuất TXT
    class TourTest:
        def __init__(self):
            self.ma_tour = "ND01"
            self.ten_tour = "Đà Nẵng - Hội An"
            self.diem_den = "Đà Nẵng"
            self.so_ngay = 3
            self.ngay_khoi_hanh = "2026-06-15"
            self.gia_co_ban = 3000000

    doi_tuong_tour = TourTest()

    # Xuất TXT với đối tượng OOP
    kq_txt = xuat_lich_trinh_text(doi_tuong_tour, "test_lich_trinh.txt")
    print("3. Xuất TXT:", "Thành công" if kq_txt else "Thất bại")

    print("=== HOÀN TẤT KIỂM THỬ ===")
