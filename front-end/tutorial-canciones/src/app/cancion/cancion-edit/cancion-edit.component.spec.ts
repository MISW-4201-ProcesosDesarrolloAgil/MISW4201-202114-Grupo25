/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, DebugElement } from '@angular/core';
import { of } from 'rxjs';

import { CancionEditComponent } from './cancion-edit.component';
import { Cancion } from 'src/app/album/album';
import { CancionService } from '../cancion.service';
import {
  FormBuilder,
  FormsModule,
  ReactiveFormsModule,
  Validators,
} from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('CancionEditComponent', () => {
  let component: CancionEditComponent;
  let fixture: ComponentFixture<CancionEditComponent>;
  let formBuilder: FormBuilder;

  const mocks = {
    cancion: new Cancion(1, 'a', 1, 1, 'a'),
  };

  beforeEach(async(() => {
    const cancionService = jasmine.createSpyObj('CancionService', [
      'getCancion',
      'editarCancion',
    ]);
    cancionService.getCancion.and.returnValue(of(mocks.cancion));
    cancionService.editarCancion.and.returnValue(of(mocks.cancion));

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
      declarations: [CancionEditComponent],
      providers: [
        ToastrService,
        { provide: FormBuilder, useValue: formBuilder },
        { provide: CancionService, useValue: cancionService },
      ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CancionEditComponent);
    component = fixture.componentInstance;
    component.cancionForm = formBuilder.group({
      titulo: ['', [Validators.required, Validators.maxLength(128)]],
      minutos: [
        '',
        [
          Validators.required,
          Validators.pattern('^[0-9]*$'),
          Validators.maxLength(2),
        ],
      ],
      segundos: [
        '',
        [
          Validators.required,
          Validators.pattern('^[0-9]*$'),
          Validators.maxLength(2),
        ],
      ],
      interprete: ['', [Validators.required, Validators.maxLength(128)]],
    });
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
