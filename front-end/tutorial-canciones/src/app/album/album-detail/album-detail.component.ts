import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ToastrService } from 'ngx-toastr';
import { AlbumService } from '../album.service';
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

  constructor(
    private routerPath: Router,
    private router: ActivatedRoute,
    private albumService: AlbumService,
    private toastr: ToastrService,
  ) { }

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

  agregarComentario(){
    if (!this.album?.id) {
      return;
    }
    this.albumService.agregarComentario(this.album.id, 'Comentario de Prueba', this.token)
      .subscribe(respuesta => {
        if (respuesta && respuesta.data) {
          this.toastr.success('El comentario fue agregado satisfactoriamente', "Comentario agregado");
          return;
        }
        this.toastr.error('Ocurrió un error agregando el comentario. Intenta de nuevo, por favor.', 'Error al comentar');
      });
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
