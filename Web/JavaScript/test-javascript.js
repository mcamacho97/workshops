const a = "Hey";

const global = () => {
  let b = "¿Qué";
  const local = () => {
    let c = "Tal?";
    return a + b + c;
  };
  return local();
};

console.log(global());
