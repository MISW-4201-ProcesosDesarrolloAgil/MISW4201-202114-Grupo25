import { Pipe, PipeTransform } from '@angular/core';
import { Cancion } from 'src/app/album/album';

@Pipe({
  name: 'durationTransform',
})
export class DurationTransformPipe implements PipeTransform {

  getNumeroConCero(num: number): string {
    return num < 10 ? `0${num}` : num.toString();
  }

  transform(cancion: Cancion): string {
    if (!cancion) {
      return '-';
    }
    const { minutos = 0, segundos = 0 } = cancion;
    const minStr = this.getNumeroConCero(minutos);
    const secStr = this.getNumeroConCero(segundos);
    return `${minStr}:${secStr}`;
  }
}
