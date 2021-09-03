/* tslint:disable:no-unused-variable */
import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { By } from '@angular/platform-browser';
import { CUSTOM_ELEMENTS_SCHEMA, DebugElement } from '@angular/core';

import { CancionListComponent } from './cancion-list.component';
import { HttpClientTestingModule } from '@angular/common/http/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrModule, ToastrService } from 'ngx-toastr';
import { AppHeaderModule } from 'src/app/app-header/app-header.module';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';

describe('CancionListComponent', () => {
  let component: CancionListComponent;
  let fixture: ComponentFixture<CancionListComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [CancionListComponent],
      imports: [
        HttpClientTestingModule,
        RouterTestingModule,
        ToastrModule.forRoot(),
        AppHeaderModule,
        BrowserAnimationsModule
      ],
      providers: [ToastrService],
      schemas: [CUSTOM_ELEMENTS_SCHEMA]
    }).compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CancionListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
