import os

# 1. Thiết lập đường dẫn tới thư mục chứa dữ liệu
# Đảm bảo bạn thay thế đường dẫn này bằng đường dẫn thực tế trên máy tính của bạn
# Dựa vào cấu trúc trong ảnh, đường dẫn có thể là:
base_dir = r"D:\Hoc Ki Cuoi\Capstone-project-VKU\Data_chicken\Data\New Castle Disease"


def delete_augmented_images(directory):
    """
    Xóa các tệp ảnh tăng cường (có chứa '_aug') trong một thư mục.
    """
    print(f"Bắt đầu quét thư mục: {directory}")
    deleted_count = 0

    # Kiểm tra xem thư mục có tồn tại không
    if not os.path.isdir(directory):
        print(f"Lỗi: Thư mục '{directory}' không tồn tại hoặc không phải là thư mục.")
        return

    # Duyệt qua tất cả các mục trong thư mục
    for filename in os.listdir(directory):
        # 2. Xác định các tệp ảnh tăng cường
        # Các tệp tăng cường có vẻ chứa chuỗi "_aug" trong tên
        if "_aug" in filename.lower() and filename.lower().endswith(".jpg"):
            file_path = os.path.join(directory, filename)

            try:
                # 3. Xóa tệp
                os.remove(file_path)
                print(f"Đã xóa: {filename}")
                deleted_count += 1
            except OSError as e:
                print(f"Lỗi khi xóa tệp {filename}: {e}")

    print("-" * 30)
    print(f"Hoàn thành. Đã xóa tổng cộng {deleted_count} tệp ảnh tăng cường.")


# Gọi hàm để thực hiện xóa
delete_augmented_images(base_dir)