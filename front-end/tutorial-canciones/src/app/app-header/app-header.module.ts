import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HeaderComponent } from './header/header.component';
import { ModalModule } from '../components/modal/modal.module';


@NgModule({
  declarations: [ HeaderComponent],
  imports:[CommonModule, ModalModule],
  exports: [HeaderComponent]
})
export class AppHeaderModule { }
