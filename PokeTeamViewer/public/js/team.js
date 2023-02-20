'use strict';
window.addEventListener('DOMContentLoaded',init);
const cabeceras= {

    'Content-Type': 'application/json',

    'Accept': 'application/json',

  };
function init(){
    mostrarEquipo();
}

function get_images_from_api(pokemon1, poke1, pokemon2, poke2){
    var api = 'https://pokeapi.co/api/v2/pokemon/';
    var p1m = pokemon1.toLowerCase();
    var p2m = pokemon2.toLowerCase();
    var imagen;
    try{
        fetch(api+p1m)
        .then(response => 
            response.json())
        .then(r => {
            if(r.sprites.front_default == null){
                imagen= 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
                poke1.setAttribute("src", imagen);
            }
            else{
                imagen = r.sprites.front_default;
                poke1.setAttribute("src", imagen);
            }
        });
        fetch(api+p2m)
        .then(response => response.json())
        .then(r => {
            if(r.sprites.front_default == null){
                imagen = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
                poke2.setAttribute("src", imagen);
            }
            else{
                imagen = r.sprites.front_default;
                poke2.setAttribute("src", imagen);
            }
        });
    }
    catch(error){
        console.log(error);
    }
    // fetch(api+p1m)
    // .then(response => response.json())
    // .then(r => {
    //     if(r.sprites.front_default == null){
    //         r.sprites.front_default = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
    //     }
    //     else{
    //         imagen = r.sprites.front_default;
    //         poke1.setAttribute("src", imagen);
    //     }
    // });
    // fetch(api+p2m)
    // .then(response => response.json())
    // .then(r => {
    //     if(r.sprites.front_default == null){
    //         r.sprites.front_default = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
    //     }
    //     else{
    //         imagen = r.sprites.front_default;
    //         poke2.setAttribute("src", imagen);
    //     }
    // });

}

function insertarPokemon(pokemon){
    let tabla = document.getElementById("table_team");
    let tr = document.createElement("tr");
    let mote1 = document.createElement('th')
    let poke1 = document.createElement('th')
    let separacion = document.createElement('th')
    let poke2 = document.createElement('th')
    let mote2 = document.createElement('th')
    
    poke1.setAttribute("id", 'poke_image');
    poke2.setAttribute("id", 'poke_image');

    mote1.innerHTML = pokemon.Mote_1;
    mote2.innerHTML = pokemon.Mote_2;

    get_images_from_api(pokemon.Pokemon_1, poke1,pokemon.Pokemon_2, poke2);

    tr.appendChild(mote1);
    tr.appendChild(poke1);
    tr.appendChild(separacion);
    tr.appendChild(poke2);
    tr.appendChild(mote2);
}

function mostrarEquipo(){
    const request = {
        method: 'GET',
        headers: cabeceras,
    };
    var url = window.location.href;
    var equipo_str = url.substring(url.lastIndexOf('=')+1);
    var equipo = equipo_str.split('_');
    for(var i= 0; i<equipo.length; i++){
        fetch('/datosEquipo/'+equipo[i], request)
        .then(response => response.json())
        .then(r => {
            let error = r.error;
            if (error == null){
                let datos = r.result[0];
                insertarPokemon(datos);
            }
            else{
                console.log(error);
            }
        })
    }
}
