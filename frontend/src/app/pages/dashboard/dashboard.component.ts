import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';   // NgIf, NgFor, date pipe
import { FormsModule } from '@angular/forms';     // ngModel
import { Router } from '@angular/router';
import { MealService, Meal } from '../../meals/meal.service';
import { AuthService } from '../../auth/auth.service';

type NewMeal = { date: string; title: string; calories: number; id?: number };

@Component({
  standalone: true,
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.scss'],
  imports: [CommonModule, FormsModule],
})
export class DashboardComponent implements OnInit {
  items: Meal[] = [];
  weekStart = this.todayISO();
  weekEnd = this.todayISO();

  form: NewMeal = { date: this.todayISO(), title: '', calories: 0 };

  loading = false;
  ok: string | null = null;
  error: string | null = null;

  constructor(
    private api: MealService,
    private auth: AuthService,
    private router: Router
  ) {}

  ngOnInit(): void {
    this.load();
  }

  // Odjava
  logout() {
    try { this.auth.logout?.(); } catch {}
    try { localStorage.removeItem('token'); } catch {}
    this.router.navigateByUrl('/login');
  }

  refresh() { this.load(); }

  edit(m: Meal) {
    this.form = { id: m.id, date: m.date, title: m.title, calories: m.calories };
    this.scrollToForm();
  }

  cancelEdit() {
    this.form = { date: this.todayISO(), title: '', calories: 0 };
  }

  remove(m: Meal) {
    if (!confirm('Obrisati ovaj obrok?')) return;
    this.loading = true;
    this.api.remove(m.id!).subscribe({
      next: () => {
        this.loading = false;
        this.setOk('Obrok obrisan.');
        this.load();
      },
      error: (e) => this.setError(e),
    });
  }

  save() {
    if (!this.form.title?.trim()) return this.setError('Naziv je obavezan.');
    if (!this.form.date) return this.setError('Datum je obavezan.');
    if (this.form.calories == null || Number.isNaN(+this.form.calories))
      return this.setError('kcal mora biti broj.');

    this.loading = true;

    const payload = {
      date: this.form.date,
      title: this.form.title.trim(),
      calories: +this.form.calories,
    };

    const req = this.form.id
      ? this.api.update(this.form.id, payload)
      : this.api.create(payload);

    req.subscribe({
      next: () => {
        this.loading = false;
        this.setOk(this.form.id ? 'Obrok ažuriran.' : 'Obrok dodan.');
        this.cancelEdit();
        this.load();
      },
      error: (e) => this.setError(e),
    });
  }

  load() {
    this.loading = true;
    this.api.list(this.weekStart, this.weekEnd).subscribe({
      next: (res) => {
        this.items = res || [];
        this.loading = false;
        this.error = null;
      },
      error: (e) => this.setError(e),
    });
  }

  // ---- helpers ----
  private setOk(msg: string) {
    this.ok = msg;
    this.error = null;
    setTimeout(() => (this.ok = null), 3000);
  }

  private setError(e: unknown) {
    this.loading = false;
    this.ok = null;
    this.error = this.extractError(e);
    console.error('API error:', e);
  }

  private extractError(e: any): string {
    const payload = e?.error ?? e;
    if (typeof payload === 'string') return payload;
    if (typeof payload?.detail === 'string') return payload.detail;
    if (Array.isArray(payload?.detail)) {
      return payload.detail
        .map((d: any) => d?.msg || d?.error || JSON.stringify(d))
        .join(' • ');
    }
    if (typeof e?.message === 'string') return e.message;
    try { return JSON.stringify(payload); }
    catch { return 'Dogodila se greška. Pokušaj ponovo.'; }
  }

  private todayISO(): string {
    const d = new Date();
    const m = (d.getMonth() + 1).toString().padStart(2, '0');
    const day = d.getDate().toString().padStart(2, '0');
    return `${d.getFullYear()}-${m}-${day}`;
  }

  private scrollToForm() {
    requestAnimationFrame(() => {
      document.querySelector('.form-anchor')?.scrollIntoView({
        behavior: 'smooth',
        block: 'center'
      });
    });
  }
}
