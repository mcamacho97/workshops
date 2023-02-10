const libro = {
  titulo: "Aprendiendo JavaScript",
  autor: "Carlos Azauste",
  numPaginas: 96,
  editorial: "carlosazaustre.es",
  precio: "17.95",
};

const propiedades = Object.getOwnPropertyNames(libro);

console.log(propiedades);