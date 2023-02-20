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
    var imagen_1 = document.createElement('img');
    var imagen_2 = document.createElement('img');
    var imagen;
    try{
        fetch(api+p1m)
        .then(response => 
            response.json())
        .then(r => {
            if(r.sprites.front_default == null){
                imagen= 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
                imagen_1.setAttribute("src", imagen);
                poke1.appendChild(imagen_1);
            }
            else{
                imagen = r.sprites.front_default;
                imagen_1.setAttribute("src", imagen);
                poke1.appendChild(imagen_1);
            }
        });
        fetch(api+p2m)
        .then(response => response.json())
        .then(r => {
            if(r.sprites.front_default == null){
                imagen = 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/0.png';
                imagen_2.setAttribute("src", imagen);
                poke2.appendChild(imagen_2);
            }
            else{
                imagen = r.sprites.front_default;
                imagen_2.setAttribute("src", imagen);
                poke2.appendChild(imagen_2);
                
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
    tabla.appendChild(tr);
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
    var tabla = document.getElementById("table_team");
    var tr = document.createElement("tr");
    var nombre_1 = document.createElement('th')
    var nombre_2 = document.createElement('th')
    var sprite_1 = document.createElement('th')
    var sprite_2 = document.createElement('th')
    var imagen_1 = document.createElement('img');
    var imagen_2 = document.createElement('img');
    var space = document.createElement('th');
    imagen_1.setAttribute("src", 'https://play.pokemonshowdown.com/sprites/trainers/butler.png');
    imagen_2.setAttribute("src", 'https://play.pokemonshowdown.com/sprites/trainers/crasherwake.png');
    sprite_1.appendChild(imagen_1);
    sprite_2.appendChild(imagen_2);
    nombre_1.innerHTML = 'SrIncognito';
    nombre_2.innerHTML = 'Jofainita';
    tr.appendChild(sprite_2);
    tr.appendChild(nombre_2);
    tr.appendChild(space);
    tr.appendChild(nombre_1);
    tr.appendChild(sprite_1);
    tabla.insertBefore(tr, tabla.childNodes[0]);

}
