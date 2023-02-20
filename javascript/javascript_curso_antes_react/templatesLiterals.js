/* Template literals */
const nombre = "Mauricio";
const apellido = "Camacho";

console.log(`${nombre} ${apellido}`);

//Aplicación a React 
const Componente = ({backgroudColor}) => {
    return (
        <div className ={`bg-color-${}`}>Hola</div>
    )
}