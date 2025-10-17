import os

def count_images_in_folder_recursive(folder_path):
    """
    Đếm số lượng file ảnh (jpg, png, v.v.) trong thư mục và TẤT CẢ thư mục con.
    """
    # Các phần mở rộng ảnh phổ biến
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp')

    image_count = 0

    if not os.path.isdir(folder_path):
        print(f"LỖI: Thư mục '{folder_path}' không tồn tại.")
        return 0

    # Sử dụng os.walk để duyệt đệ quy qua tất cả thư mục con
    for root, dirs, files in os.walk(folder_path):
        for filename in files:
            if filename.lower().endswith(image_extensions):
                image_count += 1

    return image_count

# --- CẤU HÌNH ĐƯỜNG DẪN TƯƠNG ĐỐI ---

# Lấy đường dẫn của file Python hiện tại
CURRENT_FILE_PATH = os.path.abspath(__file__)
# Lùi 2 cấp để về thư mục gốc Capstone-project-VKU
BASE_PROJECT_DIR = os.path.dirname(os.path.dirname(CURRENT_FILE_PATH))

# Đường dẫn đến thư mục 'train' (Giả định: Capstone-project-VKU/Data/train)
# Bạn cần điều chỉnh phần này nếu cấu trúc khác
TRAIN_FOLDER_PATH = os.path.join(BASE_PROJECT_DIR, "Data_chicken", "Salmonella")

# --- THỰC HIỆN ĐẾM ---

total_images = count_images_in_folder_recursive(TRAIN_FOLDER_PATH)

print("-" * 50)
print(f"Đang tìm kiếm trong thư mục: {TRAIN_FOLDER_PATH}")
if total_images > 0:
    print(f"✅ TỔNG CỘNG có {total_images} file ảnh trong tập train.")
else:
    print(f"⚠️ KHÔNG tìm thấy file ảnh nào. Vui lòng kiểm tra lại đường dẫn.")
print("-" * 50)