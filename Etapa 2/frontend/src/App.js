import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import "bootstrap/dist/css/bootstrap.min.css";
import NavBar from "./components/NavBar";
import Predict from "./components/Predict";
import Model from "./components/Retrain";

const App = () => {
  return (
    <Router>
      <div>
        <NavBar />
        <Routes>
          <Route path="/" element={<Predict />} />
          <Route path="/predict" element={<Predict />} />
          <Route path="/retrain" element={<Model />} />
        </Routes>
      </div>
    </Router>
  );
};

export default App;
