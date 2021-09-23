import { CommonModule } from '@angular/common';
import { NgModule } from '@angular/core';
import { DurationTransformPipe } from './duration-pipe.pipe';

@NgModule({
  imports: [CommonModule],
  exports: [DurationTransformPipe],
  declarations: [DurationTransformPipe]
})
export class DurationPipeModule {}
