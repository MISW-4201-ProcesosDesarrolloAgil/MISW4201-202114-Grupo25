/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { AlbumService } from './album.service';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('Service: Album', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AlbumService],
      imports: [HttpClientTestingModule]
    });
  });

  it('should ...', inject([AlbumService], (service: AlbumService) => {
    expect(service).toBeTruthy();
  }));
});
