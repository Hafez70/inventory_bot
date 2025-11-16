# 🚀 Quick Deploy Checklist

## ✅ Pre-Deployment

- [ ] Backup `public_html/` on cPanel
- [ ] Test API: https://bazardaghigh.ir/api/health
- [ ] Build passes locally: `npm run build`

---

## 📦 Deploy Steps

### 1️⃣ Build (Local Windows)
```bash
cd D:\projects\ci-farco\warehousing\webApp\mini-app
.\deploy.bat
```

### 2️⃣ Backup (cPanel Terminal)
```bash
cd ~
tar -czf public_html_backup_$(date +%Y%m%d).tar.gz public_html/
```

### 3️⃣ Upload Files (cPanel File Manager)
- Go to `public_html/`
- Upload ALL files from `dist\apps\mini-app\browser\`
- **DO NOT delete:** `api/`, `cgi-bin/`, other folders

### 4️⃣ Create .htaccess (cPanel Terminal)
```bash
cd ~/public_html
cat > .htaccess << 'EOF'
<IfModule mod_rewrite.c>
  RewriteEngine On
  RewriteCond %{REQUEST_FILENAME} -f [OR]
  RewriteCond %{REQUEST_FILENAME} -d
  RewriteRule ^ - [L]
  RewriteCond %{REQUEST_URI} !^/api
  RewriteCond %{REQUEST_URI} !^/cgi-bin
  RewriteRule ^ index.html [L]
</IfModule>
EOF
```

---

## 🧪 Testing

- [ ] Root: https://bazardaghigh.ir/ → Should show Angular app
- [ ] API: https://bazardaghigh.ir/api/health → Should return `{"status":"healthy"}`
- [ ] Search: https://bazardaghigh.ir/api/items/search?q=test → Should return items
- [ ] Refresh page → Should NOT get 404

---

## 📂 Final Structure

```
~/public_html/
├── index.html           ✅ Angular entry
├── main-*.js            ✅ Angular bundle
├── polyfills-*.js       ✅ Angular polyfills
├── styles-*.css         ✅ Angular styles
├── .htaccess            ✅ Routing config
├── api/                 ⚠️  Keep (API folder)
└── cgi-bin/             ⚠️  Keep (System folder)
```

---

## 🔄 Update Deployment

1. Build: `.\deploy.bat`
2. Upload: Overwrite files in `public_html/`
3. Clear cache: Ctrl+Shift+R

---

## 🆘 Troubleshooting

| Problem | Solution |
|---------|----------|
| Directory listing | Upload `index.html` to root |
| 404 on refresh | Create `.htaccess` |
| API not working | Check `/api` folder exists |
| Blank page | Check console (F12) |

---

## 🔗 URLs

| Service | URL |
|---------|-----|
| App | https://bazardaghigh.ir/ |
| API | https://bazardaghigh.ir/api/ |
| Health | https://bazardaghigh.ir/api/health |
| Search | https://bazardaghigh.ir/api/items/search?q=test |

---

## 📞 Need Help?

See `CPANEL_DEPLOYMENT_GUIDE.md` for detailed instructions.

