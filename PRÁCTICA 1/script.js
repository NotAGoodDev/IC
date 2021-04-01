let rows;
let columns;
let penalizacion;
let inicio;
let meta;
let obstaculos;
let click;

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
        penalizacion += 1
        cambiarPenalizacion()
    })

    $("#bajarPenalizacion").click(function () {
        if (penalizacion > 1) {
            penalizacion -= 1
            cambiarPenalizacion()
        } else {
            alert("La penalizacion no puede ser menor a 1")
        }
    })

    $("#inicio").click(function () {
        activarBoton("inicio");

        $("[id^=elem]").click(function () {
            let posicion = this.id.replace("elem", "");

            if (posicion == meta || obstaculos.includes(posicion)) {
                console.log("Ocupada")
                // console.log("Inicio: " + inicio + "\n" + "Meta: " + meta + "\n" + "Obstaculos: " + obstaculos)

            } else {
                if (click["inicio"]) {
                    if (inicio)
                        limpiarCasilla(inicio)

                    $("#" + this.id).css("background-color", "#304ffe").text("Inicio")
                    // console.log(posicionMatricial(posicion))
                    inicio = posicion;
                    inicializarMapa(columns, rows, posicionMatricial(posicion), [4,2]);// como le pasamos a la vez el inicio y el fin
                }
            }
        })
    })

    $("#meta").click(function () {
        activarBoton("meta");

        $("[id^=elem]").click(function () {
            let posicion = this.id.replace("elem", "");

            if (posicion == inicio || obstaculos.includes(posicion)) {
                console.log("Ocupada")
                // console.log("Inicio: " + inicio + "\n" + "Meta: " + meta + "\n" + "Obstaculos: " + obstaculos)

            } else {
                if (click["meta"]) {
                    if (meta)
                        limpiarCasilla(meta)

                    $("#" + this.id).css("background-color", "#00c853").text("Meta")
                    // console.log(posicionMatricial(posicion))
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
                    if (obstaculos.includes(posicion)) {
                        posArray = obstaculos.indexOf(posicion);
                        limpiarCasilla(obstaculos[posArray])

                        obstaculos.splice(posArray, 1)
                    }
                    else {
                        $("#" + this.id).css("background-color", "#dd2c00").text("!")
                        // console.log(posicionMatricial(posicion))
                        obstaculos.push(posicion)
                    }
                }
            }
        })
    })
})

function print() {

    reset()

    $(".elem").remove()

    for (let row = 1; row <= rows; row++) {

        for (let column = 1; column <= columns; column++) {
            actualElement = posicionLineal(row, column);
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
    $("#buscar")
        .after('<h3 class="penalizacion">Penalizacion: ' + penalizacion + '</h3>')
}

function posicionLineal(row, column) {
    return columns * (row - 1) + column;
}

function posicionMatricial(position) {
    position -= 1
    let x = Math.floor((position / rows))
    let y = (position) % columns

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