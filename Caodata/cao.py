from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ĐÃ SỬA CHỮA (LƯU FILE VÀO File_Saved) ---

# Lấy đường dẫn của file hiện tại (D:\...\Capstone-project-VKU\Caodata\cao.py)
CURRENT_FILE_PATH = os.path.abspath(__file__)

# Thư mục chứa file code hiện tại (Caodata)
CAODATA_DIR = os.path.dirname(CURRENT_FILE_PATH)

# Lùi về thư mục gốc của project (Capstone-project-VKU)
BASE_PROJECT_DIR = os.path.dirname(CAODATA_DIR)

# 1. Đường dẫn Driver (Nằm ngoài Caodata)
DRIVER_PATH = os.path.join(BASE_PROJECT_DIR, "chromedriver", "chromedriver.exe")

# 2. Đường dẫn file đầu ra (Nằm trong Caodata/File_Saved)
OUTPUT_DIR = os.path.join(CAODATA_DIR, "File_Saved")
FILE_PATH = os.path.join(OUTPUT_DIR, "brain_tumor_code_selenium.txt")

URL = "https://eranfeit.net/brain-tumor-classification-using-deep-learning/"


def scrape_code_with_selenium(url):
    """Sử dụng Selenium để cào các khối code từ URL."""
    driver = None
    all_code = []

    print(f"Bắt đầu cào code từ: {url}")
    print(f"Đường dẫn driver dự kiến: {DRIVER_PATH}")

    try:
        # Kiểm tra sự tồn tại của chromedriver
        if not os.path.exists(DRIVER_PATH):
            print(f"LỖI: Không tìm thấy chromedriver.exe tại: {DRIVER_PATH}")
            print("Chương trình DỪNG lại.")
            return

        # Khởi tạo WebDriver
        service = Service(DRIVER_PATH)
        driver = webdriver.Chrome(service=service)
        driver.get(url)

        # Chờ thẻ <pre> xuất hiện
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "pre")))

        # Tìm tất cả các thẻ <pre> (chứa khối code)
        code_elements = driver.find_elements(By.TAG_NAME, "pre")

        print(f"--- Đã tìm thấy {len(code_elements)} khối code ---")

        for i, element in enumerate(code_elements):
            # Lấy nội dung text
            code_content = element.text

            # Làm sạch nội dung (loại bỏ các dòng trống)
            cleaned_content = '\n'.join([line for line in code_content.splitlines() if line.strip()])

            if cleaned_content:
                all_code.append(cleaned_content)
                print(f"\n======== ĐOẠN CODE {i + 1} ========")
                print(cleaned_content)
                print("-" * 20)

        # Tạo thư mục File_Saved nếu nó chưa tồn tại
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
            print(f"Tạo thư mục: {OUTPUT_DIR}")

        # Lưu vào file text (sử dụng đường dẫn tuyệt đối đã tính toán)
        with open(FILE_PATH, "w", encoding="utf-8") as f:
            f.write("\n\n" + "=" * 50 + "\n\n".join(all_code))

        print(f"\n✅ Đã trích xuất {len(all_code)} đoạn code và lưu vào file '{FILE_PATH}'.")

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

    finally:
        # Đảm bảo đóng trình duyệt
        if driver:
            driver.quit()


# --- KHỞI CHẠY ---
if __name__ == "__main__":
    scrape_code_with_selenium(URL)