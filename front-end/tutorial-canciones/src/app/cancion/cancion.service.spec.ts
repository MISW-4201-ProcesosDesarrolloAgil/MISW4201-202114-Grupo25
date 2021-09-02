/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { CancionService } from './cancion.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('Service: Cancion', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [CancionService],
      imports: [HttpClientTestingModule]
    });
  });

  it('should ...', inject([CancionService], (service: CancionService) => {
    expect(service).toBeTruthy();
  }));
});
