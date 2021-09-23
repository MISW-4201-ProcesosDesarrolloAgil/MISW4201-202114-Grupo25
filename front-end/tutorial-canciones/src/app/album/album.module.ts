import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ReactiveFormsModule } from '@angular/forms';
import { AlbumListComponent } from './album-list/album-list.component';
import { AlbumDetailComponent } from './album-detail/album-detail.component';
import { AlbumCreateComponent } from './album-create/album-create.component';
import { AlbumEditComponent } from './album-edit/album-edit.component';
import { AppHeaderModule } from '../app-header/app-header.module';
import { AlbumJoinCancionComponent } from './album-join-cancion/album-join-cancion.component';
import { ModalModule } from '../components/modal/modal.module';
import { DurationPipeModule } from '../components/duration-pipe/duration-pipe.module';

@NgModule({
  declarations: [
    AlbumListComponent,
    AlbumDetailComponent,
    AlbumCreateComponent,
    AlbumEditComponent,
    AlbumJoinCancionComponent,
  ],
  imports: [CommonModule, ReactiveFormsModule, AppHeaderModule, ModalModule, DurationPipeModule],
  exports: [
    AlbumListComponent,
    AlbumDetailComponent,
    AlbumCreateComponent,
    AlbumEditComponent,
    AlbumJoinCancionComponent,
  ],
})
export class AlbumModule {}
