import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  userName: String = '';

  constructor(private routerPath: Router, private router: ActivatedRoute) {}

  ngOnInit(): void {
    const userName = window.sessionStorage.getItem('usuario');
    if (userName) {
      this.userName = userName;
    }
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
