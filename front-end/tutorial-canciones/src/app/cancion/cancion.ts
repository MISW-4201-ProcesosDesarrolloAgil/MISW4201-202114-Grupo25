export class Cancion {
    id: number;
    titulo: string;
    minutos: number;
    segundos: number;
    interprete: string;
    id_usuario: number;
    albumes: Array<any>;
    compartida: boolean;

    constructor(
        id: number,
        titulo: string,
        minutos: number,
        segundos: number,
        interprete: string,
        id_usuario: number,
        albumes: Array<any>,
        compartida: boolean
    ){
        this.id = id;
        this.titulo = titulo;
        this.minutos = minutos;
        this.segundos = segundos;
        this.interprete = interprete;
        this.id_usuario = id_usuario;
        this.albumes = albumes;
        this.compartida = compartida;
    }
}
