
# API Contract — E-commerce Product API

## 1. General Conventions

### 1.1. Base Path
- API prefix: `/api/v1`
- Data format: JSON
- Field naming: snake_case

### 1.2. HTTP Status Codes

| Status Code | Meaning | When to use |
|---|---|---|
| 200 | OK | Lấy/Cập nhật thành công có body |
| 201 | Created | Tạo thành công |
| 204 | No Content | Xóa thành công không có body |
| 404 | Not Found | Không tìm thấy tài nguyên |
| 409 | Conflict | Xung đột dữ liệu |
| 422 | Validation Error | Dữ liệu đầu vào không hợp lệ |
| 500 | Internal Server Error | Lỗi không dự kiến |

### 1.3. Error Response
Tất cả các lỗi API đều sử dụng cấu trúc JSON sau:
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "page_size",
        "message": "Must be between 1 and 100"
      }
    ]
  }
}

Các trường: 
- error.code: Mã định danh lỗi có thể đọc được bằng máy. 
- error.message: Tóm tắt lỗi có thể đọc được bằng người. 
- error.details: Thông tin lỗi bổ sung. Sử dụng mảng rỗng khi không có thông tin chi tiết ở cấp trường.


## 2. Product API

### 2.1. List Products

**Method:** GET

**Path:** `/api/v1/products`

**Purpose:** Truy xuất danh sách sản phẩm được phân trang với các tùy chọn tìm kiếm, lọc và sắp xếp

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| page | integer | No | 1 | Trang mà client yêu cầu, page >= 1 |
| page_size | integer | No | 20 | Số sản phẩm hiển thị ở trang. Mặc định 20, tối thiểu 1, tối đa 100 |
| search | string | No | None | Sản phẩm tìm theo name, chứa từ khóa khớp một phần với tên, không phân biệt hoa/thường |
| category_id | integer | No | None | Lọc sản phẩm theo ID danh mục |
| seller_id | integer | No | None | Lọc sản phẩm theo ID người bán |
| min_price | decimal | No | None | Giá sản phẩm tối thiểu, >= 0, không được lớn hơn max_price |
| max_price | decimal | No | None | Giá sản phẩm tối đa, >= 0, Không được nhỏ hơn min_price |
| is_active | boolean | No | true | Lọc theo trạng thái hoạt động |
| sort_by | string | No | created_at | Các giá trị được cho phép: tên, giá, thời gian tạo |
| sort_order | string | No | desc | Các giá trị được cho phép: asc, desc (asc tăng dần, desc giảm dần; mặc định desc) |

#### Success Response
- Status: 200
- Response body
{
  "items": [
    {
      "id": 1,
      "name": "Mechanical Keyboard",
      "description": "Compact mechanical keyboard",
      "price": "250.00",
      "stock_quantity": 15,
      "category_id": 2,
      "seller_id": 3,
      "is_active": true,
      "created_at": "2026-10-21T10:00:00Z",
      "updated_at": "2026-10-21T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}

#### Error Cases
page nhỏ hơn 1 hoặc không phải số nguyên | 422 VALIDATION_ERROR                             

page_size ngoài phạm vi 1-100 | 422 VALIDATION_ERROR                                           

search có kiểu không hợp lệ | 422 VALIDATION_ERROR                                      

category_id or seller_id không phải số nguyên dương | 422 VALIDATION_ERROR
                        
min_price or max_price không hợp lệ hoặc số âm | 422 VALIDATION_ERROR
                           
min_price > max_price | 422 VALIDATION_ERROR                                        

sort_by không phải giá trị cho phép | 422 VALIDATION_ERROR

sort_order không phải asc/desc | 422 VALIDATION_ERROR

### 2.2. Get Product by ID

**Method:** GET

**Path:** `/api/v1/products/{product_id}`

**Purpose:** Truy xuất một sản phẩm bởi ID.

#### Path Parameters
product_id | integer | Bắt buộc >= 1

#### Success Response
Status: 200 OK
{
  "id": 1,
  "name": "Mechanical Keyboard",
  "description": "Compact mechanical keyboard",
  "price": "250.00",
  "stock_quantity": 15,
  "category_id": 2,
  "seller_id": 3,
  "is_active": true,
  "created_at": "2026-10-21T10:00:00Z",
  "updated_at": "2026-10-21T10:00:00Z"
}

#### Error Cases
product_id không hợp lệ | 422 VALIDATION_ERROR                                    

Không có sản phẩm tồn tại | 404 NOT_FOUND

### 2.3. Create Product

**Method:** POST

**Path:** `/api/v1/products`

**Purpose:** Tạo ra sản phẩm mới.

#### Request Body
| Parameter | Type | Required | Description |
|---|---|---|---|---|
| name | string | Yes | Không được để trống sau khi loại bỏ khoảng trắng đầu cuối |
| description | string or null | No | Mô tả tùy chọn hoặc mặc định là null |
| price | decimal | Yes | Bắt buộc > 0 |
| stock_quantity | integer | Yes | Bắt buộc >= 0 |
| category_id | integer | Yes | Phải tham chiếu đến một Danh mục hiện có |
| seller_id | integer | Yes | Phải tham chiếu đến một Người bán hiện có |
| is_active | boolean | No | Mặc định là True |

#### Success Response
Status: 201 Created
{
  "name": "Mechanical Keyboard",
  "description": "Compact mechanical keyboard",
  "price": "250.00",
  "stock_quantity": 15,
  "category_id": 2,
  "seller_id": 3,
  "is_active": true
}

#### Error Cases
name trống sau khi loại bỏ khoảng trắng đầu cuối | 422 VALIDATION_ERROR

price không hợp lệ hoặc <= 0 | 422 VALIDATION_ERROR                             

stock_quantity không hợp lệ hoặc số âm | 422 VALIDATION_ERROR                                           

category_id or seller_id không hợp lệ | 422 VALIDATION_ERROR                                      

Danh mục được tham chiều không tồn tại | 404 CATEGORY_NOT_FOUND
                        
Người bán được tham chiều không tồn tại | 404 SELLER_NOT_FOUND
                                                            

### 2.4. Update Product

**Method:** PATCH

**Path:** `/api/v1/products/{product_id}`

**Purpose:** Cập nhật một phần sản phẩm

#### Path Parameters
product_id | integer | Bắt buộc >= 1

#### Request Body

| name | string | Không được để trống sau khi loại bỏ khoảng trắng đầu cuối |
| description | string or null | Mô tả tùy chọn hoặc mặc định là null |
| price | decimal | Bắt buộc > 0 |
| stock_quantity | integer | Bắt buộc >= 0 |
| category_id | integer | Phải tham chiếu đến một Danh mục hiện có |
| seller_id | integer | Phải tham chiếu đến một Người bán hiện có |
| is_active | boolean | Mặc định là True |

#### Success Response
Status: 200 OK
{
  "price": "275.00",
  "stock_quantity": 12
}

Quy tắc cập nhật: 
- Các trường bị bỏ qua sẽ không thay đổi. 
- Giá trị null chỉ được chấp nhận đối với các trường cho phép null như description. 
- id, created_at và updated_at không thể được cập nhật bởi máy khách. 
- Máy chủ cập nhật updated_at khi Sản phẩm được sửa đổi thành công. 
- Các trường không xác định sẽ bị từ chối.

#### Error Cases
product_id không hợp lệ | 422 VALIDATION_ERROR                                    

Nội dung yêu cầu trống hoặc không chứa các trường cho phép | 422 VALIDATION_ERROR

Sản phẩm không tồn tại | 404 NOT_FOUND                                          
                                     
Danh mục được tham chiều không tồn tại | 404 CATEGORY_NOT_FOUND
                        
Người bán được tham chiều không tồn tại | 404 SELLER_NOT_FOUND

### 2.5. Delete Product

**Method:** DELETE

**Path:** `/api/v1/products/{product_id}`

**Purpose:** Xóa sản phẩm hiện có

#### Path Parameters
product_id | integer | Bắt buộc >= 1

#### Success Response
Status: 204 No Content


#### Error Cases
product_id không hợp lệ | 422 VALIDATION_ERROR 

Sản phẩm không tồn tại | 404 NOT_FOUND 

---

## 3. Category API

### 3.1. List Categories

**Method:** GET

**Path:** `/api/v1/categories`

**Purpose:** Lấy danh sách Category có phân trang.

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `page` | integer | No | 1 | Trang yêu cầu, `>= 1` |
| `page_size` | integer | No | 20 | Số Category mỗi trang, từ 1 đến 100 |

#### Success Response

**Status:** 200 OK

```json
{
  "items": [
    {
      "id": 2,
      "name": "Accessories",
      "description": "Computer and desk accessories",
      "created_at": "2026-10-21T10:00:00Z",
      "updated_at": "2026-10-21T10:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_items": 1,
    "total_pages": 1
  }
}
```

#### Error Cases

- `page < 1`, `page_size` ngoài phạm vi 1–100 hoặc sai kiểu: `422 VALIDATION_ERROR`.

### 3.2. Get Category by ID

**Method:** GET

**Path:** `/api/v1/categories/{category_id}`

**Purpose:** Lấy một Category theo ID.

#### Path Parameters

- `category_id`: integer, bắt buộc `>= 1`.

#### Success Response

**Status:** 200 OK

```json
{
  "id": 2,
  "name": "Accessories",
  "description": "Computer and desk accessories",
  "created_at": "2026-10-21T10:00:00Z",
  "updated_at": "2026-10-21T10:00:00Z"
}
```

#### Error Cases

- `category_id` không hợp lệ: `422 VALIDATION_ERROR`.
- Category không tồn tại: `404 CATEGORY_NOT_FOUND`.

### 3.3. List Products by Category

**Method:** GET

**Path:** `/api/v1/categories/{category_id}/products`

**Purpose:** Lấy danh sách Product thuộc một Category, có phân trang.

#### Path Parameters

- `category_id`: integer, bắt buộc `>= 1`.

#### Query Parameters

| Parameter | Type | Required | Default | Description |
|---|---|---|---|---|
| `page` | integer | No | 1 | Trang yêu cầu, `>= 1` |
| `page_size` | integer | No | 20 | Số Product mỗi trang, từ 1 đến 100 |
| `is_active` | boolean | No | true | Mặc định chỉ lấy Product đang hoạt động; truyền false để chỉ lấy Product không hoạt động |

#### Success Response

**Status:** 200 OK

Response có cùng cấu trúc với `GET /api/v1/products`, gồm `items` và `pagination`. Mỗi phần tử trong `items` là một Product đầy đủ.

Chỉ trả về Product có `category_id` bằng `category_id` trên path.

#### Error Cases

- `category_id` không hợp lệ: `422 VALIDATION_ERROR`.
- Category không tồn tại: `404 CATEGORY_NOT_FOUND`.
- Query pagination hoặc `is_active` không hợp lệ: `422 VALIDATION_ERROR`.

### 3.4. Create Category

**Method:** POST

**Path:** `/api/v1/categories`

**Purpose:** Tạo Category mới.

#### Request Body

| Field | Type | Required | Rules |
|---|---|---|---|
| `name` | string | Yes | Loại bỏ khoảng trắng đầu/cuối; không được rỗng sau khi trim |
| `description` | string or null | No | Mặc định null |

Client không được gửi `id`, `created_at` hoặc `updated_at`.

#### Success Response

**Status:** 201 Created

Response body là toàn bộ Category vừa tạo.

```json
{
  "id": 2,
  "name": "Accessories",
  "description": "Computer and desk accessories",
  "created_at": "2026-10-21T10:00:00Z",
  "updated_at": "2026-10-21T10:00:00Z"
}
```

#### Error Cases

- `name` rỗng sau khi trim hoặc field sai kiểu: `422 VALIDATION_ERROR`.
- Client gửi field không được phép: `422 VALIDATION_ERROR`.

### 3.5. Update Category

**Method:** PATCH

**Path:** `/api/v1/categories/{category_id}`

**Purpose:** Cập nhật một phần Category.

#### Path Parameters

- `category_id`: integer, bắt buộc `>= 1`.

#### Request Body

| Field | Type | Rules |
|---|---|---|
| `name` | string | Nếu có mặt, sau trim không được rỗng; không chấp nhận null |
| `description` | string or null | Cho phép null để xóa mô tả |

Body phải có ít nhất một trường được phép cập nhật. Client không được cập nhật `id`, `created_at` hoặc `updated_at`.

#### Success Response

**Status:** 200 OK

Response body là toàn bộ Category sau cập nhật.

```json
{
  "id": 2,
  "name": "Computer Accessories",
  "description": "Computer and desk accessories",
  "created_at": "2026-10-21T10:00:00Z",
  "updated_at": "2026-10-21T10:15:00Z"
}
```

#### Error Cases

- `category_id` không hợp lệ: `422 VALIDATION_ERROR`.
- Body rỗng hoặc field không hợp lệ: `422 VALIDATION_ERROR`.
- Category không tồn tại: `404 CATEGORY_NOT_FOUND`.

### 3.6. Delete Category

**Method:** DELETE

**Path:** `/api/v1/categories/{category_id}`

**Purpose:** Xóa Category.

#### Path Parameters

- `category_id`: integer, bắt buộc `>= 1`.

#### Success Response

**Status:** 204 No Content

Không có response body.

#### Error Cases

- `category_id` không hợp lệ: `422 VALIDATION_ERROR`.
- Category không tồn tại: `404 CATEGORY_NOT_FOUND`.
- Có Product đang tham chiếu Category: `409 CATEGORY_IN_USE`.

**Business Rule:** Không được xóa Category đang được Product tham chiếu. Không tự động xóa các Product liên quan.
