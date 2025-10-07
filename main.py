import json
import os
from datetime import datetime

DATA_FILE = "data.json"

# 1. Hàm tiện ích

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


# 2. Đăng ký

def dang_ky():
    data = load_data()
    ten = input("Nhập tên: ")
    email = input("Nhập email: ")
    password = input("Nhập mật khẩu: ")
    re_password = input("Nhập lại mật khẩu: ")

    if password != re_password:
        print("❌ Mật khẩu nhập lại không khớp!")
        return

    for u in data["users"]:
        if u["email"] == email:
            print("❌ Tài khoản đã tồn tại!")
            return

    data["users"].append({
        "ten": ten,
        "email": email,
        "password": password
    })
    save_data(data)
    print("✅ Đăng ký thành công!")


# 3. Đăng nhập

def dang_nhap():
    data = load_data()
    email = input("Email: ")
    password = input("Mật khẩu: ")
    for u in data["users"]:
        if u["email"] == email and u["password"] == password:
            print(f"✅ Đăng nhập thành công! Xin chào {u['ten']}")
            return email
    print("❌ Sai email hoặc mật khẩu!")
    return None

# 4. Ghi thông tin xe (đã sửa — nhập biển số trước)

def ghi_thong_tin_xe(user_email):
    data = load_data()
    bien_so = input("Biển số: ")  # 🔺 Biển số nhập đầu tiên
    ten_xe = input("Tên xe: ")
    model = input("Model xe: ")
    nam_sx = input("Năm sản xuất: ")
    bo_phan_sua = input("Bộ phận đã sửa/thay: ")
    chi_phi = input("Chi phí sửa (VNĐ): ")
    ngay_sua = datetime.now().strftime("%d/%m/%Y")

    thong_tin = {
        "user": user_email,
        "ten_xe": ten_xe,
        "model": model,
        "nam_sx": nam_sx,
        "bien_so": bien_so,
        "bo_phan_sua": bo_phan_sua,
        "chi_phi": chi_phi,
        "ngay_sua": ngay_sua
    }
    data["xe"].append(thong_tin)
    save_data(data)
    print("✅ Đã ghi thông tin xe!")


# 5. Xem, chỉnh sửa, xóa thông tin xe

def xem_danh_sach_xe(user_email):
    data = load_data()
    list_xe = [x for x in data["xe"] if x["user"] == user_email]
    if not list_xe:
        print("⚠️ Chưa có xe nào được ghi.")
        return

    print("\n🚗 Danh sách xe đã sửa:")
    print("-" * 80)
    for i, x in enumerate(list_xe, 1):
        print(f"{i}. Biển số: {x['bien_so']} | Tên xe: {x['ten_xe']} | Model: {x['model']} | Năm: {x['nam_sx']}")
        print(f"   Bộ phận: {x['bo_phan_sua']} | Ngày: {x['ngay_sua']} | Chi phí: {x['chi_phi']} VNĐ")
        print("-" * 80)

    print("A. Chỉnh sửa thông tin xe")
    print("B. Xóa thông tin xe")
    print("Enter để quay lại")
    chon = input("Chọn thao tác: ").strip().upper()

    if chon == "A":
        sua_xe(user_email, list_xe)
    elif chon == "B":
        xoa_xe(user_email, list_xe)

def sua_xe(user_email, list_xe):
    try:
        idx = int(input("Nhập số thứ tự xe cần chỉnh sửa: ")) - 1
        if idx < 0 or idx >= len(list_xe):
            print("❌ Số thứ tự không hợp lệ!")
            return
        data = load_data()
        xe = list_xe[idx]
        print(f"🔧 Đang chỉnh sửa xe {xe['ten_xe']} ({xe['bien_so']})")

        xe["bien_so"] = input(f"Biển số ({xe['bien_so']}): ") or xe["bien_so"]
        xe["ten_xe"] = input(f"Tên xe ({xe['ten_xe']}): ") or xe["ten_xe"]
        xe["model"] = input(f"Model ({xe['model']}): ") or xe["model"]
        xe["nam_sx"] = input(f"Năm SX ({xe['nam_sx']}): ") or xe["nam_sx"]
        xe["bo_phan_sua"] = input(f"Bộ phận ({xe['bo_phan_sua']}): ") or xe["bo_phan_sua"]
        xe["chi_phi"] = input(f"Chi phí ({xe['chi_phi']}): ") or xe["chi_phi"]

        # Cập nhật vào data
        for i, x in enumerate(data["xe"]):
            if x == list_xe[idx]:
                data["xe"][i] = xe
        save_data(data)
        print("✅ Đã cập nhật thông tin xe!")
    except ValueError:
        print("❌ Lỗi: nhập không hợp lệ!")

def xoa_xe(user_email, list_xe):
    try:
        idx = int(input("Nhập số thứ tự xe cần xóa: ")) - 1
        if idx < 0 or idx >= len(list_xe):
            print("❌ Số thứ tự không hợp lệ!")
            return
        data = load_data()
        xe_xoa = list_xe[idx]
        data["xe"] = [x for x in data["xe"] if x != xe_xoa]
        save_data(data)
        print("🗑️ Đã xóa thông tin xe!")
    except ValueError:
        print("❌ Lỗi: nhập không hợp lệ!")


# 6. Xóa tài khoản

def xoa_tai_khoan(user_email):
    data = load_data()
    data["users"] = [u for u in data["users"] if u["email"] != user_email]
    data["xe"] = [x for x in data["xe"] if x["user"] != user_email]
    save_data(data)
    print(f"🗑️ Đã xóa tài khoản: {user_email}")


# 7. Menu chính

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
                dang_ky()
            elif choice == "2":
                user = dang_nhap()
                if user:
                    current_user = user
            elif choice == "0":
                break
        else:
            print(f"\n👤 Đang đăng nhập: {current_user}")
            print("1. Ghi thông tin xe sửa chữa")
            print("2. Xem / Chỉnh sửa / Xóa thông tin xe")
            print("3. Xóa tài khoản")
            print("4. Đăng xuất")
            print("0. Thoát chương trình")
            choice = input("Chọn: ")

            if choice == "1":
                ghi_thong_tin_xe(current_user)
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
