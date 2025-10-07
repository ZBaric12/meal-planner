import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Router } from '@angular/router';
import { environment } from '../../environments/environment';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private isBrowser = false;

  constructor(
    private http: HttpClient,
    private router: Router,
    @Inject(PLATFORM_ID) platformId: Object
  ) {
    this.isBrowser = isPlatformBrowser(platformId);
  }

  getToken(): string | null {
    return this.isBrowser ? localStorage.getItem('token') : null;
  }

  isLoggedIn(): boolean { return !!this.getToken(); }

  goToLogin() { this.router.navigateByUrl('/login'); }

  login(email: string, password: string) {
    const body = new URLSearchParams({ username: email, password });
    return this.http.post<{ access_token: string }>(
      `${environment.apiUrl}/auth/login`,
      body.toString(),
      { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
    );
  }

  register(email: string, password: string) {
    return this.http.post(`${environment.apiUrl}/auth/register`, { email, password });
  }

  saveToken(token: string) { if (this.isBrowser) localStorage.setItem('token', token); }

  logout() {
    if (this.isBrowser) localStorage.removeItem('token');
    this.router.navigateByUrl('/login');
  }
}
