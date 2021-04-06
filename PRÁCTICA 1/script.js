let rows;
let columns;
let penalizacion;
let inicio;
let meta;
let obstaculos;
let click;
let solucion;

$(function () {
    rows = 5;
    columns = 5;

    print();
    cambiarPenalizacion()

    $("#aniadirFila").click(function () {
        rows < 7 ? rows += 1 : alert("Demasiadas filas")
        print()
    })

    $("#aniadirColumna").click(function () {
        columns < 10 ? columns += 1 : alert("Demasiadas columnas")
        print()
    })

    $("#eliminarFila").click(function () {
        rows > 2 ? rows -= 1 : alert("No se puede poner menos filas")
        print()
    })

    $("#eliminarColumna").click(function () {
        columns > 2 ? columns -= 1 : alert("No se puede poner menos columnas")
        print()
    })

    $("#subirPenalizacion").click(function () {
        if (penalizacion == Infinity) {
            penalizacion = 1
        }
        else {
            penalizacion += 1
        }

        cambiarPenalizacion()
    })

    $("#bajarPenalizacion").click(function () {

        if (penalizacion > 1) {
            penalizacion -= 1
        } else {
            alert("Los obstáculos ahora son inaccesibles");
            penalizacion = Infinity
        }

        cambiarPenalizacion()
    })

    $("#inicio").click(function () {
        activarBoton("inicio");

        $("[id^=elem]").click(function () {
            let posicion = this.id.replace("elem", "");

            if (posicion == meta || posicionArrayObstaculo(posicion) != -1) {
                console.log("Ocupada")
                // console.log("Inicio: " + inicio + "\n" + "Meta: " + meta + "\n" + "Obstaculos: " + obstaculos)

            } else {
                if (click["inicio"]) {
                    if (inicio)
                        limpiarCasilla(inicio)

                    $("#" + this.id).css("background-color", "#304ffe").text("Inicio")
                    console.log(posicionMatricial(posicion))
                    inicio = posicion;
                }
            }
        })
    })

    $("#meta").click(function () {
        activarBoton("meta");

        $("[id^=elem]").click(function () {
            let posicion = this.id.replace("elem", "");

            if (posicion == inicio || posicionArrayObstaculo(posicion) != -1) {
                console.log("Ocupada")
                console.log("Inicio: " + inicio + "\n" + "Meta: " + meta + "\n" + "Obstaculos: " + obstaculos)

            } else {
                if (click["meta"]) {
                    if (meta)
                        limpiarCasilla(meta)

                    $("#" + this.id).css("background-color", "#f4511e").text("Meta")
                    console.log(posicionMatricial(posicion))
                    meta = posicion;
                }
            }
        })
    })

    $("#obstaculos").click(function () {
        activarBoton("obstaculos");

        $("[id^=elem]").click(function () {
            let posicion = this.id.replace("elem", "");

            if (posicion == inicio || posicion == meta) {
                console.log("Ocupada")
                // console.log("Inicio: " + inicio + "\n" + "Meta: " + meta + "\n" + "Obstaculos: " + obstaculos)

            } else {
                if (click["obstaculos"]) {

                    posArray = posicionArrayObstaculo(posicion);

                    if (posArray != -1) {   //Limpiar casillas
                        let obstaculo = obstaculos[posArray];
                        limpiarCasilla(posicionLineal(obstaculo.x + 1, obstaculo.y + 1));

                        obstaculos.splice(posArray, 1)
                    }
                    else {  //Crear objeto obstaculo e insertar en array
                        if (penalizacion == Infinity || penalizacion == "∞")
                            $("#" + this.id).css("background-color", "#ffd600").text("∞");
                        else {
                            $("#" + this.id).css("background-color", "#ffd600").text(penalizacion);
                        }

                        posicion = posicionMatricial(posicion)
                        obstaculos.push({
                            x: posicion[0],
                            y: posicion[1],
                            penalizacion: penalizacion
                        })
                    }
                }
            }
        })
    })


    $("#buscar").click(function () {

        //¿Esta todo definido?
        if (columns != undefined && rows != undefined
            && inicio != undefined && meta != undefined) {

            //Limpiar soluciones anteriores
            if (solucion != undefined) {
                solucion.forEach(celda => {
                    let posArray = posicionArrayObstaculo(posicionLineal(celda.x + 1, celda.y + 1));
                    let posicion = posicionLineal(celda.x + 1, celda.y + 1);

                    if (posArray != -1) {

                        if (obstaculos[posArray].penalizacion == Infinity)
                            $("#elem" + posicion).css("background-color", "#ffd600").text("∞");
                        else if (obstaculos[posArray].penalizacion > 0) {
                            $("#elem" + posicion).css("background-color", "#ffd600").text(penalizacion);
                        } else {
                            limpiarCasilla(posicion);
                        }
                    }
                    else {
                        limpiarCasilla(posicion);
                    }
                });
            }

            //Creamos el mapa
            inicializarMapa(
                columns,
                rows,
                posicionMatricial(inicio),
                posicionMatricial(meta),
                obstaculos
            );


            solucion = buscarCamino();

            if (solucion == null) {
                alert("No hay un camino posible");
            }
            else if (solucion.length > 0) {
                pintarCamino(solucion);
            } else if (solucion.length == 0) {
                alert("Las celdas son contiguas, no se puede dibujar el camino");

            }
            else {
                alert("No has establecido un inicio y un final");
            }
        }
    })
})

function print() {

    reset()

    $(".elem").remove()

    for (let row = 1; row <= rows; row++) {

        for (let column = 1; column <= columns; column++) {
            actualElement = posicionLineal(column, row);
            $(".tabla")
                .append('<div id="elem' + actualElement + '" class="elem"></div>')

            $("#elem" + actualElement)
                .css("grid-row", row)
                .css("grid-column", column)
        }
    }

    cambiarPenalizacion()
}

function reset() {

    inicio = undefined;
    meta = undefined;
    obstaculos = [];

    click = [];
    click["inicio"] = false;
    click["meta"] = false;
    click["obstaculos"] = false;

    penalizacion = 1;
}

function cambiarPenalizacion() {
    $(".penalizacion").remove()

    if (penalizacion != Infinity) {
        $("#buscar")
            .after('<h3 class="penalizacion">Penalizacion: ' + penalizacion + '</h3>')
    } else {
        $("#buscar")
            .after('<h3 class="penalizacion">Penalizacion: ∞</h3>')
    }
}

function posicionLineal(column, row) {
    return columns * (row - 1) + column;
}

function posicionMatricial(position) {
    position -= 1
    let x = (position) % columns
    let y = Math.floor((position / columns))

    return [x, y];
}

function limpiarCasilla(posicion) {
    $("#elem" + posicion).css("background-color", "#8c9eff").text("")
}

function activarBoton(boton) {
    click["inicio"] = false;
    click["meta"] = false;
    click["obstaculos"] = false;

    click[boton] = true;    //Todo a false y después el boton a true


    $("#inicio").css("background-color", "#b2dfdb");
    $("#meta").css("background-color", "#b2dfdb");
    $("#obstaculos").css("background-color", "#b2dfdb");

    $("#" + boton).css("background-color", "#4db6ac");      //Todo normal y después el boton distinto
}

function pintarCamino(nodos) {

    for (let i = 0; i < nodos.length; i++) {
        let posicion = posicionLineal(nodos[i].x + 1, nodos[i].y + 1);

        setTimeout(function () {
            $("#elem" + posicion).css("background-color", "#7cb342").text("");
        }, 500 * i);
    }
}

function posicionArrayObstaculo(posicion) {
    let posArray = -1;
    let obj = posicionMatricial(posicion);


    obstaculos.forEach((obs, i) => {
        if (obs.x == obj[0]
            && obs.y == obj[1]
            && obs.penalizacion != undefined) {

            posArray = i;
        }
    })

    return posArray;
}