import { NgModule, inject } from '@angular/core';
import { RouterModule, Routes, CanActivateFn } from '@angular/router';
import { LoginComponent } from './pages/login/login.component';
import { DashboardComponent } from './pages/dashboard/dashboard.component';
import { AuthService } from './auth/auth.service';

export const authGuard: CanActivateFn = () => {
  const svc = inject(AuthService);
  if (svc.isLoggedIn()) return true;
  svc.goToLogin();
  return false;
};

const routes: Routes = [
  { path: 'login', component: LoginComponent },
  { path: 'dashboard', component: DashboardComponent, canActivate: [authGuard] },
  { path: '', pathMatch: 'full', redirectTo: 'login' },
  { path: '**', redirectTo: 'login' }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule {}
