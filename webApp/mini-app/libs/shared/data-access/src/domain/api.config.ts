import { InjectionToken } from '@angular/core';

export interface ApiConfig {
  baseUrl: string;
}

export const API_CONFIG = new InjectionToken<ApiConfig>('API_CONFIG');

export const DEFAULT_API_CONFIG: ApiConfig = {
  // Default to relative path for same-domain deployment
  // Override in environment.ts for different environments
  baseUrl: '/api',
};

