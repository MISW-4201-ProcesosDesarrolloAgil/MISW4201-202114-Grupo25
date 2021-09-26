/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, DebugElement } from '@angular/core';
import { of } from 'rxjs';

import { AlbumCreateComponent } from './album-create.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { Album, Medio } from '../album';
import { AlbumService } from '../album.service';
import { FormBuilder, FormsModule, ReactiveFormsModule, Validators } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

const mocks = {
  nuevoAlbum: new Album(1, 'a', 1, 'abc', new Medio('a', 1), 1, [], []),
};

describe('AlbumCreateComponent', () => {
  let component: AlbumCreateComponent;
  let fixture: ComponentFixture<AlbumCreateComponent>;
  let formBuilder: FormBuilder;

  beforeEach(async(() => {
    const albumService = jasmine.createSpyObj('AlbumService', ['crearAlbum']);
    albumService.crearAlbum.and.returnValue(of(mocks.nuevoAlbum));
    formBuilder = new FormBuilder();

    TestBed.configureTestingModule({
      declarations: [AlbumCreateComponent],
      imports: [
        FormsModule,
        HttpClientTestingModule,
        RouterTestingModule,
        ReactiveFormsModule,
        ToastrModule.forRoot(),
        BrowserAnimationsModule,
      ],
      providers: [
        ToastrService,
        { provide: FormBuilder, useValue: formBuilder },
        { provide: AlbumService, useValue: albumService },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AlbumCreateComponent);
    component = fixture.componentInstance;
    component.albumForm = formBuilder.group({
      titulo: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(128)]],
        anio: ["", [Validators.required, Validators.minLength(4), Validators.maxLength(4)]],
        descripcion: ["", [Validators.required, Validators.minLength(1), Validators.maxLength(512)]],
        medio: ["", [Validators.required]]
    });
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
