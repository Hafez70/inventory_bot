import { Component } from '@angular/core';
import { BottomNavComponent } from '../bottom-nav/bottom-nav.component';

@Component({
  selector: 'wh-layout',
  imports: [BottomNavComponent],
  templateUrl: './layout.component.html',
  styleUrl: './layout.component.css',
})
export class LayoutComponent {}

