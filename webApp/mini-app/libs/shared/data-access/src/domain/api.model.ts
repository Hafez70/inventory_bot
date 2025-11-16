export interface ApiResponse<T> {
  data: T;
  status: string;
  message?: string;
}

export interface ApiError {
  status: number;
  message: string;
  details?: unknown;
}

