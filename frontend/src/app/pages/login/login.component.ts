import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { AuthService } from '../../auth/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
})
export class LoginComponent {
  email = '';
  password = '';

  rEmail = '';
  rPassword = '';

  loading = false;
  error: string | null = null;

  constructor(private auth: AuthService, private router: Router) {}

  login() {
    if (!this.email || !this.password) {
      this.error = 'Unesi email i lozinku.';
      return;
    }
    this.loading = true;
    this.error = null;

    this.auth.login(this.email, this.password).subscribe({
      next: () => {
        this.loading = false;
        this.router.navigateByUrl('/dashboard');
      },
      error: (e) => {
        this.loading = false;
        this.error = this.readErr(e);
      },
    });
  }

  register() {
    if (!this.rEmail || !this.rPassword) {
      this.error = 'Unesi novi email i lozinku.';
      return;
    }
    this.loading = true;
    this.error = null;

    this.auth.register(this.rEmail, this.rPassword).subscribe({
      next: () => {
        this.loading = false;
        // odmah pokušaj login s novim kredencijalima
        this.email = this.rEmail;
        this.password = this.rPassword;
        this.login();
      },
      error: (e) => {
        this.loading = false;
        this.error = this.readErr(e);
      },
    });
  }

  private readErr(e: any): string {
    const p = e?.error ?? e;
    if (typeof p === 'string') return p;
    if (typeof p?.detail === 'string') return p.detail;
    if (Array.isArray(p?.detail)) {
      return p.detail.map((d: any) => d?.msg || d?.error || JSON.stringify(d)).join(' • ');
    }
    if (typeof e?.message === 'string') return e.message;
    try { return JSON.stringify(p); } catch { return 'Došlo je do greške.'; }
  }
}
