var config = {}
config.main= {
    base: '',
    port: 5000
  }


config.localbd= {
client: "sqlite3",
connection: {
    filename: "./poke_database.db"
},
useNullAsDefault: true
}
module.exports = config;