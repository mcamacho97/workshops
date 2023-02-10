const inventario = (nombre) => {
  let _nombre = nombre; //  se utiliza _ por convención en variables privadas
  const _articulos = {};

  const add = (nombre, cantidad) => {
    _articulos[nombre] = cantidad;
  };

  const borrar = (nombre) => {
    delete _articulos[nombre];
  };

  const cantidad = (nombre) => {
    return _articulos[nombre];
  };

  function nombre () {
    return _nombre;
  };

  return {
    add,
    borrar,
    cantidad,
    nombre,
  };
};

const libros = inventario("Libros");
libros.add("El libro de la vida", 3);
console.log(libros.cantidad("El libro de la vida"));