# BẢNG PHÂN CÔNG NHIỆM VỤ GIAI ĐOẠN 1 

* **Học phần:** Lập trình Python
* **Đề tài 19:** Hệ thống quản lý tour và lịch trình du lịch
* **Giai đoạn thực hiện:** Giai đoạn 1 – Thiết kế lớp hướng đối tượng, xây dựng chức năng nghiệp vụ và lưu trữ file JSON 

---

### 1. Bảng tổng hợp phân công nhiệm vụ và tỷ lệ đóng góp

| STT | Họ và tên | File phụ trách | Nhiệm vụ chính | Tỷ lệ đóng góp |
|:---:|:---|:---|:---|:---:|
| 1 | **Nguyễn Thị Phương Uyên** | `models/tour.py` | Xây dựng lớp `Tour`, `TourNoiDia`, `TourQuocTe` (Kế thừa và đa hình tính giá vé) | 25% |
| 2 | **Trương Lý Bảo Ngân** | `models/customer.py` | Xây dựng lớp `KhachHang` (Regex kiểm tra SĐT, Email), lớp `DichVu` | 25% |
| 3 | **Đỗ Yến Nhi** | `models/booking.py` | Xây dựng lớp `LichTrinhNgay`, lớp `PhieuDatTour` (Xử lý đặt chỗ và tính tiền) | 25% |
| 4 | **Nguyễn Hữu Phương Uyên** | `controllers/tour_manager.py`<br>`utils/file_helper.py` | Xây dựng lớp `QuanLyTour` (CRUD, tìm kiếm, thống kê) và module xử lý file JSON, CSV, Text | 25% |

---

### 2. Chi tiết phân công nhiệm vụ từng thành viên

#### 1. Nguyễn Thị Phương Uyên
* **File phụ trách:** `models/tour.py`
* **Chi tiết nhiệm vụ:**
  * Xây dựng lớp cha `Tour`: khai báo các thuộc tính mã tour, tên tour, điểm đến, số ngày, ngày khởi hành, giá vé cơ bản, số chỗ tối đa, số chỗ đã đặt.
  * Viết các phương thức nghiệp vụ của lớp cha: `kiem_tra_con_cho(so_ve)`, `dat_cho(so_ve)`, `huy_cho(so_ve)`, `tinh_gia_ve()`, `to_dict()` để phục vụ xuất dữ liệu sang JSON.
  * Xây dựng lớp con `TourNoiDia` (kế thừa `Tour`): bổ sung thuộc tính phụ thu mùa cao điểm (`phu_thu`), thực hiện ghi đè (override) phương thức `tinh_gia_ve() = gia_co_ban + phu_thu`.
  * Xây dựng lớp con `TourQuocTe` (kế thừa `Tour`): bổ sung thuộc tính chi phí visa (`phi_visa`), thực hiện ghi đè (override) phương thức `tinh_gia_ve() = gia_co_ban + phi_visa`.

#### 2. Trương Lý Bảo Ngân
* **File phụ trách:** `models/customer.py`
* **Chi tiết nhiệm vụ:**
  * Xây dựng lớp `KhachHang`: khai báo các thuộc tính mã khách hàng, họ tên, số điện thoại, email.
  * Thực hiện đóng gói dữ liệu và tích hợp Regular Expression (`re`) để kiểm tra dữ liệu: số điện thoại hợp lệ gồm 10 chữ số (đầu số di động Việt Nam), email đúng định dạng; chủ động ném ngoại lệ `ValueError` nếu người dùng nhập sai.
  * Xây dựng lớp `DichVu`: khai báo các thuộc tính mã dịch vụ, tên dịch vụ, đơn giá.
  * Viết phương thức `to_dict()` cho cả 2 lớp để chuyển đổi đối tượng sang từ điển phục vụ lưu trữ file JSON.

#### 3. Đỗ Yến Nhi
* **File phụ trách:** `models/booking.py`
* **Chi tiết nhiệm vụ:**
  * Xây dựng lớp `LichTrinhNgay`: khai báo thứ tự ngày (Ngày 1, Ngày 2...), tiêu đề hoạt động, nội dung chi tiết theo từng buổi; phương thức `to_dict()` để hiển thị và lưu trữ.
  * Xây dựng lớp `PhieuDatTour`: khai báo mã đặt chỗ, khách hàng, tour được chọn, số lượng vé đăng ký, danh sách dịch vụ đi kèm.
  * Viết phương thức `xac_nhan_dat()`: gọi hàm kiểm tra số chỗ và cập nhật trừ ghế của Tour.
  * Viết phương thức `tinh_tong_tien()`: tính tổng tiền theo công thức `(tour.tinh_gia_ve() * so_ve) + tong_tien_dich_vu` dựa trên tính đa hình giá vé.
  * Viết phương thức `to_dict()` để xuất thông tin đơn đặt vé.

#### 4. Nguyễn Hữu Phương Uyên (Nhóm trưởng)
* **File phụ trách:** `controllers/tour_manager.py` và `utils/file_helper.py`
* **Chi tiết nhiệm vụ:**
  * Xây dựng module xử lý file `utils/file_helper.py`: dùng cú pháp `with open(...)` an toàn để viết các hàm `luu_json()`, `doc_json()`, `xuat_bao_cao_csv()` và `xuat_lich_trinh_text()`.
  * Xây dựng lớp quản lý trung tâm `QuanLyTour` trong `controllers/tour_manager.py`: khởi tạo và quản lý danh sách tour, danh sách phiếu đặt vé.
  * Viết các chức năng nghiệp vụ CRUD và tìm kiếm: `them_tour()`, `xoa_tour()`, `cap_nhat_tour()`, `tim_kiem()` đa tiêu chí theo điểm đến và mức giá.
  * Viết các chức năng tổng hợp và thống kê: `thong_ke_doanh_thu()`, `thong_ke_ty_le_lap_day()`.
