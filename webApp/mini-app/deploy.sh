#!/bin/bash

# 🚀 Deploy to Root Domain
# This script builds and prepares the app for deployment to https://bazardaghigh.ir/

echo "🏗️  Building Angular App for ROOT DOMAIN deployment..."
echo ""
npm run build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "📁 Built files are in: dist/apps/mini-app/browser/"
    echo ""
    echo "⚠️  IMPORTANT: Root Domain Deployment"
    echo ""
    echo "📋 Next steps for cPanel deployment:"
    echo ""
    echo "1. ⚠️  BACKUP your public_html first!"
    echo "2. Open cPanel File Manager"
    echo "3. Navigate to public_html/"
    echo "4. Upload all files from dist/apps/mini-app/browser/ to ROOT"
    echo "   (DO NOT create subfolder, upload directly to public_html/)"
    echo "5. DO NOT delete api/ or cgi-bin/ folders"
    echo ""
    echo "🌐 Your app will be at: https://bazardaghigh.ir/"
    echo "🔗 Your API will be at: https://bazardaghigh.ir/api/"
    echo ""
    echo "📖 See CPANEL_DEPLOYMENT_GUIDE.md for detailed instructions"
    echo ""
else
    echo "❌ Build failed. Please check errors above."
    exit 1
fi
