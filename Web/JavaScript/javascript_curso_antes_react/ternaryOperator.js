const coche = {
  marca: "tesla",
  model: "S",
};

// let modelo;
// if (coche.model) {
//   modelo.coche.model;
// } else {
//   modelo = "X";
// }

// modelo;

//ternary
let modelo =  coche.model ? coche.model : 'X';

//Aplicación React
const ListaTarea = ({tareas}) =>{
    return  (
        <React.Fragment>
            {tareas.length ? (
                <ul>
                    {tareas.map....}
                </ul>
            ) : (<div>No hay tareas</div>)
            }
        </React.Fragment>
    )
}