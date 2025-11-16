import { Component, signal, inject } from '@angular/core';
import { Router, RouterLink, RouterLinkActive } from '@angular/router';
import { NAV_ITEMS } from '../../domain/navigation.constants';

@Component({
  selector: 'wh-bottom-nav',
  imports: [RouterLink, RouterLinkActive],
  templateUrl: './bottom-nav.component.html',
  styleUrl: './bottom-nav.component.css',
})
export class BottomNavComponent {
  private router = inject(Router);
  
  isRTL = signal(document.dir === 'rtl');
  navItems = signal(NAV_ITEMS);

  isActiveRoute(path: string): boolean {
    return this.router.url === path;
  }
}

