import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Cancion } from './cancion';
import { Album } from '../album/album';
import { environment } from 'src/environments/environment';

@Injectable({
  providedIn: 'root',
})
export class CancionService {
  private backUrl: string = environment.baseUrl;

  constructor(private http: HttpClient) {}

  getCancionesAlbum(idAlbum: number, token: string): Observable<Cancion[]> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
    return this.http.get<Cancion[]>(
      `${this.backUrl}/album/${idAlbum}/canciones`,
      { headers: headers }
    );
  }

  getCanciones(token: string): Observable<Cancion[]> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
    return this.http.get<Cancion[]>(
      `${this.backUrl}/canciones`,
        { headers: headers }
    );
  }

  getAlbumesCancion(cancionId: number): Observable<Album[]> {
    return this.http.get<Album[]>(
      `${this.backUrl}/cancion/${cancionId}/albumes`
    );
  }

  crearCancion(cancion: Cancion): Observable<Cancion> {
    return this.http.post<Cancion>(`${this.backUrl}/canciones`, cancion);
  }

  getCancion(cancionId: number): Observable<Cancion> {
    return this.http.get<Cancion>(`${this.backUrl}/cancion/${cancionId}`);
  }

  editarCancion(cancion: Cancion, cancionId: number): Observable<Cancion> {
    return this.http.put<Cancion>(
      `${this.backUrl}/cancion/${cancionId}`,
      cancion
    );
  }

  eliminarCancion(cancionId: number): Observable<Cancion> {
    return this.http.delete<Cancion>(`${this.backUrl}/cancion/${cancionId}`);
  }

  compartirCancion(
    cancionId: number,
    usuarios: Array<string>,
    token: string
  ): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
    return this.http
      .post<string>(
        `${this.backUrl}/cancion/${cancionId}/usuarios-compartidos`,
        { usuarios_compartidos: usuarios },
        { headers: headers }
      );
  }

  consultarUsuariosCompartidos(
    cancionId: number,
    token: string
  ): Observable<any> {
    const headers = new HttpHeaders({
      Authorization: `Bearer ${token}`,
    });
    return this.http.get<string>(
      `${this.backUrl}/cancion/${cancionId}/usuarios-compartidos`,
      { headers: headers }
    );
  }
}
