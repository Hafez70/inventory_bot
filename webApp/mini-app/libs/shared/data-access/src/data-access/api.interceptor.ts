import { HttpInterceptorFn } from '@angular/common/http';

export const apiInterceptor: HttpInterceptorFn = (req, next) => {
  // Add any headers or transformations needed for API calls
  
  // Example: Add auth token if available (Telegram Web App)
  const tgWebApp = (window as { Telegram?: { WebApp?: { initData: string } } }).Telegram?.WebApp;
  
  if (tgWebApp?.initData) {
    req = req.clone({
      setHeaders: {
        'X-Telegram-Init-Data': tgWebApp.initData,
      },
    });
  }

  return next(req);
};

