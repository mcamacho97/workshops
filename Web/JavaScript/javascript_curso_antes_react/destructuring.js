const cuadrado = {
  x: 10,
  y: 10,
};

const calcularArea = ({ x, y }) => {
  //const { x, y } = cuadrado;
  return console.log(x * y);
};

calcularArea(cuadrado);

//Aplicación en react
const Avatar = ({ username, url }) => {
  return <img src={url} alt={username} />;
};
