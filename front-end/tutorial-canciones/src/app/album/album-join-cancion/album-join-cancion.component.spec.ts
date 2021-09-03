/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, DebugElement } from '@angular/core';
import { of } from 'rxjs';

import { AlbumJoinCancionComponent } from './album-join-cancion.component';
import { Album, Cancion, Medio } from '../album';
import { AlbumService } from '../album.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import {
  FormBuilder,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { CancionService } from 'src/app/cancion/cancion.service';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

const mocks = {
  album: new Album(1, 'a', 1, 'abc', new Medio('a', 1), 1, [], []),
  cancion: new Cancion(1, 'a', 1, 1, 'b'),
  canciones: [new Cancion(1, 'a', 1, 1, 'b')],
};

describe('AlbumJoinCancionComponent', () => {
  let component: AlbumJoinCancionComponent;
  let fixture: ComponentFixture<AlbumJoinCancionComponent>;
  let formBuilder: FormBuilder;

  beforeEach(async(() => {
    const albumService = jasmine.createSpyObj('AlbumService', [
      'getAlbum',
      'asociarCancion',
    ]);
    albumService.getAlbum.and.returnValue(of(mocks.album));
    albumService.asociarCancion.and.returnValue(of(mocks.cancion));

    const cancionService = jasmine.createSpyObj('AlbumService', [
      'getCanciones',
    ]);
    cancionService.getCanciones.and.returnValue(of(mocks.canciones));
    formBuilder = new FormBuilder();

    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        HttpClientTestingModule,
        RouterTestingModule,
        ReactiveFormsModule,
        ToastrModule.forRoot(),
        BrowserAnimationsModule,
      ],
      declarations: [AlbumJoinCancionComponent],
      providers: [
        ToastrService,
        { provide: FormBuilder, useValue: formBuilder },
        { provide: AlbumService, useValue: albumService },
        { provide: CancionService, useValue: cancionService },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlbumJoinCancionComponent);
    component = fixture.componentInstance;
    component.albumCancionForm = formBuilder.group({
      tituloAlbum: ['', [Validators.required]],
      idCancion: ['', [Validators.required]],
      tituloCancion: ['', [Validators.required]],
    });
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
