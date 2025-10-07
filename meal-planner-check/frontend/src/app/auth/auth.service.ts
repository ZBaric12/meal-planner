import { Injectable, Inject, PLATFORM_ID } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import { HttpClient, HttpParams } from '@angular/common/http';
import { environment } from '../../environments/environment';
import { Observable } from 'rxjs';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private api = environment.apiUrl;

  constructor(
    private http: HttpClient,
    @Inject(PLATFORM_ID) private platformId: Object,
  ) {}

  private get storage(): Storage | null {
    return isPlatformBrowser(this.platformId) ? localStorage : null;
  }

  login(email: string, password: string): Observable<any> {
    const body = new HttpParams()
      .set('username', email)
      .set('password', password);
    return this.http.post(`${this.api}/auth/login`, body.toString(), {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  }

  register(email: string, password: string): Observable<any> {
    return this.http.post(`${this.api}/auth/register`, { email, password });
  }

  saveToken(token: string) { this.storage?.setItem('access_token', token); }
  getToken(): string | null { return this.storage?.getItem('access_token') ?? null; }
  clearToken() { this.storage?.removeItem('access_token'); }
  isLoggedIn(): boolean { return !!this.getToken(); }
}
