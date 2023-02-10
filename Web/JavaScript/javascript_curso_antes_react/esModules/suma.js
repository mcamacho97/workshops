/*Se utiliza default para exportar unicamente la function que tiene "default"*/
//Si no se usa default, hay que especificar que funciones queremos importar

export const suma = (a, b) => {
  return console.log(a + b);
};

export const otraSuma = (c, d) => {
  return console.log(c + d);
};
