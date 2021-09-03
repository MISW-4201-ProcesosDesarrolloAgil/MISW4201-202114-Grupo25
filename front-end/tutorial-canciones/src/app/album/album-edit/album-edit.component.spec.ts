/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, DebugElement } from '@angular/core';
import { of } from 'rxjs';

import { AlbumEditComponent } from './album-edit.component';
import { Album, Medio } from '../album';
import {
  FormBuilder,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { AlbumService } from '../album.service';

const mocks = {
  album: new Album(1, 'a', 1, 'abc', new Medio('a', 1), 1, [], []),
};

describe('AlbumEditComponent', () => {
  let component: AlbumEditComponent;
  let fixture: ComponentFixture<AlbumEditComponent>;
  let formBuilder: FormBuilder;

  beforeEach(async(() => {
    const albumService = jasmine.createSpyObj('AlbumService', [
      'getAlbum',
      'editarAlbum',
    ]);
    albumService.getAlbum.and.returnValue(of(mocks.album));
    albumService.editarAlbum.and.returnValue(of(mocks.album));
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
      declarations: [AlbumEditComponent],
      providers: [
        ToastrService,
        { provide: FormBuilder, useValue: formBuilder },
        { provide: AlbumService, useValue: albumService },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlbumEditComponent);
    component = fixture.componentInstance;
    component.albumForm = formBuilder.group({
      titulo: [
        '',
        [
          Validators.required,
          Validators.minLength(1),
          Validators.maxLength(128),
        ],
      ],
      anio: [
        '',
        [Validators.required, Validators.minLength(4), Validators.maxLength(4)],
      ],
      descripcion: [
        '',
        [
          Validators.required,
          Validators.minLength(1),
          Validators.maxLength(512),
        ],
      ],
      medio: ['', [Validators.required]],
    });
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
