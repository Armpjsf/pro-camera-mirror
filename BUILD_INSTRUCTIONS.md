# Pro Camera Mirror - Build Instructions

## วิธีการ Build APK (เลือก 1 วิธี)

### 🌟 วิธีที่ 1: GitHub Actions (แนะนำ - ง่ายที่สุด)

1. **สร้าง GitHub Repository**
   ```bash
   cd "c:\Users\Armdd\OneDrive\Desktop\APK ME"
   git init
   git add .
   git commit -m "Initial commit"
   ```

2. **Push ไปยัง GitHub**
   - สร้าง repository ใหม่บน GitHub.com
   - Run:
   ```bash
   git remote add origin https://github.com/YOUR_USERNAME/pro-camera-mirror.git
   git branch -M main
   git push -u origin main
   ```

3. **รอ Build เสร็จ**
   - ไปที่ GitHub → Actions tab
   - รอ workflow build เสร็จ (~20-30 นาที)
   - Download APK จาก Artifacts

---

### 💻 วิธีที่ 2: Local Build ด้วย WSL2

1. **ติดตั้ง WSL2 (Ubuntu)**
   ```powershell
   wsl --install
   ```
   Restart เครื่อง

2. **เข้า WSL และติดตั้ง Dependencies**
   ```bash
   wsl
   sudo apt update
   sudo apt install -y python3-pip build-essential git zip unzip openjdk-17-jdk
   sudo apt install -y libsdl2-dev libsdl2-image-dev libsdl2-mixer-dev libsdl2-ttf-dev
   pip3 install --upgrade buildozer cython
   ```

3. **Navigate และ Build**
   ```bash
   cd "/mnt/c/Users/Armdd/OneDrive/Desktop/APK ME"
   buildozer android debug
   ```
   รอ ~30-60 นาที (ครั้งแรกจะนานเพราะต้อง download Android SDK)

4. **APK จะอยู่ที่**
   ```
   c:\Users\Armdd\OneDrive\Desktop\APK ME\bin\procamera-1.0.0-arm64-v8a_armeabi-v7a-debug.apk
   ```

---

### 🐳 วิธีที่ 3: Docker Build

1. **ติดตั้ง Docker Desktop**
   - Download จาก https://www.docker.com/products/docker-desktop

2. **Build ด้วย Docker**
   ```powershell
   cd "c:\Users\Armdd\OneDrive\Desktop\APK ME"
   docker run --rm -v ${PWD}:/app kivy/buildozer android debug
   ```

---

## ติดตั้ง APK บนมือถือ

1. **Enable Unknown Sources**
   - Settings → Security → Unknown Sources (เปิด)

2. **Transfer APK**
   - ส่งไฟล์ APK ไปมือถือผ่าน USB, Email, หรือ Cloud

3. **Install**
   - เปิดไฟล์ APK บนมือถือ
   - กด Install

4. **Grant Permissions**
   - อนุญาตให้ใช้กล้อง

---

## การใช้งาน

- **แตะ 1 ครั้ง**: ปรับความสว่าง (0% → 10% → 20% → ... → 50% → รีเซ็ต)
- **แตะ 2 ครั้ง**: กลับด้านภาพ (Mirror mode)
- **Fullscreen**: แอปจะเต็มจออัตโนมัติ

---

## ไฟล์ที่สร้างแล้ว

- ✅ `buildozer.spec` - Configuration สำหรับ build
- ✅ `requirements.txt` - Python dependencies
- ✅ `icon.png` - App icon
- ✅ `.github/workflows/build-apk.yml` - GitHub Actions workflow
