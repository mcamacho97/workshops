/* Se puede usar con Array*/
const array = [1, 2, 3, 4, 5];
const otroArray = [6, 7, 8, 9, 10];

//Antes de ECMA6
//const nuevoArray = array.concat(otroArray);

const nuevoArray = [...array, ...otroArray];
console.log(nuevoArray);

/* Se puede usar con objetos*/
const obj1 = {
  a: "a",
  b: "b",
  c: "c",
};

const obj2 = {
  d: "d",
  e: "e",
  f: "f",
};

//Antes de ECMA6
//const nuevoObjeto = Object.assign({}, obj1, obj2);

const nuevoObjeto = {...obj1, ...obj2};
console.log(nuevoObjeto);

//Aplicación con React
const Componente = ({id, ...props}) => {
    return <NuevoComponente key={id} {...props} />
}