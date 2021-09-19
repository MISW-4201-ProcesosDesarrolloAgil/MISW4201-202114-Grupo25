## MISW4201-202114-Grupo25 


### Configuracion

#### Backend
En el directorio flaskr ejecute los comandos:

```shell
export db_uri='sqlite:///ionic.db'
flask run
```


### Tests
#### Backend
En el directorio principal corra el comando: 
```shell
export db_uri='sqlite:///test.db'
pytest
```

Para realizar un nuevo test dirigase a el ejemplo ubicado en /flaskr/tests/test_ejemplo.py