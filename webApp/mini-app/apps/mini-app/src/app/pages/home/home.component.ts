import { Component } from '@angular/core';

@Component({
  selector: 'app-home',
  imports: [],
  template: `
    <div class="home-container h-full flex flex-col items-center justify-center p-6">
      <div class="text-center space-y-6">
        <!-- Welcome Icon -->
        <div class="flex justify-center">
          <div class="w-24 h-24 bg-primary-100 rounded-full flex items-center justify-center">
            <svg class="w-12 h-12 text-primary-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 12l2-2m0 0l7-7 7 7M5 10v10a1 1 0 001 1h3m10-11l2 2m-2-2v10a1 1 0 01-1 1h-3m-6 0a1 1 0 001-1v-4a1 1 0 011-1h2a1 1 0 011 1v4a1 1 0 001 1m-6 0h6"></path>
            </svg>
          </div>
        </div>

        <!-- Welcome Text -->
        <div>
          <h1 class="text-3xl font-bold text-gray-900 mb-2">
            خوش آمدید
          </h1>
          <p class="text-gray-600">
            به سیستم مدیریت انبار بازار دقیق
          </p>
        </div>

        <!-- Quick Stats (Placeholder for future dashboard) -->
        <div class="grid grid-cols-2 gap-4 mt-8 w-full max-w-md">
          <div class="bg-white rounded-lg shadow-md p-4 text-center">
            <div class="text-2xl font-bold text-primary-600">--</div>
            <div class="text-sm text-gray-600 mt-1">کل کالاها</div>
          </div>
          <div class="bg-white rounded-lg shadow-md p-4 text-center">
            <div class="text-2xl font-bold text-red-600">--</div>
            <div class="text-sm text-gray-600 mt-1">کم موجودی</div>
          </div>
        </div>

        <!-- Info Text -->
        <p class="text-sm text-gray-500 mt-6">
          در آینده، داشبورد مدیریتی در اینجا نمایش داده خواهد شد
        </p>
      </div>
    </div>
  `,
  styles: `
    .home-container {
      background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
      min-height: 100%;
    }
  `,
})
export class HomeComponent {}

