import csv
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

# --- CẤU HÌNH ĐƯỜNG DẪN ĐÃ SỬA CHỮA (Tương thích với cấu trúc của bạn) ---

# Lấy đường dẫn của thư mục Caodata (thư mục chứa file code hiện tại)
CAODATA_DIR = os.path.dirname(os.path.abspath(__file__))

# Lùi 1 cấp thư mục để trỏ về thư mục gốc của project (Capstone-project-VKU)
BASE_PROJECT_DIR = os.path.dirname(CAODATA_DIR)

# 1. Đường dẫn Driver (Nằm ngoài Caodata)
DRIVER_PATH = os.path.join(BASE_PROJECT_DIR, "chromedriver", "chromedriver.exe")

# 2. Đường dẫn CSV (Nằm trong File_Saved)
CSV_PATH = os.path.join(CAODATA_DIR, "File_Saved", "tiki_reviews.csv")


def scroll_to_bottom(driver, pause_time=1, max_scrolls=10):
    """Cuộn trang xuống nhiều lần để tải tất cả đánh giá."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    for i in range(max_scrolls):
        driver.execute_script("window.scrollBy(0, 1000);")
        time.sleep(pause_time)
        driver.execute_script("window.scrollBy(0, window.innerHeight);")
        time.sleep(pause_time)

        new_height = driver.execute_script("return document.body.scrollHeight")
        print(f"  > Đang cuộn: {i + 1}/{max_scrolls}...")

        if new_height == last_height:
            break
        last_height = new_height


def get_reviews_from_pages(driver, max_pages=10):
    """Thu thập đánh giá, tự động chuyển trang."""
    all_reviews = []
    wait = WebDriverWait(driver, 5)

    for page in range(1, max_pages + 1):
        print(f"  > Đang lấy đánh giá trang {page}...")

        try:
            wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, "review-comment__content")))
            comments = driver.find_elements(By.CLASS_NAME, "review-comment__content")
            all_reviews.extend([c.text for c in comments if c.text.strip()])
        except Exception:
            print("  > Không tìm thấy đánh giá nào trên trang này.")

        next_page_num = page + 1
        try:
            next_btn = wait.until(
                EC.element_to_be_clickable((By.XPATH, f"//a[text()='{next_page_num}']"))
            )
            next_btn.click()
            time.sleep(2)
        except Exception:
            print("  > Hết trang hoặc không có nút kế tiếp.")
            break

    return all_reviews


def getProductInfo(driver, url):
    """Truy cập URL, lấy thông tin sản phẩm và đánh giá, ghi vào CSV."""
    print("-" * 50)
    print(f"Bắt đầu xử lý URL: {url}")
    driver.get(url)

    wait = WebDriverWait(driver, 10)

    try:
        title = wait.until(EC.presence_of_element_located((By.TAG_NAME, "h1"))).text
    except Exception:
        title = "Không tìm thấy tên sản phẩm"

    try:
        price = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "product-price__current-price"))).text
    except Exception:
        price = "Không tìm thấy giá sản phẩm"

    print(f"\n📦 Sản phẩm: {title}")
    print(f"💰 Giá: {price}")

    scroll_to_bottom(driver)
    reviews = get_reviews_from_pages(driver)

    print(f"📝 Thu thập được {len(reviews)} đánh giá.")

    # Kiểm tra và tạo thư mục File_Saved nếu chưa tồn tại
    save_dir = os.path.dirname(CSV_PATH)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
        print(f"Tạo thư mục: {save_dir}")

    # Ghi vào file CSV
    file_exists = os.path.exists(CSV_PATH) and os.path.getsize(CSV_PATH) > 0
    with open(CSV_PATH, mode="a", encoding="utf-8", newline="") as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(["Tên sản phẩm", "Giá", "Đánh giá"])
        for review in reviews:
            writer.writerow([title, price, review])

    print(f"✅ Đã ghi {len(reviews)} đánh giá vào file: {CSV_PATH}")


def startBot(urls):
    """Khởi động bot và xử lý danh sách URL."""
    driver = None
    try:
        if not os.path.exists(DRIVER_PATH):
            print(f"LỖI: Không tìm thấy chromedriver.exe tại: {DRIVER_PATH}")
            print("→ Hãy kiểm tra lại cấu trúc thư mục (nó phải nằm trong Capstone-project-VKU/chromedriver).")
            return

        service = Service(DRIVER_PATH)
        driver = webdriver.Chrome(service=service)

        for url in urls:
            getProductInfo(driver, url)

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")

    finally:
        if driver:
            driver.quit()


# ----------------------------------------------------------------------------------
# DANH SÁCH URL SẢN PHẨM
# ----------------------------------------------------------------------------------
product_urls = [
    "https://tiki.vn/ta-bim-quan-huggies-skin-care-mega-jumbo-xl84-4-mieng-voi-tram-tra-diu-da-p275220816.html?itm_campaign=CTP_YPD_TKA_PLA_UNK_ALL_UNK_UNK_UNK_UNK_X.308555_Y.1890875_Z.4030442_CN.Key-ta-quan-Skin-Care&itm_medium=CPC&itm_source=tiki-ads&spid=275220817",
]

# ----------------------------------------------------------------------------------
# KHỞI CHẠY CHƯƠNG TRÌNH
# ----------------------------------------------------------------------------------
if __name__ == "__main__":
    startBot(product_urls)