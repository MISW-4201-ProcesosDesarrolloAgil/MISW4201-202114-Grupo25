/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { of } from 'rxjs';
import { CancionCreateComponent } from './cancion-create.component';
import { Cancion } from 'src/app/album/album';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { CancionService } from '../cancion.service';
import { FormBuilder, Validators } from '@angular/forms';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

const mocks = {
  cancion: new Cancion(1, 'a', 1, 1, 'b'),
};

describe('CancionCreateComponent', () => {
  let component: CancionCreateComponent;
  let fixture: ComponentFixture<CancionCreateComponent>;
  let formBuilder: FormBuilder;

  beforeEach(async(() => {
    const cancionService = jasmine.createSpyObj('CancionService', [
      'crearCancion',
    ]);
    cancionService.crearCancion.and.returnValue(of(mocks.cancion));
    formBuilder = new FormBuilder();

    TestBed.configureTestingModule({
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        ToastrModule.forRoot(),
        BrowserAnimationsModule,
      ],
      declarations: [CancionCreateComponent],
      providers: [
        ToastrService,
        { provide: CancionService, useValue: cancionService },
        { provide: FormBuilder, useValue: formBuilder },
      ],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CancionCreateComponent);
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
