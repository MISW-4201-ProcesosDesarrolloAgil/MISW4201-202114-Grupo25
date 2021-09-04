import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { Album, Cancion } from '../album';

@Component({
  selector: 'app-album-detail',
  templateUrl: './album-detail.component.html',
  styleUrls: ['./album-detail.component.scss'],
})
export class AlbumDetailComponent implements OnInit {
  @Input() album: Album;
  @Output() deleteAlbum = new EventEmitter();

  userId: number;
  token: string;

  constructor(private routerPath: Router, private router: ActivatedRoute) {}

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId);
    this.token = this.router.snapshot.params.userToken;
  }

  goToEdit() {
    this.routerPath.navigate([
      `/albumes/edit/${this.album.id}/${this.userId}/${this.token}`,
    ]);
  }

  goToJoinCancion() {
    this.routerPath.navigate([
      `/albumes/join/${this.album.id}/${this.userId}/${this.token}`,
    ]);
  }

  eliminarAlbum() {
    this.deleteAlbum.emit(this.album.id);
  }

  getDuracion(cancion: Cancion): string {
    // {{ cancion.minutos }}:{{ cancion.segundos }}
    const { minutos = 0, segundos = 0 } = cancion;
    return `${this.getNumeroConCero(minutos)}:${this.getNumeroConCero(
      segundos
    )}`;
  }

  getNumeroConCero(num: number): String {
    return num < 10 ? `0${num}` : num.toString();
  }
}
