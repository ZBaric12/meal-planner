import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { AuthService } from '../../auth/auth.service';
import { Router } from '@angular/router';

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
  error: string | null = null;

  constructor(private auth: AuthService, private router: Router) {}

  login() {
    this.error = null;
    this.auth.login(this.email, this.password).subscribe({
      next: (res) => {
        this.auth.saveToken(res.access_token);
        this.router.navigateByUrl('/dashboard');
      },
      error: (e) => this.error = e?.error?.detail || 'Neuspjela prijava.',
    });
  }

  register() {
    this.error = null;
    this.auth.register(this.rEmail, this.rPassword).subscribe({
      next: () => this.auth.login(this.rEmail, this.rPassword).subscribe({
        next: (res) => {
          this.auth.saveToken(res.access_token);
          this.router.navigateByUrl('/dashboard');
        },
        error: (e) => this.error = e?.error?.detail || 'Neuspjela prijava nakon registracije.',
      }),
      error: (e) => this.error = e?.error?.detail || 'Neuspjela registracija.',
    });
  }
}
