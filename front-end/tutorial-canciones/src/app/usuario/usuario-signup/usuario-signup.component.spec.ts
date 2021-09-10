/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { DebugElement } from '@angular/core';
import { of } from 'rxjs';
import { UsuarioSignupComponent } from './usuario-signup.component';
import { FormBuilder, FormsModule, ReactiveFormsModule } from '@angular/forms';
import { AlbumService } from 'src/app/album/album.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { ToastrModule, ToastrService } from 'ngx-toastr';

const mocks = {
  res: {
    token: '123',
  },
};

describe('UsuarioSignupComponent', () => {
  let component: UsuarioSignupComponent;
  let fixture: ComponentFixture<UsuarioSignupComponent>;
  let formBuilder: FormBuilder;

  beforeEach(async(() => {
    const usuarioService = jasmine.createSpyObj('UsuarioService', [
      'userSignUp',
    ]);
    usuarioService.userSignUp.and.returnValue(of(mocks.res));
    formBuilder = new FormBuilder();

    TestBed.configureTestingModule({
      imports: [
        FormsModule,
        HttpClientTestingModule,
        RouterTestingModule,
        ReactiveFormsModule,
        BrowserAnimationsModule,
        ToastrModule.forRoot(),
      ],
      declarations: [UsuarioSignupComponent],
      providers: [
        ToastrService,
        { provide: FormBuilder, useValue: formBuilder },
        { provide: AlbumService, useValue: usuarioService },
      ],
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UsuarioSignupComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
