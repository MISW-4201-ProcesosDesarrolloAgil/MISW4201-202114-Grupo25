import { Component, OnInit, Input, Output, EventEmitter } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { Cancion } from '../cancion';

@Component({
  selector: 'app-cancion-detail',
  templateUrl: './cancion-detail.component.html',
  styleUrls: ['./cancion-detail.component.scss'],
})
export class CancionDetailComponent implements OnInit {
  @Input() cancion: Cancion;
  @Output() deleteCancion = new EventEmitter();

  userId: number;
  token: string;

  constructor(private router: ActivatedRoute, private routerPath: Router) {}

  ngOnInit() {
    this.userId = parseInt(this.router.snapshot.params.userId);
    this.token = this.router.snapshot.params.userToken;
  }

  eliminarCancion() {
    this.deleteCancion.emit(this.cancion.id);
  }

  goToEdit() {
    this.routerPath.navigate([
      `/canciones/edit/${this.cancion.id}/${this.userId}/${this.token}`,
    ]);
  }

  getDuracion(cancion: Cancion): string {
    // {{ cancion.minutos }}:{{ cancion.segundos }}
    if (!cancion) {
      return '-';
    }
    const { minutos = 0, segundos = 0 } = cancion;
    return `${this.getNumeroConCero(minutos)}:${this.getNumeroConCero(
      segundos
    )}`;
  }

  getNumeroConCero(num: number): String {
    return num < 10 ? `0${num}` : num.toString();
  }
}
