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

* **Học phần:** Lập trình Python
* **Đề tài 19:** Hệ thống quản lý tour và lịch trình du lịch
* **Giai đoạn thực hiện:** Giai đoạn 2 – Hoàn thiện chức năng nghiệp vụ, xử lý dữ liệu, tích hợp mã nguồn và chuẩn bị báo cáo tiến độ tuần 10.

---

### 1. Bảng tổng hợp phân công nhiệm vụ và tỷ lệ đóng góp

| STT | Họ và tên | File phụ trách | Nhiệm vụ chính | Tỷ lệ đóng góp |
|:---:|:---|:---|:---|:---:|
| 1 | **Nguyễn Thị Phương Uyên** | `models/tour.py`<br>`utils/api_helper.py` | Hoàn thiện lớp Tour, quản lý lịch trình nhiều ngày, Crawl/API và sơ đồ lớp | 25% |
| 2 | **Trương Lý Bảo Ngân** | `models/customer.py`<br>`models/user.py`<br>`controllers/auth_manager.py` | Hoàn thiện khách hàng, dịch vụ, đăng nhập, đăng ký và phân quyền | 25% |
| 3 | **Đỗ Yến Nhi** | `models/booking.py` | Hoàn thiện lịch trình, nghiệp vụ đặt tour, hủy tour, tính tiền và tổng hợp kiểm thử | 25% |
| 4 | **Nguyễn Hữu Phương Uyên** | `controllers/tour_manager.py`<br>`utils/file_helper.py`<br>`config.py`<br>`main.py` | Hoàn thiện quản lý tour, phiếu đặt tour, lưu trữ JSON, thống kê và tích hợp chương trình | 25% |

---

### 2. Chi tiết phân công nhiệm vụ từng thành viên

#### 1. Nguyễn Thị Phương Uyên

* **File phụ trách:** `models/tour.py` (bổ sung) và `utils/api_helper.py` (tạo mới).

* **Chi tiết nhiệm vụ:**

**a. Bổ sung chức năng quản lý lịch trình nhiều ngày**

* Bổ sung thuộc tính `ds_lich_trinh` có kiểu List trong lớp `Tour` để lưu danh sách các đối tượng `LichTrinhNgay` đã được xây dựng trong `booking.py`.
* Viết phương thức `them_lich_trinh(lich_trinh)`: thêm lịch trình của một ngày vào tour, kiểm tra không trùng ngày và không vượt quá số ngày của tour.
* Viết phương thức `sua_lich_trinh(ngay_thu, ...)`: sử dụng vòng lặp để tìm lịch trình theo số thứ tự ngày và cập nhật nội dung hoạt động.
* Viết phương thức `xoa_lich_trinh(ngay_thu)`: tìm và xóa lịch trình của ngày tương ứng.
* Viết phương thức `lay_lich_trinh()`: trả về danh sách lịch trình của tour theo thứ tự ngày.
* Cập nhật phương thức `to_dict()` để chuyển đổi danh sách lịch trình thành dữ liệu phục vụ lưu trữ JSON.

Ví dụ: Tour Đà Lạt 3 ngày chỉ được thêm lịch trình ngày 1, ngày 2 và ngày 3; không được thêm trùng ngày hoặc thêm ngày 4.

**b. Hoàn thiện kiểm tra dữ liệu của lớp Tour**

* Sử dụng câu lệnh điều kiện để kiểm tra mã tour, tên tour và điểm đến không được bỏ trống.
* Kiểm tra giá vé lớn hơn 0; số ngày và số chỗ tối đa là số nguyên dương; phụ thu và phí visa không được âm.
* Kiểm tra ngày khởi hành đúng định dạng ngày tháng và là ngày hợp lệ.
* Kiểm tra lại các phương thức `kiem_tra_con_cho()`, `dat_cho()` và `huy_cho()`, đảm bảo không đặt vượt số chỗ còn lại hoặc hủy nhiều hơn số chỗ đã đặt.
* Sử dụng ngoại lệ `ValueError` để thông báo khi dữ liệu không hợp lệ.

**c. Xây dựng chức năng Crawl/API**

* Tạo file `utils/api_helper.py` để lấy thông tin điểm đến du lịch từ một website hoặc API công khai phù hợp.
* Sử dụng thư viện `requests` hoặc thư viện phù hợp để gửi yêu cầu và nhận dữ liệu.
* Viết hàm `lay_du_lieu_diem_den(tu_khoa)`: nhận tên địa điểm cần tìm và lấy dữ liệu từ nguồn bên ngoài.
* Sử dụng List, Dictionary và vòng lặp để trích xuất các thông tin cần thiết như tên địa điểm, địa chỉ và tọa độ nếu có.
* Lưu dữ liệu điểm đến vào danh sách `destinations` trong file `data/data.json`, sử dụng lại hàm ghi JSON trong `file_helper.py`.
* Sử dụng `try...except` để xử lý lỗi kết nối hoặc trường hợp không lấy được dữ liệu. Không ghi đè dữ liệu cũ khi API gặp lỗi.

Ví dụ: Nhập từ khóa "Đà Lạt", chương trình lấy thông tin địa điểm từ API và lưu kết quả vào JSON để sử dụng khi xây dựng tour.

**d. Kiểm thử và tài liệu**

* Kiểm thử thêm, sửa, xóa lịch trình; lịch trình trùng ngày; lịch trình vượt số ngày; giá vé âm và số chỗ không hợp lệ.
* Kiểm thử chức năng Crawl/API và ghi rõ nguồn dữ liệu sử dụng.
* Vẽ Class Diagram thể hiện các lớp, thuộc tính, phương thức và mối quan hệ giữa các lớp trong chương trình.
* Viết nội dung báo cáo tương ứng với phần công việc phụ trách.

---

#### 2. Trương Lý Bảo Ngân

* **File phụ trách:** `models/customer.py` (bổ sung), `models/user.py` và `controllers/auth_manager.py` (tạo mới).

* **Chi tiết nhiệm vụ:**

**a. Hoàn thiện lớp KhachHang và DichVu**

* Bổ sung kiểm tra mã khách hàng, họ tên không được bỏ trống.
* Kiểm tra lại Regular Expression (`re`) kiểm tra số điện thoại và email đã xây dựng ở giai đoạn 1.
* Bổ sung kiểm tra mã dịch vụ, tên dịch vụ không được bỏ trống và đơn giá không được âm.
* Sử dụng `ValueError` khi thông tin khách hàng hoặc dịch vụ không hợp lệ.
* Kiểm tra lại phương thức `to_dict()` của hai lớp để đảm bảo lưu đầy đủ thông tin vào JSON.

**b. Xây dựng lớp TaiKhoan**

* Tạo file `models/user.py` và xây dựng lớp `TaiKhoan` gồm các thuộc tính:
  * `ma_tai_khoan`: mã tài khoản.
  * `ten_dang_nhap`: tên dùng để đăng nhập.
  * `mat_khau_hash`: mật khẩu đã được băm.
  * `ho_ten`: họ tên người dùng.
  * `vai_tro`: Admin hoặc User.
* Sử dụng constructor và tính đóng gói để quản lý thông tin tài khoản.
* Viết phương thức `kiem_tra_mat_khau()` để kiểm tra mật khẩu người dùng nhập.
* Viết phương thức `doi_mat_khau()` để cập nhật mật khẩu mới.
* Viết phương thức `to_dict()` để chuyển đổi đối tượng tài khoản thành Dictionary.
* Tham khảo thư viện hỗ trợ băm mật khẩu phù hợp để không lưu mật khẩu gốc trong JSON.

**c. Xây dựng chức năng đăng ký, đăng nhập và phân quyền**

* Tạo file `controllers/auth_manager.py` và xây dựng lớp `QuanLyTaiKhoan`.
* Khai báo thuộc tính `ds_tai_khoan` có kiểu List để quản lý danh sách tài khoản và `tai_khoan_hien_tai` để lưu tài khoản đang đăng nhập.
* Viết phương thức `dang_ky()`: nhận thông tin đăng ký, sử dụng vòng lặp kiểm tra tên đăng nhập có bị trùng không, tạo tài khoản mới với vai trò User và lưu vào danh sách.
* Viết phương thức `dang_nhap(ten_dang_nhap, mat_khau)`: tìm tài khoản theo tên đăng nhập, kiểm tra mật khẩu và trả về kết quả đăng nhập thành công hoặc thất bại.
* Viết phương thức `dang_xuat()`: đưa `tai_khoan_hien_tai` về `None`.
* Viết phương thức `doi_mat_khau()` để kiểm tra mật khẩu hiện tại trước khi cập nhật mật khẩu mới.
* Viết phương thức `kiem_tra_quyen()` sử dụng câu lệnh `if...else` để kiểm tra vai trò của tài khoản.
* Phân chia chức năng giữa Admin và User:

| Chức năng | Admin | User |
|:---|:---:|:---:|
| Xem và tìm kiếm tour | Có | Có |
| Xem lịch trình | Có | Có |
| Thêm, sửa, xóa tour | Có | Không |
| Quản lý lịch trình | Có | Không |
| Đặt tour | Có | Có |
| Xem và hủy phiếu đặt của mình | Có | Có |
| Quản lý tất cả phiếu đặt tour | Có | Không |
| Thống kê và xuất báo cáo | Có | Không |
| Đổi mật khẩu cá nhân | Có | Có |

* Liên kết tài khoản với mã khách hàng để xác định phiếu đặt tour thuộc về người dùng nào.
* Viết phương thức `tai_du_lieu()` và `luu_du_lieu()` để đọc, ghi danh sách tài khoản vào file `data/users.json`, sử dụng lại module `file_helper.py`.

**d. Kiểm thử và tài liệu**

* Kiểm thử thông tin khách hàng không hợp lệ, đơn giá dịch vụ âm, đăng ký trùng tài khoản, đăng nhập sai mật khẩu và phân quyền.
* Phân tích mục tiêu, phạm vi, đối tượng sử dụng và các chức năng của hệ thống.
* Vẽ Use Case Diagram thể hiện chức năng của Admin và User.
* Viết nội dung báo cáo tương ứng với phần công việc phụ trách.

---

#### 3. Đỗ Yến Nhi

* **File phụ trách:** `models/booking.py` (bổ sung).

* **Chi tiết nhiệm vụ:**

**a. Hoàn thiện lớp LichTrinhNgay**

* Kiểm tra số thứ tự ngày phải là số nguyên dương, tiêu đề hoạt động và nội dung lịch trình không được bỏ trống.
* Kiểm tra lại các thuộc tính lưu nội dung hoạt động theo từng buổi sáng, chiều và tối.
* Đảm bảo phương thức `to_dict()` chuyển đổi đầy đủ thông tin lịch trình thành Dictionary.
* Phối hợp với thành viên phụ trách `tour.py` để liên kết lịch trình từng ngày với tour.

**b. Hoàn thiện lớp PhieuDatTour**

* Bổ sung các thuộc tính còn thiếu:
  * `ngay_dat`: ngày khách hàng đặt tour.
  * `tong_tien`: tổng tiền tại thời điểm xác nhận đặt tour.
  * `trang_thai`: Chờ xác nhận, Đã xác nhận hoặc Đã hủy.
* Kiểm tra mã phiếu đặt không được bỏ trống và số lượng vé phải là số nguyên dương.
* Hoàn thiện phương thức `xac_nhan_dat()`: kiểm tra trạng thái phiếu và số chỗ còn lại, gọi phương thức `dat_cho()` của Tour để cập nhật số chỗ đã đặt, sau đó chuyển trạng thái thành Đã xác nhận.
* Không cho phép xác nhận một phiếu nhiều lần hoặc xác nhận phiếu đã hủy.

Ví dụ: Tour có 20 chỗ, đã đặt 15 chỗ. Nếu khách đăng ký 3 vé thì còn lại 2 chỗ; nếu đăng ký 6 vé thì thông báo không đủ chỗ.

**c. Bổ sung chức năng hủy đặt tour**

* Viết phương thức `huy_dat()` sử dụng câu lệnh điều kiện để kiểm tra trạng thái phiếu.
* Nếu phiếu đang chờ xác nhận thì chỉ chuyển trạng thái thành Đã hủy.
* Nếu phiếu đã xác nhận thì gọi phương thức `huy_cho()` của Tour để hoàn trả số chỗ, sau đó chuyển trạng thái thành Đã hủy.
* Nếu phiếu đã hủy thì thông báo không thể tiếp tục hủy.

Ví dụ: Khách đã đặt 3 vé, tour còn 2 chỗ. Sau khi hủy phiếu, tour phải còn lại 5 chỗ.

**d. Hoàn thiện chức năng tính tổng tiền**

* Kiểm tra lại phương thức `tinh_tong_tien()` theo công thức:

  `tong_tien = (tour.tinh_gia_ve() * so_ve) + tong_tien_dich_vu`

* Sử dụng vòng lặp để tính tổng đơn giá các dịch vụ mà khách hàng lựa chọn.
* Thống nhất cách tính phí dịch vụ theo người hoặc theo phiếu với thành viên phụ trách lớp `DichVu`.
* Đảm bảo tính đúng giá vé của TourNoiDia và TourQuocTe thông qua tính đa hình.
* Lưu tổng tiền khi xác nhận đặt tour để không bị thay đổi khi giá tour được cập nhật sau đó.
* Cập nhật phương thức `to_dict()` để lưu mã phiếu, mã tour, khách hàng, số lượng vé, dịch vụ, ngày đặt, tổng tiền và trạng thái.

**e. Phác thảo giao diện dự kiến**

* Phác thảo bố cục các màn hình đăng nhập, danh sách tour, lịch trình, đặt tour, quản lý phiếu đặt và thống kê.
* Thể hiện các thông tin cần hiển thị, ô nhập dữ liệu và nút chức năng.
* Có thể thực hiện bằng Canva, Figma hoặc vẽ trên giấy, chưa lập trình Tkinter.

**f. Kiểm thử và tài liệu**

* Kiểm thử đặt tour thành công, đặt vượt số chỗ, xác nhận hai lần, hủy tour và tính tổng tiền khi có hoặc không có dịch vụ.
* Tổng hợp bảng kiểm thử tối thiểu 10 trường hợp của cả nhóm, gồm dữ liệu đầu vào, kết quả mong đợi, kết quả thực tế và trạng thái Pass/Fail.
* Viết nội dung báo cáo về lịch trình, đặt tour, hủy tour và tính tiền.

---

#### 4. Nguyễn Hữu Phương Uyên

* **File phụ trách:** `controllers/tour_manager.py`, `utils/file_helper.py` (bổ sung), `config.py` và `main.py` (tạo mới).

* **Chi tiết nhiệm vụ:**

**a. Hoàn thiện chức năng CRUD và tìm kiếm tour**

* Kiểm tra lại phương thức `them_tour()` để đảm bảo không thêm tour trùng mã.
* Hoàn thiện phương thức `cap_nhat_tour()`: kiểm tra dữ liệu cập nhật hợp lệ, không cho phép giảm số chỗ tối đa xuống thấp hơn số chỗ đã đặt.
* Hoàn thiện phương thức `xoa_tour()`: kiểm tra tour có tồn tại và có phiếu đặt liên quan hay không; không xóa tour đang được sử dụng trong phiếu đặt.
* Bổ sung tiêu chí ngày khởi hành vào phương thức `tim_kiem()`.
* Sử dụng vòng lặp và câu lệnh điều kiện để tìm kiếm theo điểm đến, ngày khởi hành và mức giá.
* Sử dụng phương thức `tinh_gia_ve()` để tìm kiếm theo giá vé thực tế thay vì giá vé cơ bản.

**b. Bổ sung quản lý danh sách phiếu đặt tour**

* Bổ sung thuộc tính `ds_phieu_dat` có kiểu List trong lớp `QuanLyTour`.
* Viết phương thức `them_phieu_dat(phieu)`: kiểm tra mã phiếu không trùng lặp, tour tồn tại và thêm phiếu vào danh sách.
* Viết phương thức `lay_ds_phieu_dat()`: trả về danh sách phiếu đặt tour.
* Viết phương thức `tim_phieu_dat(ma_phieu)`: sử dụng vòng lặp để tìm phiếu theo mã.
* Viết phương thức `tim_phieu_theo_khach(ma_khach)`: trả về danh sách phiếu đặt của khách hàng tương ứng.
* Viết phương thức `xac_nhan_phieu_dat(ma_phieu)`: tìm phiếu và gọi phương thức `xac_nhan_dat()` trong `booking.py`.
* Viết phương thức `huy_phieu_dat(ma_phieu)`: tìm phiếu và gọi phương thức `huy_dat()` trong `booking.py`.
* Lưu dữ liệu sau khi thực hiện thành công các thao tác thêm, xác nhận hoặc hủy phiếu đặt tour.

Không viết lại logic đặt chỗ, hủy chỗ và tính tiền đã có trong `booking.py`.

**c. Hoàn thiện chức năng thống kê**

* Chỉnh sửa phương thức `thong_ke_doanh_thu()`: sử dụng vòng lặp để cộng tổng tiền của các phiếu đặt có trạng thái Đã xác nhận.
* Không tính các phiếu Chờ xác nhận hoặc Đã hủy vào doanh thu.
* Kiểm tra lại phương thức `thong_ke_ty_le_lap_day()` theo công thức:

  `ty_le_lap_day = (so_cho_da_dat / so_cho_toi_da) * 100`

* Đảm bảo kết quả thống kê thay đổi đúng sau khi xác nhận hoặc hủy đặt tour.

**d. Hoàn thiện lưu trữ dữ liệu JSON**

* Tạo thư mục `data/` và sử dụng hai file JSON:

| File | Nội dung lưu trữ |
|:---|:---|
| `data.json` | Tour, lịch trình, khách hàng, dịch vụ, phiếu đặt tour và điểm đến từ API |
| `users.json` | Tài khoản và vai trò người dùng |

* Thống nhất cấu trúc `data.json` sử dụng Dictionary chứa các List:

      {
          "tours": [],
          "customers": [],
          "services": [],
          "bookings": [],
          "destinations": []
      }

* Lịch trình từng ngày được lưu bên trong thông tin tour.
* Cập nhật phương thức `luu_du_lieu()`: sử dụng `to_dict()` của các lớp để chuyển đổi đối tượng thành Dictionary, sau đó lưu toàn bộ dữ liệu nghiệp vụ vào `data.json`.
* Cập nhật phương thức `tai_du_lieu()`: đọc file JSON, sử dụng vòng lặp để khôi phục các đối tượng Tour, KhachHang, DichVu, LichTrinhNgay và PhieuDatTour.
* Khi khôi phục phiếu đặt, tìm tour, khách hàng và dịch vụ tương ứng theo mã đã lưu.
* Không gọi lại phương thức xác nhận đặt tour khi đọc JSON để tránh cộng số chỗ nhiều lần.
* Phối hợp với các thành viên để tạo dữ liệu mẫu; có thể sử dụng module `random` để sinh số lượng vé hoặc lựa chọn dữ liệu kiểm thử phù hợp.

**e. Hoàn thiện module file_helper.py**

* Tái sử dụng các hàm `luu_json()` và `doc_json()` đã xây dựng ở giai đoạn 1.
* Sử dụng `with open(...)`, `json.dump()` và `json.load()` để ghi, đọc dữ liệu.
* Sử dụng `try...except` để xử lý trường hợp file không tồn tại, file rỗng, JSON sai định dạng hoặc ghi file thất bại.
* Không thông báo lưu thành công nếu ghi file thất bại; giữ lại dữ liệu cũ nếu có lỗi.
* Kiểm tra lại hàm `xuat_bao_cao_csv()` để đảm bảo xuất đúng dữ liệu.
* Cập nhật hàm `xuat_lich_trinh_text()` để xuất thông tin tour và nội dung lịch trình từng ngày.

**f. Tạo file cấu hình và tích hợp chương trình**

* Tạo file `config.py` để khai báo đường dẫn đến `data.json`, `users.json` và các hằng số về vai trò, trạng thái phiếu đặt.
* Tạo file `main.py` để import và kết nối các module của từng thành viên.
* Khởi tạo các đối tượng quản lý và đọc dữ liệu JSON khi chương trình bắt đầu chạy.
* Xây dựng menu Console đơn giản bằng vòng lặp `while`, câu lệnh `if...elif...else` và hàm `input()`.
* Gọi các phương thức đã xây dựng để chạy thử chức năng đăng nhập, quản lý tour, xem lịch trình, tìm kiếm, đặt tour, hủy tour, thống kê và xuất báo cáo.
* Kiểm tra quyền Admin hoặc User trước khi thực hiện chức năng.
* Sử dụng `try...except` để xử lý trường hợp người dùng nhập sai dữ liệu.
* Có thể sử dụng `sys.exit()` để kết thúc chương trình.

**g. Kiểm thử và tài liệu**

* Kiểm thử CRUD tour, tìm kiếm theo nhiều tiêu chí, quản lý phiếu đặt, thống kê và xuất file.
* Kiểm tra dữ liệu sau khi tắt và khởi động lại chương trình.
* Phối hợp với các thành viên chạy thử toàn bộ các chức năng đã tích hợp.
* Mô tả cấu trúc dữ liệu JSON và cấu trúc thư mục trong báo cáo.
* Cập nhật file `README.md` hướng dẫn chạy chương trình.

---

> **Lưu ý:** Các thành viên chỉ bổ sung và chỉnh sửa những chức năng còn thiếu, không viết lại mã nguồn đã hoàn thành ở giai đoạn 1. Ưu tiên vận dụng các kiến thức Python cơ bản, OOP, xử lý file, Regex, Random, Sys và xử lý ngoại lệ. Giai đoạn này chưa lập trình giao diện Tkinter và chưa đóng gói ứng dụng.

