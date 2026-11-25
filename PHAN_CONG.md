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

#### 4. Nguyễn Hữu Phương Uyên
* **File phụ trách:** `controllers/tour_manager.py` và `utils/file_helper.py`
* **Chi tiết nhiệm vụ:**
  * Xây dựng module xử lý file `utils/file_helper.py`: dùng cú pháp `with open(...)` an toàn để viết các hàm `luu_json()`, `doc_json()`, `xuat_bao_cao_csv()` và `xuat_lich_trinh_text()`.
  * Xây dựng lớp quản lý trung tâm `QuanLyTour` trong `controllers/tour_manager.py`: khởi tạo và quản lý danh sách tour, danh sách phiếu đặt vé.
  * Viết các chức năng nghiệp vụ CRUD và tìm kiếm: `them_tour()`, `xoa_tour()`, `cap_nhat_tour()`, `tim_kiem()` đa tiêu chí theo điểm đến và mức giá.
  * Viết các chức năng tổng hợp và thống kê: `thong_ke_doanh_thu()`, `thong_ke_ty_le_lap_day()`.



---

# BẢNG PHÂN CÔNG NHIỆM VỤ GIAI ĐOẠN 2

- **Học phần:** Lập trình Python
- **Đề tài 19:** Hệ thống quản lý tour và lịch trình du lịch
- **Mục tiêu:** Bổ sung các chức năng còn thiếu, hoàn thiện nghiệp vụ, tích hợp mã nguồn và chuẩn bị báo cáo tiến độ tuần 10.

## 1. Bảng tổng hợp phân công nhiệm vụ

| STT | Họ và tên | File phụ trách | Nhiệm vụ chính | Tỷ lệ dự kiến |
| :---: | --- | --- | --- | :---: |
| 1 | Nguyễn Thị Phương Uyên | `models/tour.py`, `utils/api_helper.py` | Hoàn thiện Tour, quản lý lịch trình, Crawl/API | 25% |
| 2 | Trương Lý Bảo Ngân | `models/customer.py`, `models/user.py`, `controllers/auth_manager.py` | Hoàn thiện khách hàng, dịch vụ, tài khoản và phân quyền | 25% |
| 3 | Đỗ Yến Nhi | `models/booking.py` | Hoàn thiện lịch trình, phiếu đặt tour, hủy đặt tour và kiểm thử | 25% |
| 4 | Nguyễn Hữu Phương Uyên | `controllers/tour_manager.py`, `utils/file_helper.py`, `config.py`, `main.py` | Hoàn thiện quản lý nghiệp vụ, lưu trữ dữ liệu và tích hợp chương trình | 25% |

---

## 2. Chi tiết phân công nhiệm vụ

### 2.1. Nguyễn Thị Phương Uyên

**File phụ trách:**
- `models/tour.py` (bổ sung)
- `utils/api_helper.py` (tạo mới)

#### a. Bổ sung quản lý lịch trình nhiều ngày

Trong lớp `Tour`, bổ sung thuộc tính:

| Thuộc tính | Kiểu dữ liệu | Ý nghĩa |
| --- | --- | --- |
| `ds_lich_trinh` | List | Danh sách các đối tượng LichTrinhNgay thuộc tour |

Bổ sung các phương thức:

| Phương thức đề xuất | Chức năng |
| --- | --- |
| `them_lich_trinh(lich_trinh)` | Thêm lịch trình của một ngày vào tour |
| `sua_lich_trinh(ngay_thu, ...)` | Cập nhật nội dung lịch trình của ngày được chọn |
| `xoa_lich_trinh(ngay_thu)` | Xóa lịch trình theo số thứ tự ngày |
| `lay_lich_trinh()` | Trả về danh sách lịch trình của tour |
| `tim_lich_trinh(ngay_thu)` | Tìm lịch trình theo số thứ tự ngày |

**Yêu cầu xử lý:**

- [ ] Không cho phép thêm hai lịch trình có cùng số thứ tự ngày trong một tour.
- [ ] Số thứ tự ngày phải lớn hơn 0 và không vượt quá số ngày của tour.
- [ ] Khi sửa hoặc xóa lịch trình, phải kiểm tra lịch trình có tồn tại hay không.
- [ ] Danh sách lịch trình được sắp xếp theo thứ tự ngày tăng dần.
- [ ] Phối hợp với thành viên phụ trách `booking.py` để sử dụng lớp `LichTrinhNgay` hiện có, không tạo lại lớp này.
- [ ] Cập nhật phương thức `to_dict()` để chuyển toàn bộ danh sách lịch trình thành dữ liệu có thể lưu trong JSON.
- [ ] Khi khôi phục tour từ JSON, phải khôi phục được cả danh sách lịch trình.

Ví dụ: Tour Đà Lạt 3 ngày 2 đêm có thể quản lý:

- Ngày 1: Khởi hành, nhận phòng, tham quan hồ Xuân Hương.
- Ngày 2: Tham quan Langbiang và các địa điểm du lịch.
- Ngày 3: Tham quan chợ Đà Lạt và trở về.

#### b. Bổ sung kiểm tra dữ liệu lớp Tour

| Dữ liệu | Điều kiện hợp lệ |
| --- | --- |
| Mã tour | Không được bỏ trống |
| Tên tour | Không được bỏ trống |
| Điểm đến | Không được bỏ trống |
| Giá vé | Là số và lớn hơn 0 |
| Số ngày | Là số nguyên dương |
| Số chỗ tối đa | Là số nguyên dương |
| Số chỗ đã đặt | Từ 0 đến số chỗ tối đa |
| Ngày khởi hành | Đúng định dạng ngày tháng và là ngày hợp lệ |
| Phụ thu | Không được âm |
| Phí visa | Không được âm |

- [ ] Kiểm tra dữ liệu khi khởi tạo và cập nhật đối tượng.
- [ ] Sử dụng `ValueError` hoặc ngoại lệ phù hợp khi dữ liệu không hợp lệ.
- [ ] Thông báo lỗi phải thể hiện rõ trường dữ liệu bị sai.
- [ ] Kiểm tra lại phương thức đặt chỗ và hủy chỗ hiện có.
- [ ] Không cho phép đặt vượt số chỗ còn trống.
- [ ] Không cho phép số chỗ đã đặt trở thành số âm.

#### c. Xây dựng chức năng Crawl/API

Tạo file `utils/api_helper.py` để lấy dữ liệu điểm đến du lịch từ nguồn bên ngoài.

Có thể sử dụng API OpenStreetMap hoặc nguồn dữ liệu du lịch công khai phù hợp với điều khoản sử dụng.

Dữ liệu dự kiến:

| Thuộc tính | Ý nghĩa |
| --- | --- |
| `ma_diem_den` | Mã định danh điểm đến |
| `ten_diem_den` | Tên địa điểm du lịch |
| `dia_chi` | Địa chỉ hoặc khu vực |
| `tinh_thanh` | Tỉnh hoặc thành phố nếu có |
| `vi_do` | Vĩ độ |
| `kinh_do` | Kinh độ |
| `nguon_du_lieu` | Nguồn cung cấp dữ liệu |

Các trường không được nguồn cung cấp phải được xử lý phù hợp, không tự tạo thông tin sai lệch.

Phương thức đề xuất:

| Phương thức | Chức năng |
| --- | --- |
| `lay_du_lieu_diem_den(tu_khoa)` | Gửi yêu cầu lấy dữ liệu điểm đến |
| `xu_ly_du_lieu(data)` | Trích xuất và chuẩn hóa các trường cần thiết |
| `luu_diem_den(data)` | Lưu dữ liệu đã xử lý vào JSON |

**Yêu cầu xử lý:**

- [ ] Lựa chọn một nguồn dữ liệu cụ thể.
- [ ] Sử dụng thư viện phù hợp như `requests` hoặc `urllib`.
- [ ] Lấy dữ liệu dựa trên từ khóa địa điểm.
- [ ] Loại bỏ bản ghi trùng lặp hoặc thiếu thông tin quan trọng.
- [ ] Chuyển dữ liệu về cấu trúc Dictionary hoặc List.
- [ ] Tái sử dụng hàm ghi JSON trong `file_helper.py`.
- [ ] Lưu kết quả vào `data/destinations.json`.
- [ ] Xử lý lỗi kết nối, timeout và dữ liệu trả về không hợp lệ.
- [ ] Không ghi đè dữ liệu hợp lệ bằng dữ liệu rỗng khi lấy API thất bại.
- [ ] Ghi rõ nguồn API và thư viện sử dụng trong báo cáo.

#### d. Kiểm thử và tài liệu

- [ ] Kiểm thử thêm lịch trình hợp lệ.
- [ ] Kiểm thử thêm lịch trình trùng ngày.
- [ ] Kiểm thử lịch trình vượt số ngày của tour.
- [ ] Kiểm thử giá vé âm hoặc số chỗ không hợp lệ.
- [ ] Kiểm thử lấy dữ liệu API thành công và thất bại.
- [ ] Phụ trách vẽ Class Diagram của hệ thống.
- [ ] Thể hiện đầy đủ các lớp và mối quan hệ kế thừa, liên kết giữa các lớp.
- [ ] Viết phần báo cáo về Tour, lịch trình và Crawl/API.

---

### 2.2. Trương Lý Bảo Ngân

**File phụ trách:**
- `models/customer.py` (bổ sung)
- `models/user.py` (tạo mới)
- `controllers/auth_manager.py` (tạo mới)

#### a. Hoàn thiện lớp KhachHang

Bổ sung hoặc kiểm tra lại các ràng buộc sau:

| Thuộc tính | Điều kiện hợp lệ |
| --- | --- |
| Mã khách hàng | Không được bỏ trống |
| Họ tên | Không được bỏ trống |
| Số điện thoại | Đúng định dạng Regex đã xây dựng |
| Email | Đúng định dạng Regex đã xây dựng |

- [ ] Kiểm tra dữ liệu khi khởi tạo đối tượng.
- [ ] Kiểm tra dữ liệu khi thay đổi thông tin khách hàng.
- [ ] Loại bỏ khoảng trắng thừa ở đầu và cuối chuỗi.
- [ ] Không cho phép lưu số điện thoại hoặc email sai định dạng.
- [ ] Hiển thị thông báo lỗi rõ ràng.
- [ ] Kiểm tra phương thức `to_dict()` có lưu đầy đủ thông tin hay không.

#### b. Hoàn thiện lớp DichVu

| Thuộc tính | Điều kiện hợp lệ |
| --- | --- |
| Mã dịch vụ | Không được bỏ trống |
| Tên dịch vụ | Không được bỏ trống |
| Đơn giá | Là số và không được âm |

- [ ] Kiểm tra kiểu dữ liệu và giá trị của đơn giá.
- [ ] Kiểm tra dữ liệu khi khởi tạo và cập nhật dịch vụ.
- [ ] Kiểm tra phương thức chuyển đổi dịch vụ sang Dictionary.
- [ ] Phối hợp với thành viên phụ trách `booking.py` để thống nhất cách tính phí dịch vụ.

Ví dụ các dịch vụ:

- Đưa đón sân bay.
- Bảo hiểm du lịch bổ sung.
- Nâng cấp khách sạn.
- Vé tham quan bổ sung.

#### c. Xây dựng lớp TaiKhoan

Tạo file `models/user.py`.

Xây dựng lớp `TaiKhoan` với các thuộc tính đề xuất:

| Thuộc tính | Kiểu dữ liệu | Ý nghĩa |
| --- | --- | --- |
| `ma_tai_khoan` | String | Mã định danh tài khoản |
| `ten_dang_nhap` | String | Tên đăng nhập |
| `mat_khau_hash` | String | Mật khẩu đã được băm |
| `ho_ten` | String | Họ tên người dùng |
| `vai_tro` | String | Admin hoặc User |

Các phương thức đề xuất:

| Phương thức | Chức năng |
| --- | --- |
| `__init__()` | Khởi tạo đối tượng tài khoản |
| `kiem_tra_ten_dang_nhap()` | Kiểm tra định dạng tên đăng nhập |
| `kiem_tra_mat_khau()` | Kiểm tra mật khẩu với giá trị đã băm |
| `doi_mat_khau()` | Cập nhật mật khẩu |
| `to_dict()` | Chuyển tài khoản thành Dictionary |

**Yêu cầu xử lý:**

- [ ] Sử dụng constructor và tính đóng gói.
- [ ] Tên đăng nhập không được bỏ trống.
- [ ] Vai trò chỉ nhận giá trị Admin hoặc User.
- [ ] Áp dụng quy tắc mật khẩu do nhóm thống nhất.
- [ ] Ưu tiên sử dụng PBKDF2 với salt riêng cho mỗi tài khoản hoặc thư viện băm mật khẩu phù hợp.
- [ ] Không lưu mật khẩu gốc vào JSON.

#### d. Xây dựng chức năng quản lý tài khoản

Tạo file `controllers/auth_manager.py`.

Xây dựng lớp `QuanLyTaiKhoan`.

Thuộc tính đề xuất:

| Thuộc tính | Ý nghĩa |
| --- | --- |
| `ds_tai_khoan` | Danh sách các tài khoản |
| `tai_khoan_hien_tai` | Tài khoản đang đăng nhập |
| `duong_dan_file` | Đường dẫn file JSON lưu tài khoản |

Phương thức đề xuất:

| Phương thức | Chức năng |
| --- | --- |
| `dang_ky()` | Tạo tài khoản mới |
| `dang_nhap()` | Kiểm tra thông tin đăng nhập |
| `dang_xuat()` | Kết thúc phiên đăng nhập |
| `doi_mat_khau()` | Thay đổi mật khẩu tài khoản |
| `tim_tai_khoan()` | Tìm tài khoản theo tên đăng nhập |
| `kiem_tra_quyen()` | Kiểm tra quyền thực hiện chức năng |
| `tai_du_lieu()` | Đọc danh sách tài khoản |
| `luu_du_lieu()` | Lưu danh sách tài khoản |

**Luồng đăng ký:**

1. Nhận thông tin tài khoản.
2. Kiểm tra dữ liệu không được bỏ trống.
3. Kiểm tra tên đăng nhập đã tồn tại hay chưa.
4. Kiểm tra mật khẩu hợp lệ.
5. Băm mật khẩu.
6. Gán vai trò User mặc định.
7. Thêm tài khoản vào danh sách.
8. Lưu dữ liệu vào JSON.
9. Trả về kết quả đăng ký.

**Luồng đăng nhập:**

1. Nhận tên đăng nhập và mật khẩu.
2. Tìm tài khoản trong danh sách.
3. Kiểm tra mật khẩu.
4. Nếu hợp lệ, lưu tài khoản đang đăng nhập.
5. Xác định vai trò của tài khoản.
6. Nếu không hợp lệ, thông báo đăng nhập thất bại.

**Luồng đổi mật khẩu:**

1. Kiểm tra người dùng đã đăng nhập.
2. Kiểm tra mật khẩu hiện tại.
3. Kiểm tra mật khẩu mới hợp lệ.
4. Băm mật khẩu mới.
5. Cập nhật tài khoản và lưu JSON.

#### e. Phân quyền người dùng

Bảng phân quyền đề xuất:

| Chức năng | Admin | User |
| --- | :---: | :---: |
| Xem danh sách tour | Có | Có |
| Tìm kiếm tour | Có | Có |
| Xem lịch trình | Có | Có |
| Thêm, sửa, xóa tour | Có | Không |
| Quản lý lịch trình | Có | Không |
| Đặt tour | Có | Có |
| Xem tất cả phiếu đặt tour | Có | Không |
| Xem phiếu đặt tour cá nhân | Có | Có |
| Hủy phiếu đặt của người khác | Có | Không |
| Thống kê doanh thu | Có | Không |
| Xuất báo cáo | Có | Không |
| Đổi mật khẩu cá nhân | Có | Có |

- [ ] Tài khoản đăng ký thông thường chỉ có vai trò User.
- [ ] Không cho phép User tự thay đổi vai trò thành Admin.
- [ ] Kiểm tra quyền ở phần xử lý nghiệp vụ, không chỉ ở giao diện.
- [ ] Thống nhất cách liên kết tài khoản với khách hàng và phiếu đặt tour.
- [ ] Lưu dữ liệu tài khoản vào `data/users.json`.
- [ ] Tái sử dụng module xử lý JSON hiện có.

#### f. Kiểm thử và tài liệu

- [ ] Kiểm thử khách hàng có email hợp lệ.
- [ ] Kiểm thử khách hàng có số điện thoại sai.
- [ ] Kiểm thử dịch vụ có đơn giá âm.
- [ ] Kiểm thử đăng ký tài khoản thành công.
- [ ] Kiểm thử đăng ký trùng tên đăng nhập.
- [ ] Kiểm thử đăng nhập sai mật khẩu.
- [ ] Kiểm thử User thực hiện chức năng chỉ dành cho Admin.
- [ ] Phụ trách phân tích mục tiêu, phạm vi và yêu cầu chức năng.
- [ ] Vẽ Use Case Diagram.
- [ ] Viết báo cáo về khách hàng, dịch vụ, tài khoản và phân quyền.

---

### 2.3. Đỗ Yến Nhi

**File phụ trách:**
- `models/booking.py` (bổ sung)

#### a. Hoàn thiện lớp LichTrinhNgay

Sử dụng lớp đã xây dựng trong giai đoạn 1.

- [ ] Kiểm tra số thứ tự ngày là số nguyên dương.
- [ ] Kiểm tra các nội dung lịch trình cần thiết không bị bỏ trống.
- [ ] Kiểm tra dữ liệu khi khởi tạo và cập nhật.
- [ ] Đảm bảo phương thức `to_dict()` lưu đầy đủ thông tin lịch trình.
- [ ] Thống nhất cách khôi phục đối tượng lịch trình từ Dictionary.
- [ ] Phối hợp với thành viên phụ trách `tour.py` để tích hợp lịch trình vào Tour.

Lớp `LichTrinhNgay` chịu trách nhiệm lưu thông tin của một ngày.

Lớp `Tour` chịu trách nhiệm quản lý danh sách các ngày.

Không xây dựng trùng chức năng quản lý danh sách lịch trình ở hai lớp.

#### b. Hoàn thiện lớp PhieuDatTour

Kiểm tra và bổ sung các thông tin cần thiết:

| Thông tin | Ý nghĩa |
| --- | --- |
| Mã phiếu đặt | Định danh phiếu đặt tour |
| Khách hàng | Đối tượng khách đăng ký |
| Tour | Tour được đăng ký |
| Số lượng vé | Số chỗ khách đăng ký |
| Danh sách dịch vụ | Các dịch vụ khách lựa chọn |
| Ngày đặt | Thời điểm lập phiếu |
| Tổng tiền | Tổng chi phí đặt tour |
| Trạng thái | Trạng thái xử lý phiếu |

Sử dụng các trạng thái thống nhất, ví dụ:

- `CHO_XAC_NHAN`
- `DA_XAC_NHAN`
- `DA_HUY`

Không tạo thêm thuộc tính trùng với thuộc tính đã có; nếu tên hiện tại khác thì thống nhất với các thành viên.

#### c. Hoàn thiện nghiệp vụ xác nhận đặt tour

Kiểm tra lại phương thức xác nhận đặt tour đã xây dựng.

**Luồng xử lý:**

1. Kiểm tra phiếu đang ở trạng thái chờ xác nhận.
2. Kiểm tra số lượng vé là số nguyên dương.
3. Kiểm tra tour còn đủ số chỗ.
4. Tính tổng chi phí.
5. Cập nhật số chỗ đã đặt của tour.
6. Cập nhật trạng thái phiếu thành đã xác nhận.
7. Ghi nhận tổng tiền tại thời điểm xác nhận.
8. Trả về kết quả xử lý.

**Ràng buộc:**

- [ ] Không xác nhận một phiếu nhiều lần.
- [ ] Không xác nhận phiếu đã hủy.
- [ ] Không cập nhật số chỗ nếu đặt tour thất bại.
- [ ] Không cho phép đặt vượt số chỗ còn lại.

#### d. Bổ sung nghiệp vụ hủy đặt tour

Xây dựng phương thức `huy_dat()`.

**Luồng xử lý:**

1. Kiểm tra trạng thái phiếu đặt tour.
2. Nếu phiếu đã hủy, từ chối thao tác.
3. Nếu phiếu đang chờ xác nhận, chỉ cập nhật trạng thái.
4. Nếu phiếu đã xác nhận, hoàn trả số chỗ tương ứng cho tour.
5. Cập nhật trạng thái thành đã hủy.
6. Trả về kết quả xử lý.

**Ràng buộc:**

- [ ] Không hoàn trả chỗ đối với phiếu chưa xác nhận.
- [ ] Không hoàn trả chỗ hai lần.
- [ ] Không để số chỗ đã đặt trở thành số âm.
- [ ] Phiếu đã hủy không được tính vào doanh thu.

#### e. Hoàn thiện nghiệp vụ tính tổng tiền

Công thức đề xuất:

Tiền vé = Giá vé thực tế × Số lượng vé

Tiền dịch vụ = Tổng chi phí các dịch vụ đã chọn

Tổng tiền = Tiền vé + Tiền dịch vụ

- [ ] Sử dụng phương thức tính giá vé đã xây dựng trong lớp Tour.
- [ ] Đảm bảo áp dụng đúng đa hình đối với tour nội địa và quốc tế.
- [ ] Thống nhất dịch vụ nào tính theo người, dịch vụ nào tính theo phiếu.
- [ ] Không tính trùng chi phí dịch vụ.
- [ ] Kiểm tra trường hợp khách không chọn dịch vụ bổ sung.
- [ ] Lưu tổng tiền tại thời điểm xác nhận đặt tour.
- [ ] Không tự động thay đổi giá trị phiếu đã xác nhận khi giá tour thay đổi sau đó.

Ví dụ:

- Giá vé: 2.000.000 đồng/người.
- Số lượng: 3 người.
- Dịch vụ bổ sung: 300.000 đồng/người.
- Tổng tiền: 6.900.000 đồng.

#### f. Hoàn thiện chuyển đổi dữ liệu

- [ ] Kiểm tra phương thức `to_dict()` của PhieuDatTour.
- [ ] Lưu mã tour, thông tin khách hàng, số lượng vé và dịch vụ.
- [ ] Lưu ngày đặt, trạng thái và tổng tiền.
- [ ] Phối hợp với thành viên phụ trách `tour_manager.py` để khôi phục phiếu đặt từ JSON.
- [ ] Khi đọc lại phiếu đã xác nhận, không thực hiện xác nhận lần nữa làm tăng số chỗ đã đặt.

#### g. Phác thảo giao diện dự kiến

Chỉ thiết kế bố cục bằng hình ảnh, giấy, Canva hoặc Figma. Không lập trình Tkinter.

Các màn hình cần phác thảo:

- [ ] Đăng nhập và đăng ký tài khoản.
- [ ] Trang quản lý danh sách tour.
- [ ] Trang chi tiết lịch trình nhiều ngày.
- [ ] Trang đăng ký đặt tour và lựa chọn dịch vụ.
- [ ] Trang quản lý phiếu đặt tour.
- [ ] Trang thống kê.

Mỗi màn hình cần thể hiện:

- Các thông tin cần hiển thị.
- Các trường nhập dữ liệu.
- Các nút chức năng.
- Luồng chuyển sang màn hình khác.

#### h. Kiểm thử và tài liệu

- [ ] Kiểm thử đặt tour thành công.
- [ ] Kiểm thử đặt vượt số chỗ.
- [ ] Kiểm thử xác nhận một phiếu hai lần.
- [ ] Kiểm thử hủy phiếu đã xác nhận.
- [ ] Kiểm thử hủy phiếu chưa xác nhận.
- [ ] Kiểm thử hủy phiếu hai lần.
- [ ] Kiểm thử tính tổng tiền khi có và không có dịch vụ.
- [ ] Tổng hợp kết quả kiểm thử từ tất cả thành viên.
- [ ] Lập bảng kiểm thử tối thiểu 10 trường hợp ở cấp toàn hệ thống.
- [ ] Viết báo cáo về lịch trình, phiếu đặt tour và nghiệp vụ tính tiền.

---

### 2.4. Nguyễn Hữu Phương Uyên

**File phụ trách:**
- `controllers/tour_manager.py` (bổ sung)
- `utils/file_helper.py` (bổ sung)
- `config.py` (tạo mới)
- `main.py` (tạo mới)

#### a. Hoàn thiện chức năng tìm kiếm tour

Bổ sung tiêu chí ngày khởi hành vào phương thức `tim_kiem()` hiện có.

Các tiêu chí tìm kiếm:

| Tiêu chí | Yêu cầu |
| --- | --- |
| Điểm đến | Tìm theo tên hoặc từ khóa |
| Mức giá | Lọc theo giá vé thực tế |
| Ngày khởi hành | Tìm theo ngày khởi hành |
| Kết hợp | Cho phép tìm theo nhiều tiêu chí cùng lúc |

- [ ] Không phân biệt chữ hoa và chữ thường khi tìm theo điểm đến.
- [ ] Kiểm tra giá trị lọc không hợp lệ.
- [ ] Sử dụng giá vé thực tế của tour để so sánh mức giá.
- [ ] Nếu không nhập tiêu chí thì trả về danh sách phù hợp với các tiêu chí còn lại.
- [ ] Nếu không tìm thấy kết quả thì trả về danh sách rỗng và thông báo phù hợp.

#### b. Hoàn thiện chức năng cập nhật và xóa tour

- [ ] Kiểm tra mã tour có tồn tại trước khi cập nhật hoặc xóa.
- [ ] Không cho phép cập nhật giá vé thành giá trị âm hoặc bằng 0.
- [ ] Không cho phép số chỗ tối đa nhỏ hơn số chỗ đã đặt.
- [ ] Cho phép cập nhật các thuộc tính riêng của tour nội địa và quốc tế.
- [ ] Không cho phép xóa tour đang có phiếu đặt đã xác nhận.
- [ ] Xử lý phù hợp các phiếu đặt liên quan trước khi xóa tour.
- [ ] Chỉ thông báo thành công khi dữ liệu được cập nhật và lưu thành công.

#### c. Bổ sung quản lý danh sách phiếu đặt tour

Trong lớp `QuanLyTour`, bổ sung thuộc tính:

| Thuộc tính | Kiểu dữ liệu | Ý nghĩa |
| --- | --- | --- |
| `ds_phieu_dat` | List | Danh sách các đối tượng PhieuDatTour |

Các phương thức đề xuất:

| Phương thức | Chức năng |
| --- | --- |
| `them_phieu_dat(phieu)` | Thêm phiếu đặt vào hệ thống |
| `lay_ds_phieu_dat()` | Lấy danh sách phiếu đặt |
| `tim_phieu_dat(ma_phieu)` | Tìm phiếu theo mã |
| `tim_phieu_theo_khach(ma_khach)` | Tìm phiếu theo khách hàng |
| `xac_nhan_phieu_dat(ma_phieu)` | Gọi nghiệp vụ xác nhận đặt tour |
| `huy_phieu_dat(ma_phieu)` | Gọi nghiệp vụ hủy đặt tour |
| `luu_phieu_dat()` | Lưu danh sách phiếu vào JSON |
| `tai_phieu_dat()` | Khôi phục danh sách phiếu từ JSON |

**Luồng thêm phiếu đặt:**

1. Kiểm tra mã phiếu không bị trùng.
2. Kiểm tra tour có tồn tại trong hệ thống.
3. Kiểm tra thông tin khách hàng và số lượng vé.
4. Thêm phiếu vào danh sách.
5. Lưu dữ liệu.
6. Trả về kết quả xử lý.

**Luồng xác nhận phiếu:**

1. Tìm phiếu theo mã.
2. Kiểm tra quyền thực hiện.
3. Gọi phương thức xác nhận của lớp PhieuDatTour.
4. Lưu lại dữ liệu tour và phiếu đặt.
5. Trả về kết quả xử lý.

**Luồng hủy phiếu:**

1. Tìm phiếu theo mã.
2. Kiểm tra quyền thực hiện.
3. Gọi phương thức `huy_dat()` của lớp PhieuDatTour.
4. Lưu trạng thái phiếu và số chỗ mới của tour.
5. Trả về kết quả xử lý.

Lưu ý: Không viết lại nghiệp vụ tính tiền, đặt chỗ hoặc hủy chỗ đã có trong `booking.py`. Lớp QuanLyTour chỉ chịu trách nhiệm điều phối và quản lý danh sách.

#### d. Hoàn thiện chức năng thống kê

**Thống kê doanh thu:**

- [ ] Tính doanh thu dựa trên tổng tiền của các phiếu đã xác nhận.
- [ ] Tính cả chi phí dịch vụ đã được ghi nhận.
- [ ] Không tính phiếu đang chờ xác nhận.
- [ ] Không tính phiếu đã hủy.
- [ ] Có thể tổng hợp doanh thu theo từng tour.

Công thức:

Doanh thu = Tổng tiền của tất cả phiếu đặt đã xác nhận.

**Thống kê tỷ lệ lấp đầy:**

Tỷ lệ lấp đầy = Số chỗ đã đặt / Số chỗ tối đa × 100%.

- [ ] Kiểm tra trường hợp số chỗ tối đa không hợp lệ.
- [ ] Kết quả phải nằm trong khoảng từ 0% đến 100%.
- [ ] Kiểm tra tỷ lệ lấp đầy thay đổi chính xác sau khi đặt hoặc hủy tour.

#### e. Hoàn thiện module file_helper.py

Tái sử dụng các hàm đọc, ghi JSON và xuất CSV/TXT đã xây dựng trong giai đoạn 1.

**Bổ sung kiểm tra đọc file:**

- [ ] File không tồn tại.
- [ ] File rỗng.
- [ ] JSON sai định dạng.
- [ ] Không có quyền đọc file.
- [ ] Dữ liệu đọc được không đúng cấu trúc mong đợi.

**Bổ sung kiểm tra ghi file:**

- [ ] Tự động tạo thư mục dữ liệu nếu chưa tồn tại.
- [ ] Kiểm tra lỗi ghi file.
- [ ] Không thông báo lưu thành công khi ghi file thất bại.
- [ ] Ưu tiên ghi vào file tạm trước khi thay thế file chính.
- [ ] Có phương án sao lưu hoặc khôi phục dữ liệu.
- [ ] Không tự động ghi đè file dữ liệu bị lỗi bằng danh sách rỗng.
- [ ] Khi cập nhật nhiều file liên quan, phải có cách xử lý nếu một bước lưu thất bại.

**Hoàn thiện xuất CSV:**

- [ ] Kiểm tra tiêu đề các cột.
- [ ] Đảm bảo dữ liệu xuất đúng với danh sách hiện tại.
- [ ] Kiểm tra mã hóa tiếng Việt.
- [ ] Thông báo kết quả xuất file.

**Hoàn thiện xuất lịch trình TXT:**

Nội dung file cần có:

- Mã tour.
- Tên tour.
- Điểm đến.
- Ngày khởi hành.
- Số ngày.
- Giá vé.
- Nội dung lịch trình ngày 1.
- Nội dung lịch trình ngày 2.
- Các ngày tiếp theo.

#### f. Thiết kế cấu trúc dữ liệu JSON

Tạo thư mục `data/`.

Các file dự kiến:

| File | Nội dung |
| --- | --- |
| `tours.json` | Danh sách tour và lịch trình |
| `bookings.json` | Danh sách phiếu đặt, khách hàng và dịch vụ liên quan |
| `users.json` | Danh sách tài khoản |
| `destinations.json` | Dữ liệu điểm đến từ Crawl/API |

**Yêu cầu:**

- [ ] Thống nhất tên trường dữ liệu với từng thành viên.
- [ ] Chuẩn bị các tour nội địa và quốc tế mẫu.
- [ ] Chuẩn bị các tour có lịch trình nhiều ngày.
- [ ] Chuẩn bị phiếu đặt ở các trạng thái khác nhau.
- [ ] Dùng thông tin khách hàng và tài khoản giả lập để kiểm thử.
- [ ] Khi đọc lại dữ liệu, khôi phục đúng lớp TourNoiDia hoặc TourQuocTe.
- [ ] Khôi phục đầy đủ danh sách lịch trình.
- [ ] Khôi phục các đối tượng khách hàng và dịch vụ.
- [ ] Liên kết phiếu đặt với đúng đối tượng Tour trong danh sách quản lý.
- [ ] Không tạo các đối tượng Tour độc lập gây sai lệch số chỗ.
- [ ] Không cộng lại số chỗ của phiếu đã xác nhận khi khởi động chương trình.

#### g. Tạo file config.py

Quản lý các đường dẫn và hằng số dùng chung.

Các hằng số đề xuất:

| Hằng số | Ý nghĩa |
| --- | --- |
| `DATA_DIR` | Đường dẫn thư mục dữ liệu |
| `TOURS_FILE` | Đường dẫn tours.json |
| `BOOKINGS_FILE` | Đường dẫn bookings.json |
| `USERS_FILE` | Đường dẫn users.json |
| `DESTINATIONS_FILE` | Đường dẫn destinations.json |
| `ROLE_ADMIN` | Vai trò quản trị viên |
| `ROLE_USER` | Vai trò người dùng |
| `STATUS_PENDING` | Trạng thái chờ xác nhận |
| `STATUS_CONFIRMED` | Trạng thái đã xác nhận |
| `STATUS_CANCELLED` | Trạng thái đã hủy |

- [ ] Sử dụng đường dẫn tương đối với thư mục project.
- [ ] Đảm bảo chương trình chạy được khi chuyển sang máy khác.
- [ ] Không sử dụng đường dẫn tuyệt đối chỉ tồn tại trên máy cá nhân.
- [ ] Không lưu mật khẩu hoặc API key trực tiếp trong mã nguồn.

#### h. Tạo file main.py và tích hợp chương trình

Tạo file `main.py` để chạy thử chương trình trên Console.

Menu dự kiến:

1. Đăng ký tài khoản.
2. Đăng nhập.
3. Hiển thị danh sách tour.
4. Thêm tour.
5. Cập nhật tour.
6. Xóa tour.
7. Tìm kiếm tour.
8. Xem lịch trình.
9. Đặt tour.
10. Xem phiếu đặt tour.
11. Hủy phiếu đặt tour.
12. Thống kê doanh thu.
13. Thống kê tỷ lệ lấp đầy.
14. Xuất báo cáo.
15. Lấy dữ liệu điểm đến từ API.
16. Đổi mật khẩu.
17. Đăng xuất.
0. Thoát chương trình.

Menu hiển thị chức năng phù hợp với vai trò của tài khoản.

**Yêu cầu:**

- [ ] Import và sử dụng các module của từng thành viên.
- [ ] Khởi tạo đối tượng quản lý tour và tài khoản.
- [ ] Đọc dữ liệu từ JSON khi chương trình khởi động.
- [ ] Kiểm tra và xử lý lựa chọn menu.
- [ ] Kiểm tra quyền trước khi thực hiện chức năng.
- [ ] Xử lý trường hợp người dùng nhập sai kiểu dữ liệu.
- [ ] Gọi các phương thức nghiệp vụ đã xây dựng.
- [ ] Lưu dữ liệu sau khi thực hiện thay đổi.
- [ ] Không viết toàn bộ nghiệp vụ trực tiếp trong main.py.
- [ ] Không sử dụng Tkinter trong giai đoạn này.

#### i. Kiểm thử và tài liệu

- [ ] Kiểm thử tìm kiếm theo từng tiêu chí.
- [ ] Kiểm thử tìm kiếm kết hợp nhiều tiêu chí.
- [ ] Kiểm thử cập nhật tour có dữ liệu không hợp lệ.
- [ ] Kiểm thử xóa tour đang có khách đăng ký.
- [ ] Kiểm thử lưu và đọc lại phiếu đặt tour.
- [ ] Kiểm thử thống kê doanh thu sau khi hủy phiếu.
- [ ] Kiểm thử file JSON sai định dạng.
- [ ] Kiểm thử tích hợp toàn bộ module.
- [ ] Cập nhật README.md hướng dẫn chạy chương trình.
- [ ] Mô tả cấu trúc thư mục và cấu trúc dữ liệu JSON trong báo cáo.

---

## 3. Nhiệm vụ chung của cả nhóm

### 3.1. Thống nhất mã nguồn

- [ ] Thống nhất tên lớp, thuộc tính và phương thức.
- [ ] Thống nhất cách truyền đối tượng giữa các module.
- [ ] Thống nhất cấu trúc dữ liệu JSON.
- [ ] Thống nhất công thức tính giá vé và dịch vụ.
- [ ] Thống nhất trạng thái phiếu đặt tour.
- [ ] Thống nhất chức năng và quyền của Admin, User.
- [ ] Không viết trùng chức năng giữa các thành viên.

### 3.2. Kiểm thử tích hợp

Thực hiện tối thiểu một quy trình hoàn chỉnh:

1. Đăng ký tài khoản.
2. Đăng nhập.
3. Tạo hoặc xem tour có lịch trình nhiều ngày.
4. Tìm kiếm tour.
5. Chọn khách hàng và dịch vụ.
6. Tạo phiếu đặt tour.
7. Xác nhận đặt tour.
8. Kiểm tra số chỗ còn lại.
9. Kiểm tra tổng tiền.
10. Kiểm tra doanh thu.
11. Tắt và khởi động lại chương trình.
12. Kiểm tra dữ liệu đã lưu.
13. Hủy phiếu đặt tour.
14. Kiểm tra số chỗ và doanh thu sau khi hủy.

Bảng kiểm thử cần có:

| Mã kiểm thử | Chức năng | Dữ liệu đầu vào | Kết quả mong đợi | Kết quả thực tế | Pass/Fail | Người kiểm thử |
| --- | --- | --- | --- | --- | --- | --- |

Không đánh dấu Pass khi chưa thực hiện kiểm thử thực tế.

### 3.3. Tài liệu báo cáo tiến độ

| Nội dung | Người phụ trách |
| --- | --- |
| Mục tiêu, phạm vi và phân tích yêu cầu | Trương Lý Bảo Ngân |
| Use Case Diagram | Trương Lý Bảo Ngân |
| Class Diagram | Nguyễn Thị Phương Uyên |
| Thiết kế cấu trúc dữ liệu JSON | Nguyễn Hữu Phương Uyên |
| Phác thảo giao diện | Đỗ Yến Nhi |
| Tổng hợp bảng kiểm thử | Đỗ Yến Nhi |
| Cấu trúc mã nguồn và hướng dẫn chạy | Nguyễn Hữu Phương Uyên |
| Mô tả chức năng đã thực hiện | Tất cả thành viên |
| Báo cáo tiến độ tuần 10 | Tất cả thành viên |

---

## 4. Cấu trúc thư mục dự kiến

    Nhom06_lop_python_06/
    ├── models/
    │   ├── tour.py
    │   ├── customer.py
    │   ├── booking.py
    │   └── user.py
    ├── controllers/
    │   ├── tour_manager.py
    │   └── auth_manager.py
    ├── utils/
    │   ├── file_helper.py
    │   └── api_helper.py
    ├── data/
    │   ├── tours.json
    │   ├── bookings.json
    │   ├── users.json
    │   └── destinations.json
    ├── docs/
    ├── tests/
    ├── config.py
    ├── main.py
    ├── README.md
    └── PHAN_CONG.md

---

## 5. Kết quả cần đạt trước báo cáo tiến độ tuần 10

- [ ] Các lớp nghiệp vụ được hoàn thiện và liên kết với nhau.
- [ ] Quản lý được tour và lịch trình nhiều ngày.
- [ ] Thực hiện được nghiệp vụ đặt tour và hủy tour.
- [ ] Tính đúng giá vé và dịch vụ.
- [ ] Thực hiện được CRUD và tìm kiếm.
- [ ] Thống kê được doanh thu và tỷ lệ lấp đầy.
- [ ] Lưu và khôi phục được dữ liệu JSON.
- [ ] Có dữ liệu mẫu để chạy thử.
- [ ] Có chức năng tài khoản và phân quyền cơ bản.
- [ ] Có chức năng Crawl/API cơ bản.
- [ ] Có chương trình Console để demo.
- [ ] Có tài liệu phân tích yêu cầu.
- [ ] Có Use Case Diagram và Class Diagram.
- [ ] Có tài liệu thiết kế dữ liệu.
- [ ] Có bản phác thảo giao diện.
- [ ] Có bảng kiểm thử và kết quả kiểm thử thực tế.
- [ ] Có báo cáo tiến độ tuần 10.

---

## 6. Lưu ý

- Kế thừa toàn bộ mã nguồn đã hoàn thành trong giai đoạn 1.
- Chỉ bổ sung hoặc chỉnh sửa những chức năng còn thiếu.
- Tên thuộc tính và phương thức trong bảng phân công là đề xuất, cần thống nhất với mã nguồn hiện có trước khi triển khai.
- Mỗi thành viên phải kiểm thử phần việc của mình trước khi đưa lên nhánh main.
- Không lập trình giao diện Tkinter trong giai đoạn này.
- Phần giao diện chỉ dừng ở mức phác thảo bố cục.
- Chưa thực hiện đóng gói ứng dụng thành file EXE.
- Tài khoản, phân quyền và Crawl/API được triển khai sớm để giảm khối lượng công việc cuối kỳ.
- Tỷ lệ đóng góp được điều chỉnh theo kết quả thực hiện thực tế.
