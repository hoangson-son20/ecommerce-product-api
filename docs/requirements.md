
# Project Requirements — E-commerce Product API

## 1. Project Overview

### 1.1 Purpose

Xây dựng REST API quản lý danh mục sản phẩm, sản phẩm và người bán
cho một hệ thống thương mại điện tử.

Project tập trung vào các kiến thức Backend:
- HTTP và REST API.
- FastAPI và Pydantic.
- PostgreSQL và SQLAlchemy ORM.
- Validation và xử lý lỗi.
- Database constraints và transaction.
- Automated testing.

### 1.2 Users

- API Client: ứng dụng hoặc công cụ gửi HTTP request đến API.
- Nhân viên/quản lý: người vận hành hệ thống thông qua client.

Phiên bản đầu tiên chưa triển khai authentication và authorization.
Các endpoint chưa có cơ chế giới hạn quyền truy cập theo vai trò.

### 1.3 Main Data

Hệ thống quản lý ba entity chính:

- Product: thông tin sản phẩm, giá, tồn kho và trạng thái.
- Category: danh mục sản phẩm.
- Seller: thông tin người bán.

Mỗi Product thuộc về một Category và một Seller.

## 2. Scope

### 2.1 In Scope

- CRUD Product, Category và Seller.
- Tìm kiếm theo ID hoặc tên trên các tài nguyên phù hợp.
- Lọc dữ liệu theo các thuộc tính được hỗ trợ.
- Sắp xếp kết quả.
- Phân trang danh sách.
- Validation dữ liệu đầu vào.
- Xử lý lỗi HTTP nhất quán.
- Kết nối PostgreSQL bằng SQLAlchemy.
- Kiểm soát transaction và tính toàn vẹn dữ liệu.
- Automated tests cho API và database.
- Cấu hình qua biến môi trường.
- README hướng dẫn cài đặt và chạy project.

### 2.2 Out of Scope

- Authentication và authorization.
- Giỏ hàng và đặt hàng.
- Thanh toán.
- Đánh giá, bình luận và feedback.
- Frontend.
- Microservices.
- Triển khai production trên cloud.

## 3. Functional Requirements

### 3.1 Product

- FR-001: Client có thể lấy danh sách sản phẩm.
- FR-002: Client có thể lấy chi tiết một sản phẩm theo ID.
- FR-003: Client có thể tạo sản phẩm mới.
- FR-004: Client có thể cập nhật thông tin sản phẩm.
- FR-005: Client có thể xóa sản phẩm.
- FR-006: Client có thể tìm kiếm sản phẩm theo ID chính xác hoặc tên.
- FR-007: Client có thể lọc sản phẩm theo Category, Seller, giá và trạng thái.
- FR-008: Client có thể sắp xếp sản phẩm theo tên hoặc giá.
- FR-009: Client có thể phân trang danh sách sản phẩm.
- FR-010: Client có thể cập nhật số lượng tồn kho thông qua thao tác cập nhật Product.
- FR-011: Client có thể cập nhật trạng thái hoạt động của sản phẩm.

### 3.2 Category

- FR-012: Client có thể lấy danh sách Category.
- FR-013: Client có thể lấy chi tiết một Category theo ID.
- FR-014: Client có thể xem danh sách Product thuộc một Category.
- FR-015: Client có thể tạo Category mới.
- FR-016: Client có thể cập nhật Category.
- FR-017: Client có thể xóa Category nếu không còn Product tham chiếu.
- FR-018: Client có thể tìm kiếm Category theo ID hoặc tên.
- FR-019: Client có thể lọc, sắp xếp và phân trang danh sách Category.

### 3.3 Seller

- FR-020: Client có thể lấy danh sách Seller.
- FR-021: Client có thể lấy chi tiết một Seller theo ID.
- FR-022: Client có thể xem danh sách Product thuộc một Seller.
- FR-023: Client có thể tạo Seller mới.
- FR-024: Client có thể cập nhật Seller.
- FR-025: Client có thể xóa Seller nếu không còn Product tham chiếu.
- FR-026: Client có thể tìm kiếm Seller theo ID hoặc tên.
- FR-027: Client có thể lọc, sắp xếp và phân trang danh sách Seller.

### 3.4 Search, Filtering, Sorting, Pagination

- FR-028: Tìm kiếm theo ID sử dụng giá trị ID chính xác.
- FR-029: Tìm kiếm theo tên hỗ trợ chuỗi con và không phân biệt
  chữ hoa/chữ thường.
- FR-030: Product hỗ trợ lọc theo category_id, seller_id,
  min_price, max_price và is_active.
- FR-031: Product hỗ trợ sắp xếp theo name hoặc price.
- FR-032: Category và Seller hỗ trợ sắp xếp theo name.
- FR-033: Các bộ lọc có thể được kết hợp trong cùng một request.
- FR-034: Danh sách hỗ trợ page và page_size.
- FR-035: Khi không có kết quả, API trả về HTTP 200 với danh sách rỗng.
- FR-036: API từ chối các tham số phân trang, lọc hoặc sắp xếp
  không hợp lệ theo quy ước của API.

## 4. Business Rules

### 4.1 Product

- BR-001: Tên Product không được rỗng sau khi loại bỏ khoảng trắng
  ở đầu và cuối.
- BR-002: Tên Product hỗ trợ chữ cái tiếng Việt có dấu, chữ cái
  tiếng Anh, số, khoảng trắng và một số dấu câu thông dụng.
- BR-003: Giá Product phải lớn hơn 0.
- BR-004: Giá tiền sử dụng kiểu dữ liệu số thập phân chính xác,
  không sử dụng floating-point để lưu giá trị tiền tệ.
- BR-005: Số lượng tồn kho phải là số nguyên không âm.
- BR-006: Product phải tham chiếu đến Category và Seller tồn tại.
- BR-007: Product có is_active = false được xem là không hoạt động.
- BR-008: Danh sách Product mặc định chỉ hiển thị sản phẩm đang hoạt động.
  Client có thể truyền is_active để lọc theo trạng thái.

### 4.2 Category

- BR-009: Tên Category không được rỗng sau khi loại bỏ khoảng trắng
  ở đầu và cuối.
- BR-010: Không cho phép xóa Category khi còn Product tham chiếu đến nó.
- BR-011: Tên Category hỗ trợ chữ cái tiếng Việt có dấu, chữ cái
  tiếng Anh, số, khoảng trắng và một số dấu câu thông dụng.

### 4.3 Seller

- BR-012: Tên Seller không được rỗng sau khi loại bỏ khoảng trắng
  ở đầu và cuối.
- BR-013: Email Seller phải có định dạng hợp lệ.
- BR-014: Email Seller phải duy nhất; so sánh email không phân biệt
  chữ hoa/chữ thường.
- BR-015: Không cho phép xóa Seller khi còn Product tham chiếu đến nó.

### 4.4 API Query Rules

- BR-016: page bắt đầu từ 1.
- BR-017: page_size mặc định là 20 và tối đa là 100.
- BR-018: page và page_size phải là số nguyên dương.
- BR-019: min_price không được lớn hơn max_price.
- BR-020: Chỉ cho phép các trường sắp xếp đã được API công bố.
- BR-021: Chiều sắp xếp chỉ nhận asc hoặc desc.
- BR-022: Khi client không truyền tham số sắp xếp, API sử dụng
  thứ tự mặc định ổn định.
- BR-023: Dữ liệu không hợp lệ không được ghi vào database.

## 5. Non-functional Requirements

### 5.1 Testing

- NFR-001: Có thể chạy toàn bộ automated tests bằng một lệnh.
- NFR-002: Tests bao gồm trường hợp thành công, dữ liệu không hợp lệ,
  tài nguyên không tồn tại và vi phạm ràng buộc dữ liệu.
- NFR-003: Tests không phụ thuộc vào dữ liệu được tạo thủ công
  từ lần chạy trước.

### 5.2 Configuration and Security

- NFR-004: Database connection string được cấu hình qua biến môi trường.
- NFR-005: File chứa secret không được commit lên Git.
- NFR-006: Cung cấp .env.example không chứa secret thực.
- NFR-007: Database application user chỉ có các quyền cần thiết
  cho ứng dụng trong môi trường phát triển.

### 5.3 Data Integrity

- NFR-008: Database sử dụng primary key, foreign key và các constraint
  phù hợp để bảo vệ tính toàn vẹn dữ liệu.
- NFR-009: Các thao tác ghi dữ liệu xử lý commit và rollback phù hợp.
- NFR-010: Lỗi database không được làm lộ thông tin nhạy cảm
  trong HTTP response.

### 5.4 Performance and Maintainability

- NFR-011: Endpoint danh sách phải hỗ trợ pagination.
- NFR-012: Giới hạn page_size để tránh trả về lượng dữ liệu quá lớn.
- NFR-013: Routing, validation, business logic và database access
  được tổ chức thành các phần có trách nhiệm rõ ràng.
- NFR-014: Không truy vấn toàn bộ bảng chỉ để lọc và phân trang
  khi database có thể thực hiện trực tiếp.
- NFR-015: Các index bổ sung phải có lý do dựa trên truy vấn
  hoặc nhu cầu tra cứu cụ thể.

### 5.5 Documentation

- NFR-016: README hướng dẫn cài đặt môi trường, cấu hình database,
  chạy ứng dụng và chạy tests.
- NFR-017: API contract mô tả endpoint, request, response,
  status code và các trường hợp lỗi chính.

## 6. Assumptions and Open Questions

- Đây là project học tập, chưa phải hệ thống thương mại điện tử
  triển khai cho người dùng thật.
- Phiên bản đầu tiên chưa có authentication hoặc phân quyền.
- Một Product chỉ thuộc về một Category và một Seller.
- Product, Category và Seller được lưu trong PostgreSQL.
- Việc xóa Product là xóa bản ghi; chưa triển khai soft delete.
- Việc xóa Category hoặc Seller bị từ chối khi vẫn còn Product tham chiếu.
- Chưa đặt mục tiêu tải đồng thời hoặc SLA cụ thể.
- Cơ chế migration database, chẳng hạn Alembic, sẽ được quyết định
  khi triển khai phần database.
