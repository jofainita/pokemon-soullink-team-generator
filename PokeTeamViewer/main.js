'use strict';
// carga y ejecuta config.js
const config = require('./config.js');
const express = require('express');
const app = express();
var knex = null;
const path = require('path');
const publico = path.join(__dirname, 'public');
app.use(express.static(publico));
const PORT = 5000;
app.listen(PORT, function () {
  console.log(`Aplicación lanzada en el puerto ${ PORT }!`);
});
app.get(config.main.base+'/ayuda', (req, res) => res.sendFile(path.join(publico, 'index.html')));
app.use('/', express.static(publico));
app.use(async(req, res, next) => {
    conecta_db();
    next();});

function conecta_db(){
    var options = config.localbd;
    options.debug = true;
    knex = require('knex')(options);
}

// convierte el cuerpo del mensaje de la petición en JSON al objeto de JavaScript req.body:
app.use(express.json());

// middleware para descodificar caracteres UTF-8 en la URL:
app.use( (req, res, next) => {
  req.url = decodeURI(req.url);
  next();
});

// middleware para las cabeceras de CORS:
app.use( (req, res, next) => {
  res.header("Access-Control-Allow-Origin", "*");
  res.header('Access-Control-Allow-Methods', 'DELETE, PUT, GET, POST, OPTIONS');
  res.header("Access-Control-Allow-Headers", "content-type");
  next();
});

// sacar toda la info de las rutas
app.get(config.main.base+'/allRoutes', async (req, res) => {
    try{
        let routes = await knex('Datos_base').select();
        res.status(200).send({result: {routes}, error: null});
    }catch(err){
        res.status(500).json({result: none ,error: err.message});
    }
});

// sacar los incompatibles para un tipo
app.get(config.main.base+'/incompatibles/:tipo', async (req, res) => {
    try{
        let incompatibles = await knex('Incompatible').select('incompatibles').where('Tipo',req.params.tipo);
        res.status(200).send({result: incompatibles, error: null});
    }catch(err){
        res.status(500).json({result: none ,error: err.message});
    }
});

