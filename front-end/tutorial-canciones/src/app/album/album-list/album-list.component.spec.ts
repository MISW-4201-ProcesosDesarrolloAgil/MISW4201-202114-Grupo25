/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, DebugElement } from '@angular/core';
import { of } from 'rxjs';

import { AlbumListComponent } from './album-list.component';
import { Album, Cancion, Medio } from '../album';
import { AlbumService } from '../album.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';

const mocks = {
  albumes: [new Album(1, 'a', 1, 'abc', new Medio('a', 1), 1, [], [])],
  canciones: [new Cancion(1, 'a', 1, 1, 'a')],
};

describe('AlbumListComponent', () => {
  let component: AlbumListComponent;
  let fixture: ComponentFixture<AlbumListComponent>;

  beforeEach(async(() => {
    const albumService = jasmine.createSpyObj('AlbumService', [
      'getAlbumes',
      'getCancionesAlbum',
    ]);
    albumService.getAlbumes.and.returnValue(of(mocks.albumes));
    albumService.getCancionesAlbum.and.returnValue(of(mocks.canciones));

    TestBed.configureTestingModule({
      declarations: [AlbumListComponent],
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        ToastrModule.forRoot(),
      ],
      providers: [
        ToastrService,
        { provide: AlbumService, useValue: albumService },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlbumListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
