# PENGI CHATBOT 👋

PenGi ChatBot là một Web app dành cho chatbot để tư vấn tuyển sinh cho các trường Đại học ở Việt Nam. Đây là 1 sản phẩm phi lợi nhuận,
hướng đến cộng động học sinh và phụ huynh ở VIỆT NAM nhằm giải quyết vấn đề tư vấn tuyển sinh, giải đáp thắc mắc về các trường đại học
ở Việt Nam.

## Thiết lập môi trường

### Front-end

1. Tải xuống NVM for Windows: [nvm-setup.exe](https://github.com/coreybutler/nvm-windows/releases/download/1.1.12/nvm-setup.exe)
2. Chạy file `.exe` và lưu lại từng PATH mà NVM thiết lập, nên thiết lập theo mặc định.
3. Sau khi cài đặt, mở `cmd` và chạy `nvm`.
4. Trong `cmd`, gõ lệnh sau để cài đặt Node.js phiên bản _21.0.0_:
   ```bash
   nvm install 21.0.0
   ```

### Back-end

1. Khởi động anaconda prompt, tạo một env mới tên là backend theo command sau

```bash
conda create --name backend python=3.10
```

2. Sau đó khởi động env backend bằng command sau

```bash
conda activate backend
```

3. Sau đó cd đến rootfolder, tạo 1 venv ảo bằng command:
   ```bash
   python -m venv venv
   ```
4. Sau đó cd đến backend folder, install requirements file bằng command:
   ```bash
   pip install -r requirments.txt
   ```

## Khởi động hệ thống

- Để khởi động hệ thống, chúng ta sẽ bật 2 COMMAND PROMPT:

1. Ở COMMAND PROMPT ĐẦU TIÊN, ta kích hoạt env bằng **TỪNG** command sau:

   ```bash
   conda activate backend
   cd venv/Scripts
   activate
   cd ../..
   cd backend
   starts_windows
   ```

2. COMMAND PROMPT thứ 2 trỏ đến ROOT FOLDER. Ví dụ root folder đang lưu ở ổ `E:\PengiChat` , thì ta sẽ dùng lệnh
   `bash
    cd E:\PengiChat
    `
   Sau đó gõ command sau để khởi động front-end:
   `bash
    npm run s-dev
    `

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
