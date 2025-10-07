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
  regEmail = '';
  regPassword = '';
  error = '';

  constructor(private auth: AuthService, private router: Router) {}

  onLogin() {
    this.error = '';
    this.auth.login(this.email, this.password).subscribe({
      next: (res: any) => {
        this.auth.saveToken(res.access_token);
        this.router.navigate(['/dashboard']);
      },
      error: (err) => this.error = err?.error?.detail || 'Greška pri prijavi',
    });
  }

  onRegister() {
    this.error = '';
    this.auth.register(this.regEmail, this.regPassword).subscribe({
      next: () => {
        this.email = this.regEmail;
        this.password = this.regPassword;
        this.onLogin();
      },
      error: (err) => this.error = err?.error || 'Greška pri registraciji',
    });
  }
}
