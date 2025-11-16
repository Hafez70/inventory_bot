import { NavItem } from './navigation.model';

export const NAV_ITEMS: NavItem[] = [
  {
    path: '/home',
    label: 'خانه',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path></svg>`,
    activeIcon: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M10.707 2.293a1 1 0 00-1.414 0l-7 7a1 1 0 001.414 1.414L4 10.414V17a1 1 0 001 1h2a1 1 0 001-1v-2a1 1 0 011-1h2a1 1 0 011 1v2a1 1 0 001 1h2a1 1 0 001-1v-6.586l.293.293a1 1 0 001.414-1.414l-7-7z"></path></svg>`,
  },
  {
    path: '/search',
    label: 'جستجو',
    icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path></svg>`,
    activeIcon: `<svg fill="currentColor" viewBox="0 0 24 24"><path d="M9 2a7 7 0 104.906 12.02l5.537 5.536a1 1 0 001.414-1.414l-5.536-5.537A7 7 0 009 2z"></path></svg>`,
  },
];

