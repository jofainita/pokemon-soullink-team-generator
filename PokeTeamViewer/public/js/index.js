'use strict';
window.addEventListener('DOMContentLoaded',init);
const cabeceras= {

    'Content-Type': 'application/json',

    'Accept': 'application/json',

  };
function init(){
    mostrarRutas();
}

function updateTable(event){
    let tr = event.target.parentNode.parentNode;
    let check = event.target;
    if(check.checked){
        check.readOnly = true;
        check.disabled = true;
    }
    let tipo = tr.getAttribute("tipo");
    const request = {
        method: 'GET',
        headers: cabeceras,
    };
    fetch('/incompatibles/'+tipo, request)
    .then(response => response.json())
    .then(r => {
        let error = r.error;
        if (error == null){
            let incompatibles = r.result[0].incompatibles;
            let tabla = document.getElementById("table_inicial");
            let filas = tabla.getElementsByTagName("tr");
            for(let i= 0; i<filas.length; i++){
                let tipo_fila = filas[i].getAttribute("tipo");
                if((incompatibles.includes(' '+tipo_fila+',' ) | incompatibles.includes('['+tipo_fila+',') 
                | incompatibles.includes(' '+tipo_fila+']'))
                & (filas[i] != tr)){
                    filas[i].style.display = "none";
                }
            }
        }
        else{
            console.log(error);
        }
    })
}

function insertarRuta(ruta){
    let tabla = document.getElementById("table_inicial");
    let tr = document.createElement("tr");
    tr.setAttribute("tipo", ruta.Id_Tipo);
    tr.setAttribute("table-id", ruta.id);
    let Localizacion = document.createElement('th')
    let Mote_1 = document.createElement('th')
    let Pokemon_1 = document.createElement('th')
    let Tipo_1 = document.createElement('th')
    let Mote_2 = document.createElement('th')
    let Pokemon_2 = document.createElement('th')
    let Tipo_2 = document.createElement('th')
    let Combinacion = document.createElement('th')
    let sitio_check = document.createElement('th')
    let check = document.createElement('input')
    check.addEventListener('change',updateTable,false);
    check.type = "checkbox"
    sitio_check.appendChild(check)
    Localizacion.innerHTML = ruta.Ruta;
    Mote_1.innerHTML = ruta.Mote_1;
    Pokemon_1.innerHTML = ruta.Pokemon_1;
    Tipo_1.innerHTML = ruta.Tipo_1;
    Tipo_1.setAttribute("id", ruta.Tipo_1)
    Mote_2.innerHTML = ruta.Mote_2;
    Pokemon_2.innerHTML = ruta.Pokemon_2;
    Tipo_2.innerHTML = ruta.Tipo_2;
    Tipo_2.setAttribute("id", ruta.Tipo_2)
    Combinacion.innerHTML = ruta.Id_Tipo;
    tr.appendChild(Localizacion);
    tr.appendChild(Mote_1);
    tr.appendChild(Pokemon_1);
    tr.appendChild(Tipo_1);
    tr.appendChild(Mote_2);
    tr.appendChild(Pokemon_2);
    tr.appendChild(Tipo_2);
    tr.appendChild(Combinacion);
    tr.appendChild(sitio_check);
    tabla.appendChild(tr);
}

async function mostrarRutas(){
    const request = {
        method: 'GET',
        headers: cabeceras,
    };
    fetch('/allRoutes', request)
    .then(response => response.json())
    .then(r => {
        let error = r.error;
        if (error == null){
            for(let i= 0; i<r.result.routes.length; i++){
                insertarRuta(r.result.routes[i]);
            }
        }
        else{
            console.log(error);
        }
    })
}

//funcion que guarda un equipo y lo abre en otra página
function getTeam(){
    let table = document.getElementById("table_inicial");
    let filas = table.getElementsByTagName("tr");
    let uri = "";
    for(let i= 1; i<filas.length; i++){
        let check = filas[i].getElementsByTagName("input")[0];
        if(check.checked){
            let ruta = filas[i].getAttribute("table-id");
            uri += ruta + "_";
        }
    }
    if(uri != ""){
        uri = uri.substring(0,uri.length-1);
        window.open("/team.html?team="+uri);
    }
}
