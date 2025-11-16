export const SEARCH_CONFIG = {
  MIN_QUERY_LENGTH: 2,
  DEBOUNCE_TIME: 500,
} as const;

export const EMPTY_STATES = {
  NO_SEARCH: {
    title: 'جستجوی کالا',
    description: 'برای یافتن کالا، نام، کد سفارشی یا توضیحات آن را وارد کنید',
  },
  NO_RESULTS: {
    title: 'نتیجه‌ای یافت نشد',
    description: 'هیچ کالایی با این مشخصات پیدا نشد. لطفا عبارت دیگری را جستجو کنید',
  },
} as const;

export const PLACEHOLDERS = {
  SEARCH_INPUT: 'نام کالا، کد سفارشی یا توضیحات...',
} as const;

