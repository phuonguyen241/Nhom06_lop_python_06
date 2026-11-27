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






# BẢNG PHÂN CÔNG NHIỆM VỤ GIAI ĐOẠN 2

* **Học phần:** Lập trình Python
* **Đề tài 19:** Hệ thống quản lý tour và lịch trình du lịch
* **Giai đoạn thực hiện:** Giai đoạn 2 – Hoàn thiện chức năng nghiệp vụ, lưu trữ dữ liệu JSON, xử lý ngoại lệ, liên kết các module nghiệp vụ, kiểm thử bước đầu và viết báo cáo tiến độ tuần 10.

---

### 1. Bảng tổng hợp phân công nhiệm vụ và tỷ lệ đóng góp

| STT | Họ và tên | File phụ trách | Nhiệm vụ chính | Tỷ lệ đóng góp dự kiến |
|:---:|:---|:---|:---|:---:|
| 1 | **Nguyễn Thị Phương Uyên** | `models/tour.py`<br>`utils/api_helper.py` | Hoàn thiện lớp Tour, quản lý lịch trình nhiều ngày, Crawl/API và sơ đồ lớp | 25% |
| 2 | **Trương Lý Bảo Ngân** | `models/customer.py`<br>`models/user.py` | Hoàn thiện các lớp khách hàng, dịch vụ, tài khoản, phân quyền và phân tích yêu cầu hệ thống | 25% |
| 3 | **Đỗ Yến Nhi** | `models/booking.py` | Hoàn thiện lịch trình ngày, nghiệp vụ đặt tour, hủy tour, tính tổng chi phí, phác thảo giao diện và tổng hợp kiểm thử bước đầu | 25% |
| 4 | **Nguyễn Hữu Phương Uyên** | `controllers/tour_manager.py`<br>`utils/file_helper.py`<br>`config.py` | Hoàn thiện lớp quản lý nghiệp vụ, quản lý tour, khách hàng, dịch vụ và phiếu đặt, thống kê, lưu trữ JSON, xử lý file và liên kết các module nghiệp vụ | 25% |
| | **Tổng cộng** | | | **100%** |

---

### 2. Chi tiết phân công nhiệm vụ từng thành viên

#### 1. Nguyễn Thị Phương Uyên

* **File phụ trách:**
  * `models/tour.py` (bổ sung).
  * `utils/api_helper.py` (tạo mới).

* **Chi tiết nhiệm vụ lập trình:**

**a. Bổ sung chức năng quản lý lịch trình nhiều ngày**

* Bổ sung thuộc tính `ds_lich_trinh` có kiểu List trong lớp `Tour` để lưu danh sách các đối tượng `LichTrinhNgay` đã được xây dựng trong `booking.py`, không tạo lại lớp này.
* Viết phương thức `them_lich_trinh(lich_trinh)`: nhận đối tượng lịch trình của một ngày, kiểm tra số thứ tự ngày không bị trùng và không vượt quá số ngày của tour trước khi thêm vào danh sách.
* Viết phương thức `sua_lich_trinh(ngay_thu, ...)`: tìm lịch trình theo số thứ tự ngày và cập nhật tiêu đề, nội dung hoạt động của ngày đó.
* Viết phương thức `xoa_lich_trinh(ngay_thu)`: tìm và xóa lịch trình của ngày được chọn; thông báo nếu không tìm thấy.
* Viết phương thức `lay_lich_trinh()`: trả về danh sách lịch trình theo thứ tự ngày tăng dần.
* Cập nhật phương thức `to_dict()` để lưu đầy đủ thông tin tour và danh sách lịch trình phục vụ lưu trữ JSON.
* Đảm bảo phương thức `to_dict()` của `TourNoiDia` và `TourQuocTe` vẫn lưu đầy đủ thông tin riêng của từng loại tour, bao gồm phụ thu và phí visa.

Ví dụ: Tour Đà Lạt 3 ngày chỉ được thêm lịch trình ngày 1, ngày 2 và ngày 3; không được thêm trùng ngày hoặc thêm ngày 4.

**b. Hoàn thiện kiểm tra dữ liệu lớp Tour**

* Kiểm tra mã tour, tên tour và điểm đến không được bỏ trống.
* Kiểm tra giá vé cơ bản phải lớn hơn 0; số ngày và số chỗ tối đa phải là số nguyên dương.
* Kiểm tra số chỗ đã đặt không được âm hoặc vượt quá số chỗ tối đa.
* Kiểm tra ngày khởi hành đúng định dạng ngày tháng do nhóm thống nhất và là ngày hợp lệ.
* Kiểm tra phụ thu của `TourNoiDia` và phí visa của `TourQuocTe` không được âm.
* Kiểm tra lại các phương thức `kiem_tra_con_cho()`, `dat_cho()` và `huy_cho()` để không xảy ra trường hợp đặt vượt số chỗ, đặt số lượng vé không hợp lệ hoặc hủy nhiều hơn số chỗ đã đặt.
* Sử dụng câu lệnh điều kiện và ngoại lệ `ValueError` để xử lý dữ liệu không hợp lệ.

**c. Tìm hiểu và xây dựng chức năng Crawl/API**

* Tạo file `utils/api_helper.py` để lấy dữ liệu điểm đến du lịch từ một website hoặc API công khai phù hợp.
* Lựa chọn một phương pháp thực hiện: Crawl dữ liệu hoặc sử dụng API, không cần thực hiện cả hai.
* Viết hàm `lay_du_lieu_diem_den(tu_khoa)` để lấy thông tin địa điểm du lịch dựa trên từ khóa được nhập.
* Sử dụng List, Dictionary và vòng lặp để trích xuất các thông tin cần thiết như tên địa điểm, địa chỉ và tọa độ nếu nguồn dữ liệu có cung cấp.
* Kiểm tra và loại bỏ dữ liệu trùng lặp hoặc không hợp lệ.
* Sử dụng `try...except` để xử lý lỗi kết nối, thời gian chờ hoặc trường hợp không lấy được dữ liệu.
* Trả về danh sách điểm đến đã xử lý; phối hợp với thành viên phụ trách `tour_manager.py` để lưu vào danh sách `destinations` trong file `data.json`.
* Ghi lại nguồn dữ liệu và thư viện sử dụng để phục vụ viết báo cáo.

Ví dụ: Nhập từ khóa "Đà Lạt", chương trình lấy thông tin các địa điểm phù hợp từ nguồn bên ngoài để hỗ trợ xây dựng lịch trình du lịch.

* **Nhiệm vụ kiểm thử:**
  * Kiểm thử thêm, sửa và xóa lịch trình.
  * Kiểm thử thêm lịch trình trùng ngày hoặc vượt số ngày của tour.
  * Kiểm thử giá vé âm, số chỗ không hợp lệ và đặt vượt số chỗ.
  * Kiểm thử tính giá vé tour nội địa và tour quốc tế.
  * Kiểm thử chức năng Crawl/API theo tiến độ thực tế.
  * Gửi kết quả kiểm thử cho Đỗ Yến Nhi tổng hợp.

* **Nội dung báo cáo phụ trách:**

**Đợt 1 – Viết song song với lập trình**

* **Mục 2.3.5. Xây dựng lịch trình du lịch:**
  * Mô tả chức năng quản lý lịch trình nhiều ngày.
  * Trình bày dữ liệu đầu vào, quá trình xử lý và kết quả đầu ra.
  * Vẽ Flowchart cho các thao tác thêm, sửa và xóa lịch trình.
  * Đưa ra ví dụ minh họa lịch trình của một tour du lịch.

* **Sơ đồ lớp (Class Diagram):**
  * Thể hiện các lớp, thuộc tính, phương thức và mối quan hệ theo mã nguồn nghiệp vụ.

* **Mục 2.5. Phương pháp Crawl dữ liệu hoặc sử dụng API:**
  * Giới thiệu website hoặc API được lựa chọn.
  * Trình bày thư viện và phương pháp thu thập dữ liệu.
  * Mô tả cách xử lý và lưu trữ dữ liệu vào JSON.
  * Ghi rõ nguồn dữ liệu được sử dụng.
  * Trình bày theo tiến độ thực tế.

---

#### 2. Trương Lý Bảo Ngân

* **File phụ trách:**
  * `models/customer.py` (bổ sung).
  * `models/user.py` (tạo mới).

* **Chi tiết nhiệm vụ lập trình:**

**a. Hoàn thiện lớp KhachHang và DichVu**

* Bổ sung kiểm tra mã khách hàng và họ tên không được bỏ trống.
* Kiểm tra lại Regular Expression (`re`) dùng để kiểm tra số điện thoại và email đã xây dựng trong giai đoạn 1.
* Đảm bảo thông tin khách hàng được kiểm tra khi khởi tạo hoặc cập nhật.
* Bổ sung kiểm tra mã dịch vụ, tên dịch vụ không được bỏ trống và đơn giá phải là số không âm.
* Sử dụng ngoại lệ `ValueError` khi thông tin khách hàng hoặc dịch vụ không hợp lệ.
* Kiểm tra lại phương thức `to_dict()` của hai lớp để đảm bảo lưu đầy đủ thông tin vào JSON.
* Thống nhất với thành viên phụ trách `booking.py` về cách tính phí dịch vụ. Các dịch vụ bổ sung được tính theo người.

**b. Xây dựng lớp TaiKhoan**

* Tạo file `models/user.py` và xây dựng lớp `TaiKhoan` gồm các thuộc tính:
  * `ma_tai_khoan`: mã định danh tài khoản.
  * `ten_dang_nhap`: tên dùng để đăng nhập.
  * `mat_khau_hash`: mật khẩu đã được băm.
  * `ho_ten`: họ tên người dùng.
  * `vai_tro`: Admin hoặc User.
  * `ma_khach_hang`: mã khách hàng liên kết với tài khoản User.
* Sử dụng constructor và tính đóng gói để quản lý thông tin tài khoản.
* Kiểm tra tên đăng nhập và mật khẩu không được bỏ trống.
* Viết phương thức `kiem_tra_mat_khau(mat_khau)` để kiểm tra mật khẩu người dùng nhập.
* Viết phương thức `doi_mat_khau(mat_khau_moi)` để cập nhật mật khẩu mới.
* Viết phương thức `to_dict()` để chuyển thông tin tài khoản thành Dictionary phục vụ lưu JSON.
* Tìm hiểu thư viện hỗ trợ băm mật khẩu có sẵn, không tự xây dựng thuật toán bảo mật.
* Sử dụng các hằng số vai trò được khai báo trong `config.py`.

**c. Xây dựng lớp QuanLyTaiKhoan**

* Xây dựng lớp `QuanLyTaiKhoan` ngay trong file `models/user.py`, không tạo thêm file quản lý tài khoản.
* Khai báo thuộc tính `ds_tai_khoan` có kiểu List để quản lý danh sách tài khoản và `tai_khoan_hien_tai` để lưu tài khoản đang đăng nhập.
* Viết phương thức `dang_ky()`: nhận thông tin đăng ký, kiểm tra tên đăng nhập không bị trùng, tạo tài khoản mới với vai trò User và lưu dữ liệu.
* Viết phương thức `dang_nhap(ten_dang_nhap, mat_khau)`: sử dụng vòng lặp để tìm tài khoản theo tên đăng nhập, kiểm tra mật khẩu và ghi nhận tài khoản đang đăng nhập nếu thông tin chính xác.
* Viết phương thức `dang_xuat()`: đưa tài khoản đang đăng nhập về `None`.
* Viết phương thức `doi_mat_khau()`: kiểm tra người dùng đã đăng nhập và mật khẩu hiện tại trước khi cập nhật mật khẩu mới.
* Viết phương thức `kiem_tra_quyen()` sử dụng câu lệnh điều kiện để kiểm tra vai trò của tài khoản.
* Sử dụng các hàm `luu_json()` và `doc_json()` trong `file_helper.py` để lưu và đọc danh sách tài khoản từ file `users.json`.
* Sử dụng đường dẫn file tài khoản được khai báo trong `config.py`.

**d. Xây dựng chức năng phân quyền**

Phân chia chức năng theo hai vai trò:

| Chức năng | Admin | User |
|:---|:---:|:---:|
| Xem và tìm kiếm tour | Có | Có |
| Xem lịch trình | Có | Có |
| Thêm, sửa, xóa tour | Có | Không |
| Quản lý lịch trình | Có | Không |
| Đặt tour | Có | Có |
| Xem và hủy phiếu đặt cá nhân | Có | Có |
| Quản lý tất cả phiếu đặt tour | Có | Không |
| Thống kê doanh thu và tỷ lệ lấp đầy | Có | Không |
| Xuất báo cáo | Có | Không |
| Đổi mật khẩu cá nhân | Có | Có |
| Quản lý khách hàng | Có | Không |
| Quản lý dịch vụ bổ sung | Có | Không |
| Tra cứu điểm đến qua API | Có | Có |

* Tài khoản đăng ký mới mặc định có vai trò User, không cho phép người dùng tự cấp quyền Admin.
* Chuẩn bị tài khoản Admin mẫu để kiểm thử.
* Liên kết tài khoản User với mã khách hàng để xác định phiếu đặt tour thuộc về người dùng nào.
* Phối hợp với thành viên phụ trách `tour_manager.py` để thống nhất cách tạo hoặc liên kết thông tin khách hàng khi đăng ký tài khoản.
* Xây dựng và kiểm thử cơ chế kiểm tra quyền và quyền sở hữu phiếu đặt.

* **Nhiệm vụ kiểm thử:**
  * Kiểm thử số điện thoại và email hợp lệ, không hợp lệ.
  * Kiểm thử khách hàng bỏ trống họ tên và dịch vụ có đơn giá âm.
  * Kiểm thử đăng ký thành công, đăng ký trùng tên đăng nhập và đăng nhập sai mật khẩu.
  * Kiểm thử đổi mật khẩu và phân quyền Admin, User theo tiến độ thực tế.
  * Gửi kết quả kiểm thử cho Đỗ Yến Nhi tổng hợp.

* **Nội dung báo cáo phụ trách:**

**Đợt 1 – Viết song song với lập trình**

* **Mục 1.2. Thông tin về đồ án:**
  * Giới thiệu tên đề tài, mục tiêu, phạm vi và đối tượng sử dụng.
  * Liệt kê và mô tả ngắn gọn các chức năng của hệ thống.
  * Xác định chức năng của Admin và User.
  * Xây dựng Use Case Diagram minh họa các chức năng của hệ thống.

* **Mục 2.6. Chức năng quản trị ứng dụng:**
  * Mô tả chức năng đăng ký tài khoản, đăng nhập, đăng xuất và đổi mật khẩu.
  * Trình bày bảng phân quyền Admin và User.
  * Vẽ Flowchart cho các chức năng quản trị đã xây dựng.
  * Mô tả cách kiểm tra thông tin tài khoản và lưu trữ trong file `users.json`.
  * Trình bày theo tiến độ thực tế.

---

#### 3. Đỗ Yến Nhi

* **File phụ trách:** `models/booking.py` (bổ sung).

* **Chi tiết nhiệm vụ lập trình:**

**a. Hoàn thiện lớp LichTrinhNgay**

* Kiểm tra số thứ tự ngày phải là số nguyên dương.
* Kiểm tra tiêu đề hoạt động không được bỏ trống.
* Kiểm tra nội dung hoạt động của từng buổi phải đúng kiểu dữ liệu và không được bỏ trống toàn bộ hoạt động trong ngày.
* Đảm bảo lưu đầy đủ thông tin hoạt động theo từng buổi sáng, chiều và tối dựa trên các thuộc tính đã xây dựng.
* Kiểm tra lại phương thức `to_dict()` để chuyển đầy đủ thông tin lịch trình thành Dictionary.
* Phối hợp với thành viên phụ trách `tour.py` để liên kết các đối tượng `LichTrinhNgay` với tour.

Lớp `LichTrinhNgay` quản lý thông tin của một ngày; lớp `Tour` quản lý danh sách lịch trình nhiều ngày.

**b. Hoàn thiện lớp PhieuDatTour**

* Bổ sung các thuộc tính còn thiếu:
  * `ngay_dat`: ngày khách hàng đặt tour.
  * `tong_tien`: tổng tiền được ghi nhận khi xác nhận đặt tour.
  * `trang_thai`: Chờ xác nhận, Đã xác nhận hoặc Đã hủy.
* Sử dụng các hằng số trạng thái được khai báo trong `config.py`.
* Kiểm tra mã phiếu đặt không được bỏ trống và số lượng vé phải là số nguyên dương.
* Hoàn thiện phương thức `xac_nhan_dat()`: kiểm tra phiếu đang chờ xác nhận và tour còn đủ số chỗ.
* Tính tổng chi phí và gọi phương thức `dat_cho()` của Tour để cập nhật số chỗ đã đặt.
* Ghi nhận tổng tiền và chuyển trạng thái phiếu thành Đã xác nhận nếu đặt tour thành công.
* Nếu đặt tour thất bại thì giữ nguyên số chỗ và trạng thái phiếu.
* Không cho phép xác nhận một phiếu nhiều lần hoặc xác nhận phiếu đã hủy.

Ví dụ: Tour có 20 chỗ, đã đặt 15 chỗ. Khách đăng ký 3 vé thì tour còn 2 chỗ. Nếu đăng ký 6 vé thì thông báo không đủ chỗ.

**c. Bổ sung chức năng hủy đặt tour**

* Viết phương thức `huy_dat()` sử dụng câu lệnh điều kiện để kiểm tra trạng thái phiếu.
* Nếu phiếu đang chờ xác nhận thì chỉ chuyển trạng thái thành Đã hủy, không thay đổi số chỗ.
* Nếu phiếu đã xác nhận thì gọi phương thức `huy_cho()` của Tour để hoàn trả số chỗ và chuyển trạng thái thành Đã hủy.
* Nếu phiếu đã hủy thì thông báo không thể tiếp tục hủy để tránh hoàn trả số chỗ nhiều lần.

Ví dụ: Tour đang còn 2 chỗ, khách hủy phiếu đã đặt 3 vé thì tour phải còn lại 5 chỗ.

**d. Hoàn thiện chức năng tính tổng chi phí**

* Kiểm tra lại phương thức `tinh_tong_tien()` theo công thức:

  `tong_tien = (tour.tinh_gia_ve() * so_ve) + tong_tien_dich_vu`

* Sử dụng vòng lặp để tính tổng đơn giá các dịch vụ mà khách hàng lựa chọn.
* Tổng tiền dịch vụ bằng tổng đơn giá các dịch vụ nhân với số lượng vé.
* Sử dụng phương thức `tinh_gia_ve()` để áp dụng đúng tính đa hình của tour nội địa và tour quốc tế.
* Kiểm tra trường hợp khách hàng không lựa chọn dịch vụ bổ sung.
* Lưu tổng tiền tại thời điểm xác nhận để không bị thay đổi khi giá tour được cập nhật sau đó.
* Cập nhật phương thức `to_dict()` để lưu mã phiếu, mã tour, mã khách hàng, danh sách mã dịch vụ, số lượng vé, ngày đặt, tổng tiền và trạng thái.
* Phối hợp với thành viên phụ trách `tour_manager.py` để thống nhất cách khôi phục phiếu đặt từ JSON.

Ví dụ: Giá tour 2.000.000 đồng/người, dịch vụ bổ sung 300.000 đồng/người và khách đặt 3 vé thì tổng tiền là 6.900.000 đồng.

**e. Phác thảo giao diện**

* Phác thảo bố cục các màn hình đăng nhập, quản lý tour, lịch trình, đặt tour, quản lý phiếu đặt và thống kê.
* Thể hiện vị trí các ô nhập thông tin, nút chức năng và khu vực hiển thị dữ liệu.
* Phối hợp với các thành viên để thống nhất bố cục giao diện.
* Có thể sử dụng Canva, Figma hoặc vẽ trên giấy, không yêu cầu thiết kế quá chi tiết.

* **Nhiệm vụ kiểm thử:**
  * Kiểm thử đặt tour thành công, đặt vượt số chỗ và số lượng vé không hợp lệ.
  * Kiểm thử xác nhận một phiếu hai lần.
  * Kiểm thử hủy phiếu đã xác nhận, phiếu chưa xác nhận và hủy hai lần.
  * Kiểm thử tính tổng tiền khi có hoặc không có dịch vụ.
  * Thu thập và tổng hợp kết quả kiểm thử bước đầu của các thành viên thành bảng tối thiểu 10 trường hợp tiêu biểu.
  * Bảng kiểm thử gồm chức năng, dữ liệu đầu vào, kết quả mong đợi, kết quả thực tế và trạng thái Pass/Fail.
  * Lưu kết quả và minh chứng kiểm thử.

* **Nội dung báo cáo phụ trách:**

**Đợt 1 – Viết song song với lập trình**

* **Mục 2.3.6. Đăng ký đặt tour:**
  * Mô tả quá trình nhập thông tin khách hàng, lựa chọn tour, số lượng vé và dịch vụ bổ sung.
  * Trình bày cách kiểm tra số chỗ còn trống, lập phiếu và xác nhận đặt tour.
  * Vẽ Flowchart chức năng đặt tour.

* **Mục 2.3.7. Hủy đặt tour:**
  * Mô tả quá trình kiểm tra trạng thái phiếu, hủy phiếu và hoàn trả số chỗ.
  * Vẽ Flowchart chức năng hủy đặt tour.

* **Mục 2.3.8. Tính tổng chi phí đặt tour:**
  * Trình bày công thức tính tiền vé và chi phí dịch vụ.
  * Đưa ra ví dụ minh họa kết quả tính tiền.
  * Vẽ Flowchart chức năng tính tổng chi phí.

---

#### 4. Nguyễn Hữu Phương Uyên

* **File phụ trách:**
  * `controllers/tour_manager.py` (bổ sung).
  * `utils/file_helper.py` (bổ sung).
  * `config.py` (tạo mới).

* **Chi tiết nhiệm vụ lập trình:**

**a. Xây dựng file cấu hình config.py**

* Tạo file `config.py` để khai báo các hằng số sử dụng chung:
  * `DATA_FILE`: đường dẫn đến `data/data.json`.
  * `USERS_FILE`: đường dẫn đến `data/users.json`.
  * `ROLE_ADMIN`: vai trò Admin.
  * `ROLE_USER`: vai trò User.
  * `STATUS_PENDING`: trạng thái Chờ xác nhận.
  * `STATUS_CONFIRMED`: trạng thái Đã xác nhận.
  * `STATUS_CANCELLED`: trạng thái Đã hủy.
* Sử dụng đường dẫn dựa trên thư mục project để chương trình có thể chạy trên các máy tính khác nhau.
* Thống nhất các hằng số với các thành viên để sử dụng chung thông qua câu lệnh `import`.
* Hoàn thành và chia sẻ file cấu hình trước khi các thành viên sử dụng các hằng số trong module của mình.

**b. Hoàn thiện chức năng CRUD và tìm kiếm tour**

* Kiểm tra lại phương thức `them_tour()` để đảm bảo không thêm tour trùng mã.
* Hoàn thiện phương thức `cap_nhat_tour()`: kiểm tra thông tin cập nhật hợp lệ, không cho phép giảm số chỗ tối đa xuống thấp hơn số chỗ đã đặt hoặc giảm số ngày không phù hợp với lịch trình hiện tại.
* Hoàn thiện phương thức `xoa_tour()`: kiểm tra tour có tồn tại hay không; không cho phép xóa tour đang có phiếu đặt liên quan để tránh mất liên kết dữ liệu.
* Bổ sung tiêu chí ngày khởi hành vào phương thức `tim_kiem()` đã xây dựng trong giai đoạn 1.
* Sử dụng vòng lặp và câu lệnh điều kiện để tìm kiếm theo điểm đến, ngày khởi hành và mức giá.
* Sử dụng phương thức `tinh_gia_ve()` để tìm kiếm theo giá vé thực tế thay vì giá vé cơ bản.
* Cho phép tìm kiếm theo từng tiêu chí hoặc kết hợp nhiều tiêu chí.

Ví dụ: Tìm các tour đi Đà Lạt có giá không vượt quá 3.000.000 đồng và khởi hành vào ngày được nhập.

**c. Bổ sung chức năng quản lý khách hàng, dịch vụ và phiếu đặt tour**

* Bổ sung hoặc hoàn thiện thuộc tính `ds_phieu_dat` có kiểu List trong lớp `QuanLyTour` để quản lý các đối tượng `PhieuDatTour`.
* Bổ sung các danh sách `ds_khach_hang`, `ds_dich_vu` và `ds_diem_den` để quản lý dữ liệu sử dụng khi lập phiếu đặt và xây dựng tour.
* Viết các phương thức thêm và tìm khách hàng, dịch vụ theo mã; kiểm tra mã không bị trùng lặp.
* Viết phương thức `them_phieu_dat(phieu)`: kiểm tra mã phiếu không bị trùng, thông tin tour, khách hàng và dịch vụ hợp lệ trước khi thêm phiếu vào danh sách.
* Viết phương thức `lay_ds_phieu_dat()`: trả về danh sách phiếu đặt tour.
* Viết phương thức `tim_phieu_dat(ma_phieu)`: sử dụng vòng lặp để tìm phiếu theo mã.
* Viết phương thức `tim_phieu_theo_khach(ma_khach)`: tìm danh sách phiếu đặt thuộc về một khách hàng.
* Viết phương thức `xac_nhan_phieu_dat(ma_phieu)`: tìm phiếu theo mã và gọi phương thức `xac_nhan_dat()` trong `booking.py`.
* Viết phương thức `huy_phieu_dat(ma_phieu)`: tìm phiếu theo mã và gọi phương thức `huy_dat()` trong `booking.py`.
* Lưu dữ liệu sau khi thêm, xác nhận hoặc hủy phiếu đặt thành công.

Không viết lại nghiệp vụ đặt chỗ, hủy chỗ và tính tiền đã được xây dựng trong `booking.py`.

**d. Hoàn thiện chức năng thống kê**

* Chỉnh sửa phương thức `thong_ke_doanh_thu()`: sử dụng vòng lặp để cộng tổng tiền của các phiếu đặt có trạng thái Đã xác nhận, bao gồm cả chi phí dịch vụ.
* Không tính các phiếu Chờ xác nhận hoặc Đã hủy vào doanh thu.
* Kiểm tra lại phương thức `thong_ke_ty_le_lap_day()` theo công thức:

  `ty_le_lap_day = (tong_so_cho_da_dat / tong_so_cho_toi_da) * 100`

* Xử lý trường hợp số chỗ tối đa không hợp lệ để tránh lỗi chia cho 0.
* Đảm bảo doanh thu và tỷ lệ lấp đầy thay đổi chính xác sau khi xác nhận hoặc hủy đặt tour.

Ví dụ: Tour có 20 chỗ, đã đặt 15 chỗ thì tỷ lệ lấp đầy là 75%. Sau khi hủy phiếu gồm 3 vé, tỷ lệ lấp đầy còn 60%.

**e. Hoàn thiện chức năng lưu trữ dữ liệu JSON**

* Tạo thư mục `data/` để lưu hai file JSON:

| File | Nội dung lưu trữ |
|:---|:---|
| `data.json` | Tour, lịch trình, khách hàng, dịch vụ, phiếu đặt tour và điểm đến từ Crawl/API |
| `users.json` | Danh sách tài khoản và vai trò người dùng |

* Thống nhất cấu trúc `data.json` sử dụng Dictionary chứa các List:

      {
          "tours": [],
          "customers": [],
          "services": [],
          "bookings": [],
          "destinations": []
      }

* Lịch trình từng ngày được lưu bên trong thông tin của mỗi tour, không tạo file JSON riêng cho lịch trình.
* Hoàn thiện phương thức `luu_du_lieu()`: sử dụng `to_dict()` của các lớp để chuyển đối tượng thành Dictionary và lưu toàn bộ dữ liệu nghiệp vụ vào `data.json`.
* Hoàn thiện phương thức `tai_du_lieu()`: đọc JSON và sử dụng vòng lặp để khôi phục các đối tượng tour, khách hàng, dịch vụ, lịch trình và phiếu đặt.
* Khôi phục đúng đối tượng `TourNoiDia` hoặc `TourQuocTe` dựa trên loại tour đã lưu.
* Khi khôi phục phiếu đặt, tìm đúng đối tượng tour, khách hàng và dịch vụ tương ứng theo mã đã lưu.
* Không gọi lại phương thức xác nhận đặt tour khi đọc JSON để tránh cộng số chỗ đã đặt nhiều lần.
* Phối hợp với thành viên phụ trách `user.py` để lưu và đọc dữ liệu tài khoản riêng trong `users.json`.
* Phối hợp với thành viên phụ trách `api_helper.py` để lưu dữ liệu điểm đến vào danh sách `destinations` mà không làm mất các dữ liệu khác.

**f. Hoàn thiện module xử lý file**

* Tái sử dụng các hàm `luu_json()` và `doc_json()` đã xây dựng ở giai đoạn 1.
* Sử dụng `with open(...)`, `json.dump()` và `json.load()` để đọc và ghi dữ liệu.
* Sử dụng `try...except` để xử lý các trường hợp file không tồn tại, file rỗng, JSON sai định dạng, không có quyền truy cập hoặc ghi file thất bại.
* Bổ sung cách sao lưu dữ liệu đơn giản trước khi ghi đè file.
* Không tự động ghi đè file dữ liệu bị lỗi bằng danh sách rỗng.
* Không thông báo lưu thành công nếu ghi file thất bại; có cách khôi phục dữ liệu trước khi thay đổi nếu lưu không thành công.
* Kiểm tra lại hàm `xuat_bao_cao_csv()` để đảm bảo xuất đúng dữ liệu thống kê và hiển thị được tiếng Việt.
* Cập nhật hàm `xuat_lich_trinh_text()` để xuất thông tin tour và nội dung lịch trình theo từng ngày.

**g. Liên kết các module nghiệp vụ và kiểm thử bước đầu**

* Liên kết các lớp Tour, KhachHang, DichVu, LichTrinhNgay và PhieuDatTour thông qua lớp QuanLyTour.
* Sử dụng các hàm xử lý file trong `file_helper.py` để đọc, ghi, sao lưu và xuất dữ liệu.
* Xây dựng các kịch bản kiểm thử trong `tour_manager.py` và `file_helper.py` thông qua `if __name__ == "__main__":`.
* Chuẩn bị dữ liệu và file kiểm thử riêng, không làm ảnh hưởng đến dữ liệu chính thức.
* Kiểm tra sự phối hợp giữa các module trong quá trình quản lý tour, khách hàng, dịch vụ, lịch trình, phiếu đặt, thống kê và lưu trữ dữ liệu.
* Phối hợp với các thành viên xử lý lỗi khi liên kết các module nghiệp vụ.
* Cập nhật hướng dẫn chạy kiểm thử trong `README.md`.

* **Nhiệm vụ kiểm thử:**
  * Kiểm thử thêm tour trùng mã, cập nhật tour không hợp lệ và xóa tour đang có phiếu đặt.
  * Kiểm thử tìm kiếm theo điểm đến, mức giá và ngày khởi hành.
  * Kiểm thử quản lý khách hàng, dịch vụ và phiếu đặt.
  * Kiểm thử thống kê doanh thu và tỷ lệ lấp đầy.
  * Kiểm thử đọc, ghi JSON và xuất file CSV, TXT.
  * Kiểm thử khả năng sao lưu và bảo toàn dữ liệu khi xảy ra lỗi.
  * Kiểm thử lưu và khôi phục dữ liệu JSON bằng cách khởi tạo lại đối tượng quản lý.
  * Phối hợp với các thành viên kiểm thử tích hợp bước đầu giữa các module nghiệp vụ.
  * Gửi kết quả kiểm thử cho Đỗ Yến Nhi tổng hợp.

* **Nội dung báo cáo phụ trách:**

**Đợt 1 – Viết song song với lập trình**

* **Mục 1.1. Nhóm thực hiện:**
  * Mục 1.1.1. Thông tin thành viên nhóm: lập bảng họ tên, mã sinh viên và lớp của từng thành viên.
  * Mục 1.1.2. Phân công nhiệm vụ: trình bày bảng tổng hợp nhiệm vụ lập trình, nội dung báo cáo và tỷ lệ đóng góp dự kiến của từng thành viên.

* **Mục 2.3.1. Thêm mới tour:**
  * Mô tả quá trình nhập thông tin tour, kiểm tra dữ liệu, kiểm tra trùng mã, thêm vào danh sách và lưu JSON.
  * Vẽ Flowchart chức năng thêm mới tour.

* **Mục 2.3.2. Cập nhật tour:**
  * Mô tả quá trình tìm tour theo mã, kiểm tra thông tin cập nhật và lưu dữ liệu mới.
  * Vẽ Flowchart chức năng cập nhật tour.

* **Mục 2.3.3. Xóa tour:**
  * Mô tả quá trình tìm tour, kiểm tra phiếu đặt liên quan và xóa dữ liệu.
  * Vẽ Flowchart chức năng xóa tour.

* **Mục 2.3.4. Tìm kiếm tour:**
  * Mô tả các tiêu chí tìm kiếm theo điểm đến, ngày khởi hành và mức giá.
  * Trình bày cách duyệt danh sách và trả về kết quả phù hợp.
  * Vẽ Flowchart chức năng tìm kiếm tour.

* **Mục 2.3.9. Thống kê doanh thu và tỷ lệ lấp đầy:**
  * Trình bày công thức thống kê doanh thu và tỷ lệ lấp đầy.
  * Giải thích cách sử dụng dữ liệu tour và phiếu đặt để thống kê.
  * Vẽ Flowchart cho các chức năng thống kê.

* **Mục 2.3.10. Xuất báo cáo và lịch trình:**
  * Mô tả chức năng xuất báo cáo thống kê CSV và lịch trình TXT.
  * Trình bày nội dung dữ liệu được xuất.
  * Vẽ Flowchart cho các chức năng xuất file.

* **Mục 2.4. Cách thức lưu trữ, quản lý dữ liệu:**
  * Mục 2.4.1. Cấu trúc dữ liệu JSON: mô tả cấu trúc `data.json`, `users.json`, vị trí lưu trữ và ý nghĩa các trường dữ liệu.
  * Mục 2.4.2. Hàm đọc ghi dữ liệu: mô tả các hàm `luu_json()`, `doc_json()`, `luu_du_lieu()` và `tai_du_lieu()`.
  * Giải thích cách chuyển đổi đối tượng thành Dictionary và khôi phục đối tượng từ JSON.
  * Trình bày cách xử lý lỗi khi đọc và ghi file.
  * Phối hợp với thành viên phụ trách tài khoản để mô tả chính xác cấu trúc `users.json`.







