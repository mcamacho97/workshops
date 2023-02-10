const user = {
  nombre: "Mauricio",
  edad: 25,
  location: {
    x: 10912192.12,
    y: 12121234.23,
    city: {
      zipcode: "12121212",
      ldl: "ASASA",
    },
  },
};

const zipcode = user?.location?.city?.zipcode;

console.log(zipcode);
