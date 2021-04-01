var columnas = 5;
var filas = 5;
var mapa;
var met;
var inici;
var listaAbierta;
var listaCerrada;

function nodoMinimaF(lista) {
    indiceMinima = 0; //suponemos que está en el primero
    for (var i = 0; i < lista.length; i++) {
        if (lista[i].f < lista[indiceMinima].f) {
            indiceMinima = i;
        }
    }

    return lista[indiceMinima];
}

function eliminarDeArray(nodo, lista) {
    for (var i = lista.length - 1; i >= 0; i--) {
        if (lista[i] === nodo) {
            lista.splice(i, 1);
        }
    }
}

function distancia(nodo1, nodo2) {
    return Math.sqrt(Math.pow((nodo2.i - nodo1.i), 2) + Math.pow((nodo2.j - nodo1.j), 2));
}

function busquedaArray(lista, elem) {
    for (var i = 0; i < lista.length; i++) {
        if (lista[i] === elem) {
            return true;
        }
    }

    return false;
}

function nodo(i, j) {
    this.i = i;
    this.j = j;
    this.g = 0;
    this.h = 0;
    this.f = 0;
    this.hijos = [];
    this.padre;
    this.expandir = function () {
        var i = this.i;
        var j = this.j;
        // falta comprobar que no son obstaculos o padre
        if (i > 0) {
            if (mapa[i - 1][j] === undefined) {
                mapa[i - 1][j] = new nodo(i - 1, j); //calculo aquila f, g y h?
            }
            this.hijos.push(mapa[i - 1][j]);
        }
        if (i > 0 && j > 0) {
            if (mapa[i - 1][j - 1] === undefined) {
                mapa[i - 1][j - 1] = new nodo(i - 1, j - 1);
            }
            this.hijos.push(mapa[i - 1][j - 1]);
        }
        if (j > 0) {
            if (mapa[i][j - 1] === undefined) {
                mapa[i][j - 1] = new nodo(i, j - 1);
            }
            this.hijos.push(mapa[i][j - 1]);
        }
        if (j > 0 && i < columnas - 1) {
            if (mapa[i + 1][j - 1] === undefined) {
                mapa[i + 1][j - 1] = new nodo(i + 1, j - 1);
            }
            this.hijos.push(mapa[i + 1][j - 1]);
        }
        if (i < columnas - 1) {
            if (mapa[i + 1][j] === undefined) {
                mapa[i + 1][j] = new nodo(i + 1, j);
            }
            this.hijos.push(mapa[i + 1][j]);
        }
        if (j < filas - 1 && i < columnas - 1) {
            if (mapa[i + 1][j + 1] === undefined) {
                mapa[i + 1][j + 1] = new nodo(i + 1, j + 1);
            }
            this.hijos.push(mapa[i + 1][j + 1]);
        }
        if (j < filas - 1) {
            if (mapa[i][j + 1] === undefined) {
                mapa[i][j + 1] = new nodo(i, j + 1);
            }
            this.hijos.push(mapa[i][j + 1]);
        }
        if (j < filas - 1 && i > 0) {
            if (mapa[i - 1][j + 1] === undefined) {
                mapa[i - 1][j + 1] = new nodo(i - 1, j + 1);
            }
            this.hijos.push(mapa[i - 1][j + 1]);
        }


    }

}

function inicializarMapa(cols, fils, pos_inicio, pos_meta) {
    listaAbierta = [];
    listaCerrada = [];
    inicio_i = pos_inicio[1]; //me las pasa al reves
    inicio_j = pos_inicio[0]; //me las pasa al reves
    fin_i = pos_meta[0];
    fin_j = pos_meta[1];
    columnas = cols;
    filas = fils;
    mapa = new Array(columnas);
    for (var i = 0; i < columnas; i++) {
        mapa[i] = new Array(filas);
    }
    //creo el nodo inicial
    inici = new nodo(inicio_i, inicio_j);
    mapa[inicio_i][inicio_j] = inici;
    //creo el nodo meta
    met = new nodo(fin_i, fin_j);
    mapa[fin_i][fin_j] = met;
    //añado el nodo inicial a listaAbierta
    listaAbierta.push(inici);
    //añado h y f al nodo inicio
    inici.h = distancia(inici, met);
    inici.f = inici.g + inici.h;

    buscarCamino();



}

function buscarCamino() {
    var fallo = false,
        fin = false,
        m;
    while (!(fallo || fin)) {
        if (listaAbierta.length <= 0) {
            fallo = true;
        }
        m = nodoMinimaF(listaAbierta);
        //console.log(m);
        eliminarDeArray(m, listaAbierta);
        listaCerrada.push(m);

        if (m === met) {
            fin = true;
            console.log("VAMOOOOOOOOS");
        }

        m.expandir();

        for (var i = 0; i < m.hijos.length; i++) {
            var hijo = m.hijos[i];
            var nuevaDistancia = m.g + distancia(m, hijo);
            if (busquedaArray(listaAbierta, hijo)) {
                if (nuevaDistancia < hijo.g) {
                    hijo.g = nuevaDistancia;
                    hijo.f = hijo.g + hijo.h;
                    hijo.padre = m;
                }
            } else if (busquedaArray(listaCerrada, hijo)) {
                if (nuevaDistancia < hijo.g) {
                    //cambiar la g, el padre y hacer recorrido en profundidad de sus hijos
                }
            } else { //no está ni en abierta ni en cerrada
                hijo.g = m.g + distancia(m, hijo);
                hijo.h = distancia(hijo, met);
                hijo.f = hijo.g + hijo.h;
                hijo.padre = m;
                listaAbierta.push(hijo);
            }

        }
        /*console.log(mapa);
        console.log(m);
        console.log(listaAbierta);
        console.log(listaCerrada);*/

    }

    if(fin){
        //función que nos muestre el camino optimo 
    }

    /*console.log("metaaaaaaaaaaa");
    console.log(met);*/

}