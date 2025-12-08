import csv
import os
import random

# =========================
# PREFIX CHO TỪNG LOẠI FILE
# =========================

PREFIX_MAP = {
    "password": ["password: ", "code: ", "secret: ", "pwd: ", "pass: "],
    "message": ["msg: ", "message: ", "txt: ", "content: ", "text: "],
    "name": ["name: ", "fname: ", "username: ", "lname: ", "fullname: "],
    "address": ["address: ", "addr: "],
    "email": ["email: "],
    "phone_number": ["phonenumber: ", "number: ", "phone: ", "sdt: ", "sodienthoai: "],
    "content_type": ["Content-Type: "],
}

def add_prefix(filepath: str, text: str):
    """Thêm prefix ngẫu nhiên dựa trên tên file."""
    name = os.path.basename(filepath).split('.')[0].lower()

    # tìm prefix phù hợp
    for key in PREFIX_MAP:
        if key in name:
            return random.choice(PREFIX_MAP[key]) + text

    # không thuộc nhóm nào → giữ nguyên
    return text


# =========================
# READ NORMAL
# =========================

def read_norm_txt(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # thêm prefix
            payload = add_prefix(filepath, line)

            yield {
                "payload": payload,
                "type": os.path.basename(filepath).split('.')[0],
                "label": "normal"
            }


# =========================
# READ MALICIOUS
# =========================

def read_anom_txt(filepath: str):
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            # thêm prefix
            payload = add_prefix(filepath, line)

            yield {
                "payload": payload,
                "type": os.path.basename(filepath).split('.')[0],
                "label": "malicious"
            }


# =========================
# APPEND FOLDER → CSV
# =========================

def append_folder_to_csv(folder: str, label: str, csv_file="data.csv"):
    file_exists = os.path.isfile(csv_file)

    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["payload", "type", "label"])

        if not file_exists:
            writer.writeheader()

        folder_path = folder + "/"
        for filename in os.listdir(folder_path):
            if not filename.lower().endswith(".txt"):
                continue

            filepath = folder_path + filename
            print(f"Đang xử lý file: {filepath}")

            if label == "malicious":
                for row in read_anom_txt(filepath):
                    writer.writerow(row)
            else:
                for row in read_norm_txt(filepath):
                    writer.writerow(row)

    print(f"➡ Đã thêm dữ liệu từ thư mục '{folder}/' vào '{csv_file}'")


# ===============================
# CHẠY CHO 2 THƯ MỤC norm & anom
# ===============================

append_folder_to_csv("norm", "normal")
append_folder_to_csv("anom", "malicious")
