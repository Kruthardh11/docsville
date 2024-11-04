import React, { useState } from "react";
import axios from "axios";

const DocumentUpload = () => {
    const [file, setFile] = useState(null);
    const [data, setData] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]);
    };

    const handleUpload = async () => {
        const formData = new FormData();
        formData.append("file", file);

        try {
            const response = await axios.post("http://localhost:8000/extract_document_data/", formData, {
                headers: {
                    "Content-Type": "multipart/form-data",
                },
            });
            setData(response.data);
        } catch (error) {
            console.error("Error extracting document data:", error);
        }
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            <div className="bg-white shadow-md rounded-lg p-8 w-full max-w-md">
                <h1 className="text-2xl font-bold text-center mb-6">Upload Document</h1>
                <input
                    type="file"
                    onChange={handleFileChange}
                    className="mb-4 block w-full text-sm text-gray-500 border border-gray-300 rounded-lg focus:outline-none focus:ring focus:ring-blue-300"
                />
                <button
                    onClick={handleUpload}
                    className="w-full bg-blue-500 hover:bg-blue-600 text-white font-semibold py-2 rounded-lg transition duration-200"
                >
                    Upload
                </button>
                {data && (
                    <div className="mt-6">
                        <h2 className="text-xl font-semibold mb-2">Extracted Data:</h2>
                        <p className="text-gray-700"><strong>Name:</strong> {data.name}</p>
                        <p className="text-gray-700"><strong>Document Number:</strong> {data.document_number}</p>
                        <p className="text-gray-700"><strong>Expiration Date:</strong> {data.expiration_date}</p>
                    </div>
                )}
            </div>
        </div>
    );
};

export default DocumentUpload;
