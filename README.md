# PENGI CHATBOT 👋

PenGi ChatBot là một Web app dành cho chatbot để tư vấn tuyển sinh cho các trường Đại học ở Việt Nam. Đây là 1 sản phẩm phi lợi nhuận,
hướng đến cộng động học sinh và phụ huynh ở VIỆT NAM nhằm giải quyết vấn đề tư vấn tuyển sinh, giải đáp thắc mắc về các trường đại học
ở Việt Nam.

## Hướng dẫn

### Front-end

1. Tải xuống NVM for Windows: [nvm-setup.exe](https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.exe)
2. Chạy file `.exe` và lưu lại từng PATH mà NVM thiết lập, nên thiết lập theo mặc định.
3. Sau khi cài đặt, chạy lần lượt các lệnh:
4. ```bash
   nvm install 21.0.0
   ```
5. ```bash
   nvm use 21.0.0
   ```
6. Cài đặt bun:
   ```bash
   npm install -g bun
   ```
7. Dev
   ```bash
   bun run dev
   ```
8. Build
   ```bash
   bun run build
   ```

### Back-end (Dùng VSCODE)

1. Ctrl + Shift + P => Gõ "Python: Create Environment" => Chọn Conda cài bản python 3.11

2. Sau đó cd đến backend folder, install requirements file bằng command:
   ```bash
   pip install -r requirments.txt
   ```
3. Chạy ứng dụng
   ```bash
   start_window.bat
   ```

# Lưu ý: ĐẢM BẢO RẰNG TRƯỚC KHI CHẠY THÌ npm phải hoạt động .BẮT BUỘC COMMAND PROMPT thứ 2 phải trỏ đến ROOT FOLDER.

# XEM ROUTER TỪNG APP:

- Đầu tiên, khởi động command prompt thứ nhất như đã hướng dẫn phía trên
- Sau đó, để xem được từng router, copy các đường dẫn sau:

  - Trỏ đến file main (default):

  ```text
  http://localhost:8080/docs
  ```

  - Trỏ để Ollama functions:

  ```text
  http://localhost:8080/ollama/docs
  ```

  - Trỏ đến images function:

  ```text
  http://localhost:8080/images/api/v1/docs
  ```

  - Trỏ đến rag functions:

  ```text
  http://localhost:8080/rag/api/v1/docs
  ```

  - Trỏ đến audio functions:

  ```text
  http://localhost:8080/audio/api/v1/docs#/
  ```

  - Trỏ đến api function:

  ```text
  http://localhost:8080/api/v1/docs#/
  ```

uvicorn main:app --host 0.0.0.0 --port 8080 --forwarded-allow-ips '\*' --reload
