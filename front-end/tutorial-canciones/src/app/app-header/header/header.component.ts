import { Component, OnInit, ViewChild } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { ModalComponent } from 'src/app/components/modal/modal.component';
import { ModalConfig } from 'src/app/components/modal/modal.config';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  userName: String = '';
  @ViewChild('modal') private modal: ModalComponent;

  public modalConfig: ModalConfig = {
    modalTitle: 'Acerca de Ionic',
    dismissButtonLabel: 'Aceptar'
  };

  constructor(private routerPath: Router, private router: ActivatedRoute) {}

  ngOnInit(): void {
    const userName = window.sessionStorage.getItem('usuario');
    if (userName) {
      this.userName = userName;
    }
  }

  mostrarCreditos() {
    return this.modal.open();
  }

  goTo(menu: string) {
    const userId = parseInt(this.router.snapshot.params.userId);
    const token = this.router.snapshot.params.userToken;
    if (menu === 'logIn') {
      window.sessionStorage.removeItem('usuario');
      this.routerPath.navigate([`/`]);
    } else if (menu === 'album') {
      this.routerPath.navigate([`/albumes/${userId}/${token}`]);
    } else {
      this.routerPath.navigate([`/canciones/${userId}/${token}`]);
    }
  }
}
