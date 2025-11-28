# Find Box Auto-Suggest

<p align="center">
  <strong>Ứng dụng tìm kiếm và gợi ý từ khóa nhanh chóng cho Windows</strong><br>
  <em>A lightning-fast keyword search and auto-suggestion tool for Windows</em>
</p>

---

## 📖 Giới Thiệu / Overview

**Find Box Auto-Suggest** là một ứng dụng tiện ích desktop cho Windows, cho phép bạn nhanh chóng truy cập và sao chép các từ khóa, câu lệnh, đoạn văn bản thường dùng chỉ với vài phím tắt.

Ứng dụng hoạt động như một "clipboard manager thông minh" với khả năng tìm kiếm và gợi ý theo thời gian thực, giúp tăng năng suất làm việc đáng kể.

---

## ✨ Điểm Nổi Bật / Key Features

### 🚀 Truy Cập Siêu Nhanh
- **Global Hotkey**: Nhấn `Ctrl + Alt + F` tại bất kỳ đâu để mở hộp tìm kiếm
- **Xuất hiện tại con trỏ chuột**: Hộp tìm kiếm luôn hiện ở vị trí thuận tiện nhất
- **Tự động ẩn**: Click ra ngoài hoặc nhấn `Esc` để đóng ngay lập tức

### 🎯 Tìm Kiếm Thông Minh
- **Gợi ý theo thời gian thực**: Kết quả hiện ngay khi bạn gõ
- **Tìm kiếm ưu tiên**: 
  - Ưu tiên từ khóa tắt (shortcut)
  - Sau đó là nội dung (content)
  - Hỗ trợ tìm kiếm "starts with" và "contains"
- **Hỗ trợ tiếng Việt**: Tìm kiếm và hiển thị hoàn hảo với ký tự có dấu

### ⌨️ Điều Hướng Linh Hoạt
- **Phím mũi tên**: Di chuyển lên/xuống để chọn gợi ý
- **Tự động điền**: Gợi ý được chọn tự động điền vào ô tìm kiếm
- **Enter hoặc Click**: Sao chép ngay vào clipboard
- **Highlight đầu tiên**: Kết quả đầu tiên tự động được đánh dấu sẵn

### 🔧 Định Dạng Shortcut Mạnh Mẽ
**Format**: `shortcut||nội dung thực tế`

**Ví dụ**:
```
ch  ||clear-history
ssh ||ssh ayumi@100.95.20.19
conda||conda activate ana39
```

**Lợi ích**:
- Gõ `ch` → Hiện `ch ||clear-history` → Enter → Copy `clear-history`
- Dễ nhớ, dễ tìm với các phím tắt ngắn gọn
- Hiển thị đầy đủ context nhưng chỉ copy phần cần thiết

### 🎨 Giao Diện Hiện Đại
- **Borderless & Transparent**: Giao diện tối giản, không viền
- **Dark Theme**: Màu tối dễ nhìn, tương phản cao
- **Responsive**: Tự động điều chỉnh kích thước theo nội dung
- **Smart Positioning**: Tự động hiện lên/xuống tùy theo vị trí màn hình

### 💾 Quản Lý Từ Khóa
- **Thêm nhanh**: Nút `+` để thêm keyword mới ngay từ hộp tìm kiếm
- **Auto-reload**: Tự động cập nhật khi file `keyword.txt` thay đổi
- **Simple Format**: Chỉ cần text file đơn giản, không cần database

### 🔒 Ổn Định & Hiệu Năng
- **Singleton Pattern**: Chỉ 1 instance chạy tại một thời điểm
- **Low CPU**: Gần như không tiêu tốn tài nguyên khi idle
- **No Lag**: Phản hồi tức thì, không giật lag
- **Plugin-ready**: Dễ dàng tích hợp vào các ứng dụng Python khác

---

## 🛠️ Cài Đặt / Installation

### Yêu Cầu Hệ Thống
- **OS**: Windows 10/11
- **Python**: 3.9 trở lên
- **Dependencies**: PyQt6, pynput

### Các Bước Cài Đặt

1. **Clone hoặc tải project**:
```bash
git clone <repository-url>
cd auto-suggest
```

2. **Cài đặt dependencies**:
```bash
pip install -r requirements.txt
```

3. **Chạy ứng dụng**:
```bash
python main.py
```

4. **Sử dụng**:
   - Nhấn `Ctrl + Alt + F` để mở hộp tìm kiếm
   - Gõ để tìm kiếm
   - Nhấn Enter hoặc Click để copy

---

## 📚 Hướng Dẫn Sử Dụng / User Guide

### 1. Mở Hộp Tìm Kiếm
- Nhấn `Ctrl + Alt + F` tại bất kỳ đâu
- Hộp tìm kiếm xuất hiện tại vị trí con trỏ chuột
- Con trỏ tự động focus vào ô nhập liệu

### 2. Tìm Kiếm
- Gõ từ khóa (ví dụ: `ssh`, `conda`, `ch`)
- Danh sách gợi ý hiện ngay lập tức
- Từ khóa đầu tiên tự động được highlight

### 3. Chọn và Copy
**Cách 1**: Nhấn `Enter` ngay → Copy từ khóa đầu tiên
**Cách 2**: Dùng `↑`/`↓` để chọn → Nhấn `Enter`
**Cách 3**: Click chuột vào gợi ý

### 4. Thêm Từ Khóa Mới
- Gõ nội dung mới vào ô tìm kiếm
- Nhấn nút `+` bên phải
- Từ khóa được thêm vào đầu file `keyword.txt`

### 5. Đóng Hộp Tìm Kiếm
- Nhấn `Esc`
- Click ra ngoài hộp tìm kiếm
- Chọn và copy một từ khóa (tự động đóng)

---

## 📝 Quản Lý Keyword File

### Định Dạng File `keyword.txt`

**Format 1**: Shortcut với nội dung đầy đủ
```
shortcut||nội dung thực tế
```

**Format 2**: Nội dung thông thường (không có shortcut)
```
nội dung đơn giản
```

### Ví Dụ Thực Tế

```
# Commands
ch  ||clear-history
ws  ||webserver
ns  ||nvidia-smi

# SSH Connections  
ssh ||ssh ayumi@100.95.20.19
ssh ||ssh -t ayumi@100.95.20.19 'cd /home/ayumi && ./run.sh'

# Conda Environments
conda  ||conda activate ana39
conda9 ||conda activate ana9
conda11||conda activate ana11

# Vietnamese Text
dg ||đơn giản
gt ||giải thích
hd ||hướng dẫn
```

### Thứ Tự Ưu Tiên Tìm Kiếm

Khi bạn gõ `ssh`:
1. **Shortcut bắt đầu với "ssh"** → Hiện trước
2. **Nội dung bắt đầu với "ssh"** → Hiện sau
3. **Shortcut chứa "ssh"** → Hiện sau nữa
4. **Nội dung chứa "ssh"** → Cuối cùng

---

## 🏗️ Kiến Trúc Ứng Dụng / Architecture

### Cấu Trúc Thư Mục
```
auto-suggest/
├── main.py              # Entry point
├── keyword.txt          # Dữ liệu từ khóa
├── requirements.txt     # Dependencies
├── GEMINI.md           # Project context
├── README.md           # Documentation
└── src/
    ├── ui.py           # Giao diện PyQt6
    ├── search.py       # Logic tìm kiếm
    ├── hotkey.py       # Global hotkey listener
    └── plugin.py       # Plugin wrapper
```

### Các Module Chính

#### 1. `main.py`
- Entry point của ứng dụng
- Khởi tạo QApplication
- Kết nối các components
- Implement Singleton pattern

#### 2. `src/ui.py` - SearchOverlay
- Giao diện hộp tìm kiếm
- Borderless, frameless window
- Event handling (keyboard, mouse, focus)
- Smart positioning (up/down)
- Click-outside detection

#### 3. `src/search.py` - SearchEngine
- Load và parse `keyword.txt`
- Tìm kiếm với prioritization
- File watcher (auto-reload)
- Hỗ trợ format `shortcut||content`

#### 4. `src/hotkey.py` - HotkeyListener
- Listen global hotkey `Ctrl+Alt+F`
- Listen global `Esc` key
- Thread-safe signal communication
- Pynput integration

#### 5. `src/plugin.py` - FindBoxPlugin
- Wrapper để dễ dàng integrate
- Hỗ trợ embed vào app khác

---

## 🎮 Phím Tắt / Keyboard Shortcuts

| Phím | Chức Năng |
|------|-----------|
| `Ctrl + Alt + F` | Mở/Focus hộp tìm kiếm |
| `Esc` | Đóng hộp tìm kiếm (global) |
| `↓` | Di chuyển xuống gợi ý |
| `↑` | Di chuyển lên gợi ý |
| `Enter` | Copy gợi ý được chọn |
| `Click` | Copy gợi ý được click |

---

## 🔮 Phương Hướng Phát Triển / Future Development

### Tính Năng Đang Xem Xét

#### 📊 Thống Kê & Analytics
- [ ] Đếm số lần sử dụng mỗi keyword
- [ ] Sắp xếp theo độ phổ biến
- [ ] Gợi ý thông minh dựa trên context

#### 🔍 Tìm Kiếm Nâng Cao
- [ ] Fuzzy search (tìm kiếm mờ)
- [ ] Tìm kiếm regex
- [ ] Tìm kiếm theo tag/category
- [ ] Multi-file support

#### 🎨 Giao Diện
- [ ] Themes (Light/Dark/Custom)
- [ ] Configurable colors
- [ ] Font customization
- [ ] Icon support

#### ⚙️ Cấu Hình
- [ ] Settings GUI
- [ ] Custom hotkey configuration
- [ ] Window size/position preferences
- [ ] Max results limit

#### 🔄 Đồng Bộ
- [ ] Cloud sync (Google Drive, Dropbox)
- [ ] Git integration
- [ ] Multi-device sync
- [ ] Import/Export functionality

#### 🧩 Tích Hợp
- [ ] Browser extension
- [ ] VS Code extension
- [ ] PowerToys integration
- [ ] Alfred/Raycast-like workflow

#### 🛡️ Bảo Mật
- [ ] Encrypted keywords
- [ ] Password-protected items
- [ ] Biometric unlock
- [ ] Clipboard auto-clear

#### 📱 Cross-Platform
- [ ] macOS support
- [ ] Linux support
- [ ] Web version
- [ ] Mobile companion app

---

## 🐛 Troubleshooting

### Ứng dụng không chạy
```bash
# Kiểm tra dependencies
pip install -r requirements.txt --upgrade

# Kiểm tra Python version
python --version  # Cần >= 3.9
```

### Hotkey không hoạt động
- Kiểm tra xem `Ctrl + Alt + F` có bị trùng với phím tắt khác không
- Chạy ứng dụng với quyền Administrator (nếu cần)
- Kiểm tra pynput đã cài đúng chưa

### File keyword.txt không tự động reload
- Kiểm tra quyền đọc/ghi file
- Đảm bảo file tồn tại trong cùng thư mục với `main.py`

### Giao diện bị lỗi hiển thị
- Cập nhật PyQt6: `pip install PyQt6 --upgrade`
- Kiểm tra driver card màn hình

---

## 🤝 Đóng Góp / Contributing

Mọi đóng góp đều được hoan nghênh! Bạn có thể:

- 🐛 Báo cáo bug qua Issues
- 💡 Đề xuất tính năng mới
- 🔧 Gửi Pull Request
- 📖 Cải thiện documentation
- 🌍 Dịch sang ngôn ngữ khác

---

## 📄 License

[Thêm license của bạn ở đây]

---

## 👨‍💻 Tác Giả / Author

[Thêm thông tin của bạn]

---

## 🙏 Lời Cảm Ơn / Acknowledgments

- **PyQt6**: Giao diện đẹp và mạnh mẽ
- **pynput**: Global hotkey listener
- **Python Community**: Hỗ trợ và inspiration

---

## 📞 Liên Hệ / Contact

- Email: [your-email]
- GitHub: [your-github]
- Issues: [issues-url]

---

<p align="center">
  Made with ❤️ for productivity enthusiasts
</p>
