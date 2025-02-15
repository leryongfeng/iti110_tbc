import React, { useState } from "react";

const CalibrateImageUploader = ({ setImageUrl }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState("");
    const [fruit, setFruit] = useState("");  // New state for fruit name
    const [price, setPrice] = useState("");  // New state for price


    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert("Please select an image first!");
            return;
        }
    
        if (!fruit.trim() || !price.trim()) {
            alert("Please enter both fruit name and price.");
            return;
        }
    
        const formData = new FormData();
        formData.append("image", selectedFile);
         const fruitData = {
            price: parseFloat(price),
            //size: parseFloat(size)
        };
        formData.append(fruit, JSON.stringify(fruitData)); // Send fruit object

    
        try {
            const response = await fetch("http://127.0.0.1:5000/calibrate", {
                method: "POST",
                body: formData,  // Don't set Content-Type manually
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            // Convert response to a blob (image format)
            const imageBlob = await response.blob();
            const imageUrl = URL.createObjectURL(imageBlob);
    
            setUploadStatus("Calibrate for " + fruit + " successful!");
            setImageUrl(imageUrl);  // Pass image URL to parent
        } catch (error) {
            setUploadStatus(`Upload failed: ${error.message}`);
        }
    };
    
    return (
        <div>
            <input type="file" accept="image/*" onChange={handleFileChange} /><br />
            
            <input 
                type="text" 
                placeholder="Enter fruit name" 
                value={fruit} 
                onChange={(e) => setFruit(e.target.value)} 
            /><br />

            <input 
                type="number" 
                placeholder="Enter price" 
                value={price} 
                onChange={(e) => setPrice(e.target.value)} 
                step="0.01" 
            /><br />

            <button onClick={handleUpload}>Upload Image</button>
            <p>{uploadStatus}</p>
        </div>
    );
};

export default CalibrateImageUploader;
