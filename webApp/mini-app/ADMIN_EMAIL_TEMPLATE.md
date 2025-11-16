# ⚠️ توجه: این روش دیگه کار نمیکنه!

**ادمین هاست گفته:**
> در هاست اشتراکی امکان اجرا روی پورت دلخواه و Reverse Proxy وجود ندارد.

---

## ✅ راه‌حل جدید:

### از cPanel Python App استفاده کن!

1. برو به **cPanel → Setup Python App**
2. کلیک روی **Create Application**
3. تنظیمات:
   - **Python Version**: `3.11`
   - **Application Root**: `/home/xqaebsls/app`
   - **Application URL**: `bazardaghigh.ir/api` (یا `api.bazardaghigh.ir`)
   - **Application Startup File**: `passenger_wsgi_api.py`
   - **Application Entry Point**: `application`

4. **Create** و بعد **Run Pip Install**

---

## 📖 راهنمای کامل:

فایل `CPANEL_API_SETUP.md` رو باز کن.

---

## 📧 ایمیل به ادمین (اختیاری):

اگه میخوای روی **ساب‌دامین** API رو اجرا کنی:

---

**موضوع:** درخواست ساخت ساب‌دامین

سلام،

برای پروژه ربات تلگرام نیاز دارم یک ساب‌دامین:

- **آدرس**: `api.bazardaghigh.ir`
- **مسیر روت**: `/home/xqaebsls/app` (همون جایی که پروژه هست)
- **SSL**: لطفاً Let's Encrypt نصب کنید

من خودم از cPanel Python App برای اجرای API استفاده می‌کنم.

ممنون

---

