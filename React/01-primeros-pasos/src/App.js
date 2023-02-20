import logo from "./logo.svg";
import "./App.css";
import MiComponente from "./components/MiComponente";
import { SegundoComponente } from "./components/SegundoComponente";
import { TercerComponente } from "./components/TercerComponente";
import { EventosComponentes } from "./components/EventosComponentes";

function App() {
  const fichaMedica = {
    altura: "172cm",
    grupo: "A+",
    estado: "Bueno",
    alergia: "Polvo",
  };
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>Bienvenido al master en react!</p>
        <div className="componentes">
          <hr />
          <EventosComponentes />
          <hr />
          <TercerComponente ficha={fichaMedica} />
          <hr />
          <SegundoComponente />
          <hr />
          <MiComponente />
        </div>
      </header>
    </div>
  );
}

export default App;
