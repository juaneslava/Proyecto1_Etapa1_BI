import React, { useState } from "react";
import { Button, Form, Container, Table } from "react-bootstrap";
import axios from "axios";

const Predict = () => {
    const [input, setInput] = useState("");
    const [predictions, setPredictions] = useState([]);

    const handleSubmit = async (e) => {
        e.preventDefault();
        const postData = [{
            'Textos_espanol': input,
        }];
        try {
            const response = await axios.post(
                "http://127.0.0.1:8000/predict_input",
                postData
            );
            
            const newPrediction = response.data.predictions[0];
            setPredictions(prevPredictions => [...prevPredictions, newPrediction]);
            setInput(""); 
        } catch (error) {
            console.error("Error fetching prediction:", error);
            alert("Failed to fetch prediction. Check the console for more details.");
        }
    };

    return (
        <Container fluid style={styles.container}>

            <h2 style={styles.title}>Predicción por Texto</h2>

            <Form onSubmit={handleSubmit} style={styles.form}>
                <Form.Group controlId="formText">
                    <Form.Control
                        as="textarea"
                        placeholder="Ingrese el texto que desea clasificar..."
                        rows={2}
                        value={input}
                        onChange={(e) => setInput(e.target.value)}
                        style={styles.textArea}
                    />
                </Form.Group>
                <Button
                    variant={"primary"}
                    type="submit"
                    size="sm"
                    style={styles.button}
                >
                    Clasificar
                </Button>
            </Form>


            <h3 style={styles.subtitle}>Resultados de predicciones:</h3>
            {predictions.length > 0 && (
                <Table striped bordered hover responsive="sm" style={styles.table}>
                    <thead>
                        <tr>
                            <th>#</th>
                            <th style={styles.textColumn}>Texto</th>
                            <th style={styles.smallColumn}>Clase</th>
                            <th style={styles.smallColumn}>Probabilidad</th>
                        </tr>
                    </thead>
                    <tbody>
                        {predictions.map((prediction, index) => (
                            <tr key={index}>
                                <td>{index + 1}</td>
                                <td style={styles.textContent}>{prediction.text}</td>
                                <td>{prediction.prediction}</td>
                                <td>{prediction.score.toFixed(2)}</td>
                            </tr>
                        ))}
                    </tbody>
                </Table>
            )}
        </Container>
    );
};

const styles = {
    container: {
        margin: "20px auto",
        maxWidth: "800px",
        padding: "20px",
        backgroundColor: "#f9f9f9",
        borderRadius: "10px",
        boxShadow: "0 4px 12px rgba(0, 0, 0, 0.1)"
    },
    title: {
        textAlign: "center",
        fontWeight: "bold",
        fontSize: "24px",
        marginBottom: "20px",
        color: "#333"
    },
    form: {
        backgroundColor: "#f1f1f1",
        padding: "15px",
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)",
        marginBottom: "20px"
    },
    textArea: {
        resize: "none",
        fontSize: "14px",
        marginBottom: "10px",
        borderRadius: "5px",
        padding: "10px"
    },
    button: {
        fontSize: "12px",
        padding: "8px 20px",
        fontWeight: "bold",
        display: "block",
        margin: "10px auto 0 auto",
        borderRadius: "5px",
        width: "auto"
    },
    subtitle: {
        textAlign: "center",
        fontSize: "20px",
        marginBottom: "20px",
        color: "#666"
    },
    table: {
        fontSize: "14px",
        textAlign: "center",
        backgroundColor: "#fff",
        borderRadius: "10px",
        boxShadow: "0 4px 8px rgba(0, 0, 0, 0.1)"
    },
    textColumn: {
        width: "60%",
        textAlign: "left",
    },
    smallColumn: {
        width: "10%",
    },
    textContent: {
        wordBreak: "break-word",
        whiteSpace: "pre-wrap",
    }
};

export default Predict;
