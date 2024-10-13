import { Button, Form, Container, Card } from "react-bootstrap";
import React, { useState, useEffect } from "react";
import axios from "axios";

const Retrain = () => {
    const [f1, setF1] = useState(0);
    const [recall, setRecall] = useState(0);
    const [precision, setPrecision] = useState(0);
    const [file, setFile] = useState(null);
    const [isUploading, setIsUploading] = useState(false);

    const fetchMetrics = async () => {
        try {
            const metrics = await axios.get(`http://127.0.0.1:8000/report`);
            const obj = metrics.data;
            setF1(obj.f1);
            setRecall(obj.recall);
            setPrecision(obj.precision);
        } catch (error) {
            console.error("Error fetching metrics:", error);
            alert("Error al obtener métricas. Revisa la consola para más detalles.");
        }
    };

    const handleFileChange = (e) => {
        setFile(e.target.files ? e.target.files[0] : null);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (file) {
            setIsUploading(true);
            const formData = new FormData();
            formData.append("file", file);

            try {
                await axios.post(
                    "http://127.0.0.1:8000/retrain",
                    formData,
                    {
                        headers: {
                            "Content-Type": "multipart/form-data",
                        },
                    }
                );
                fetchMetrics();
            } catch (error) {
                console.error("Error uploading file:", error);
                alert("Error en el reentrenamiento. Por favor, revisa la consola para más detalles.");
            } finally {
                setIsUploading(false);
            }
        }
    };

    useEffect(() => {
        fetchMetrics();
    }, []);

    return (
        <Container style={{ maxWidth: "600px", margin: "0 auto", textAlign: "center" }}>
            <Card className="mb-4" style={{ border: '2px solid #007bff' }}>
                <Card.Body>
                    <Card.Title style={{ fontWeight: "bold", fontSize: "24px", color: "#007bff" }}>
                        🚀 Estadísticas del Modelo 🚀
                    </Card.Title>
                    <Card.Text style={{ fontSize: "18px", margin: "20px 0" }}>
                        Aquí tienes un resumen de las métricas de rendimiento de tu modelo:
                    </Card.Text>
                    <div style={{ textAlign: "left", padding: "10px" }}>
                        <p style={{ fontWeight: "bold" }}>
                            🌟 Precisión: {precision.toFixed(4) * 100}%
                        </p>
                        <p style={{ fontWeight: "bold" }}>
                            🎯 Recall: {recall.toFixed(4) * 100}%
                        </p>
                        <p style={{ fontWeight: "bold" }}>
                            🥇 Puntaje F1: {f1.toFixed(4) * 100}%
                        </p>
                    </div>
                </Card.Body>
            </Card>

            <Card>
                <Card.Body>
                    <Card.Title style={{ fontWeight: "bold", fontSize: "24px", color: "#28a745" }}>
                        📁 Reentrenar Tu Modelo 📁
                    </Card.Title>
                    <Card.Text style={{ fontSize: "18px", margin: "10px 0" }}>
                        Carga un archivo CSV o XLSX para iniciar el reentrenamiento:
                    </Card.Text>
                    <Form onSubmit={handleSubmit}>
                        <Form.Group controlId="formFile" className="mb-3">
                            <Form.Control type="file" onChange={handleFileChange} />
                        </Form.Group>
                        <Button
                            variant={isUploading ? "danger" : "success"}
                            type="submit"
                            disabled={!file || isUploading}
                        >
                            {isUploading ? "Cargando..." : "Enviar"}
                        </Button>
                    </Form>
                </Card.Body>
            </Card>
        </Container>
    );
};

export default Retrain;