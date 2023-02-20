/* Shorthand Property names */
const nombre = "Mauricio";
const edad  = 25;
const pais = "Nicaragua";

const persona = {
    nombre: nombre,
    edad: edad,
    pais: pais
}

console.log(persona);


//Aplicación a React 
const componente = (initialState, totalCount) => {
    const [state, setState] = useState({initialState, totalCount})
}