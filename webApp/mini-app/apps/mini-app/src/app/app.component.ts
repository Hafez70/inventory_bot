import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { LayoutComponent } from '@warehousing/shared/ui-layout';

@Component({
  selector: 'app-root',
  imports: [RouterOutlet, LayoutComponent],
  template: `
    <wh-layout>
      <router-outlet />
    </wh-layout>
  `,
  styles: `
    :host {
      display: block;
      height: 100vh;
      overflow: hidden;
    }
  `,
})
export class AppComponent {}

