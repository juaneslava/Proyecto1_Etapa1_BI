import { Navbar, Nav } from "react-bootstrap";
import { useLocation } from "react-router-dom";
import "./NavBar.css";

const NavBar = () => {
    const location = useLocation();

    return (
        <Navbar bg="dark" variant="dark" expand="lg" className="shadow">
            <Navbar.Brand href="/" style={{ fontWeight: "bold", fontSize: "24px" }}>
                🧠 Inteligencia de Negocios
            </Navbar.Brand>
            <Navbar.Toggle aria-controls="basic-navbar-nav" />
            <Navbar.Collapse id="basic-navbar-nav">
                <Nav className="mx-auto nav">
                    <Nav.Link
                        href="/predict"
                        className={`nav-link ${location.pathname === "/predict" ? "active" : ""}`}
                    >
                        Predicción por Texto
                    </Nav.Link>
                    <span className="separator">|</span>
                    <Nav.Link
                        href="/retrain"
                        className={`nav-link ${location.pathname === "/retrain" ? "active" : ""}`}
                    >
                        Re-entrenar Modelo
                    </Nav.Link>
                </Nav>
            </Navbar.Collapse>
        </Navbar>
    );
};

export default NavBar;
