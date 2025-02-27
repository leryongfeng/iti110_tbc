import React, { useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;

const CalibrateImageUploader = ({ setImageUrl, addLog }) => {
    const [selectedFile, setSelectedFile] = useState(null);
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
        let imageBlob = null; // Store image blob whether success or error
    
        try {
            const controller = new AbortController();
            // 60 second timeout
            const timeoutId = setTimeout(() => controller.abort(), 60000);

            const response = await fetch(`${API_URL}/calibrate`, {
                method: "POST",
                body: formData,  // Don't set Content-Type manually
                headers: { "Accept": "application/json" },
            }, { signal: controller.signal });

            imageBlob = await response.blob();
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const imageUrl = URL.createObjectURL(imageBlob);
    
            setImageUrl(imageUrl);  // Pass image URL to parent

            addLog("Calibrate for " + fruit + " successful!"); // ✅ Log success
        } catch (error) {
            addLog(`Calibration failed: Please try again. ${error.response.message}`); // ✅ Log success

            if (imageBlob) {
                const imageUrl = URL.createObjectURL(imageBlob);
                setImageUrl(imageUrl); // Still display image even on error
            }
        }
    };
    
    return (
        <div>
            <input type="file" accept="image/*" onChange={handleFileChange}/><br/>
            <select value={fruit}
                    onChange={(e) => setFruit(e.target.value)}>
                <option disabled={true} value="" color="gray">Enter fruit name</option>
                <option name="apple">apple</option>
                <option name="banana">banana</option>
                <option name="kiwi">kiwi</option>
                <option name="pear">pear</option>
                <option name="starfruit">starfruit</option>
            </select>
            <input
                type="number"
                placeholder="Enter price"
                value={price}
                onChange={(e) => setPrice(e.target.value)}
                step="0.01"
            /><br/>

            <button onClick={handleUpload}>Calibrate</button>
        </div>
    );
};

export default CalibrateImageUploader;
