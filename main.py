import json
import os
from datetime import datetime

DATA_FILE = "data.json"

# ==============================
# 1. Hàm tiện ích
# ==============================
def load_data():
    """Đọc dữ liệu từ file JSON"""
    if not os.path.exists(DATA_FILE):
        return {"users": [], "xe": []}
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_data(data):
    """Lưu dữ liệu vào file JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

# ==============================
# 2. Đăng ký
# ==============================
def dang_ky(email, password):
    data = load_data()
    for u in data["users"]:
        if u["email"] == email:
            print("❌ Tài khoản đã tồn tại!")
            return
    data["users"].append({"email": email, "password": password})
    save_data(data)
    print("✅ Đăng ký thành công!")

# ==============================
# 3. Đăng nhập
# ==============================
def dang_nhap(email, password):
    data = load_data()
    for u in data["users"]:
        if u["email"] == email and u["password"] == password:
            print("✅ Đăng nhập thành công!")
            return email
    print("❌ Sai email hoặc mật khẩu!")
    return None

# ==============================
# 4. Ghi thông tin xe
# ==============================
def ghi_thong_tin_xe(user_email, ten_xe, bien_so, chi_phi, ngay_sua=None):
    data = load_data()
    if ngay_sua is None:
        ngay_sua = datetime.now().strftime("%d/%m/%Y")
    thong_tin = {
        "user": user_email,
        "ten_xe": ten_xe,
        "bien_so": bien_so,
        "chi_phi": chi_phi,
        "ngay_sua": ngay_sua
    }
    data["xe"].append(thong_tin)
    save_data(data)
    print("✅ Đã ghi thông tin xe!")

# ==============================
# 5. Xem danh sách xe
# ==============================
def xem_danh_sach_xe(user_email):
    data = load_data()
    list_xe = [x for x in data["xe"] if x["user"] == user_email]
    if not list_xe:
        print("⚠️ Chưa có xe nào được ghi.")
        return
    print("\n🚗 Danh sách xe đã sửa:")
    print("-" * 60)
    for x in list_xe:
        print(f"Tên xe: {x['ten_xe']}\nBiển số: {x['bien_so']}\nNgày sửa: {x['ngay_sua']}\nChi phí: {x['chi_phi']} VNĐ\n---")

# ==============================
# 6. Xóa tài khoản
# ==============================
def xoa_tai_khoan(user_email):
    data = load_data()
    # Xóa user
    data["users"] = [u for u in data["users"] if u["email"] != user_email]
    # Xóa dữ liệu xe của user đó
    data["xe"] = [x for x in data["xe"] if x["user"] != user_email]
    save_data(data)
    print(f"🗑️ Đã xóa tài khoản: {user_email}")

# ==============================
# 7. Chạy chương trình
# ==============================
def menu():
    current_user = None
    while True:
        print("\n===== QUẢN LÝ SỬA XE =====")
        if not current_user:
            print("1. Đăng ký")
            print("2. Đăng nhập")
            print("0. Thoát")
            choice = input("Chọn: ")
            if choice == "1":
                email = input("Nhập email: ")
                password = input("Nhập mật khẩu: ")
                dang_ky(email, password)
            elif choice == "2":
                email = input("Email: ")
                password = input("Mật khẩu: ")
                user = dang_nhap(email, password)
                if user:
                    current_user = user
            elif choice == "0":
                break
        else:
            print(f"\n👤 Đang đăng nhập: {current_user}")
            print("1. Ghi thông tin xe")
            print("2. Xem danh sách xe")
            print("3. Xóa tài khoản")
            print("4. Đăng xuất")
            print("0. Thoát chương trình")
            choice = input("Chọn: ")

            if choice == "1":
                ten = input("Tên xe: ")
                bien = input("Biển số: ")
                chi_phi = input("Chi phí sửa (VNĐ): ")
                ghi_thong_tin_xe(current_user, ten, bien, chi_phi)
            elif choice == "2":
                xem_danh_sach_xe(current_user)
            elif choice == "3":
                xoa_tai_khoan(current_user)
                current_user = None
            elif choice == "4":
                current_user = None
                print("👋 Đã đăng xuất.")
            elif choice == "0":
                break

if __name__ == "__main__":
    menu()
