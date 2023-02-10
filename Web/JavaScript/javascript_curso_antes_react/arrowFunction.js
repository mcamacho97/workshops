//Antes
function nombreDeLaFuncion () {
    return "Hola";
}

//Ahora
const funcionFlecha = () => "Hola"

nombreDeLaFuncion();
funcionFlecha();

//Aplicación en react
function ListaDeTareas () {
    return (
        <ul>
            {listado.map(elemento => (<li>{elemento.nombre}</li>))}
        </ul>
    );
}