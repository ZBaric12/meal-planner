import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export type Meal = { id?: number; date: string; title: string; calories: number };

@Injectable({ providedIn: 'root' })
export class MealService {
  private base = `${environment.apiUrl}/meals`;
  constructor(private http: HttpClient) {}

  list(from?: string, to?: string): Observable<Meal[]> {
    let params = new HttpParams();
    if (from) params = params.set('from_', from);
    if (to) params = params.set('to', to);
    return this.http.get<Meal[]>(this.base, { params });
  }

  create(data: Omit<Meal, 'id'>): Observable<Meal> {
    return this.http.post<Meal>(this.base, data);
  }
  update(id: number, data: Omit<Meal, 'id'>): Observable<Meal> {
    return this.http.put<Meal>(`${this.base}/${id}`, data);
  }
  remove(id: number): Observable<void> {
    return this.http.delete<void>(`${this.base}/${id}`);
  }
}
