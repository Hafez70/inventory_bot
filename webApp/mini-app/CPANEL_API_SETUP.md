# راهنمای راه‌اندازی API در cPanel (بدون پورت دلخواه)

## ⚠️ محدودیت هاست اشتراکی
- امکان اجرای سرویس روی پورت دلخواه وجود ندارد
- امکان تنظیم Reverse Proxy وجود ندارد

---

## ✅ راه‌حل: استفاده از Passenger (cPanel Python App)

---

## 📋 مراحل (خودت انجام بده):

### 1️⃣ در cPanel:

1. برو به **Setup Python App**
2. کلیک روی **Create Application**
3. تنظیمات زیر رو وارد کن:

```
Python Version: 3.11
Application Root: /home/xqaebsls/app
Application URL: bazardaghigh.ir/api (یا api.bazardaghigh.ir اگه ساب‌دامین ساختی)
Application Startup File: passenger_wsgi_api.py
Application Entry Point: application
```

4. کلیک روی **Create**

---

### 2️⃣ نصب Dependencies:

بعد از ساخت، cPanel یه دکمه **Run Pip Install** میده.
روی اون کلیک کن تا dependencies نصب بشه.

یا از Terminal:

```bash
cd ~/app
source ~/virtualenv/app/3.11/bin/activate
pip install -r requirements.txt
```

---

### 3️⃣ Restart Application:

بعد از هر تغییر، باید API رو Restart کنی:

در cPanel → Setup Python App → کلیک روی آیکون **Restart**

---

## 🧪 تست:

### آدرس API:
- اگه روی مسیر نصب کردی: `https://bazardaghigh.ir/api`
- اگه روی ساب‌دامین: `https://api.bazardaghigh.ir`

### تست Health:
```bash
curl https://bazardaghigh.ir/api/health
# یا
curl https://api.bazardaghigh.ir/health
```

### تست Docs:
مرورگر رو باز کن:
- `https://bazardaghigh.ir/api/docs`
- `https://api.bazardaghigh.ir/docs`

---

## ⚠️ نکات مهم:

1. **فایل `passenger_wsgi_api.py` باید در root باشه** (`/home/xqaebsls/app/`)
2. **هر بار تغییر کدی دادی، باید Restart کنی**
3. **اگه Error میده، log رو چک کن:**
   ```bash
   tail -50 ~/app/tmp/log/passenger.log
   ```

---

## 🚨 مشکلات احتمالی:

### 1. `ModuleNotFoundError`:
```bash
cd ~/app
source ~/virtualenv/app/3.11/bin/activate
pip install -r requirements.txt
```

### 2. `500 Internal Server Error`:
```bash
tail -100 ~/app/tmp/log/passenger.log
tail -100 ~/logs/error_log
```

### 3. API کار نمیکنه:
- مطمئن شو که `passenger_wsgi_api.py` در root هست
- مطمئن شو که Application Startup File درست تنظیم شده
- Restart کن

---

## 📝 نتیجه:

با این روش، API مستقیماً از طریق Apache/Passenger اجرا میشه و نیازی به پورت دلخواه یا Reverse Proxy نیست.

✅ **این روش با هاست اشتراکی سازگار است.**

