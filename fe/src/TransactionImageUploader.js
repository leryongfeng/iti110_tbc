import React, { useState } from "react";

const API_URL = process.env.REACT_APP_API_URL;

const TransactionImageUploader = ({ transactionNumber, updateTransaction, setImageUrl, addLog }) => {
    const [selectedFile, setSelectedFile] = useState(null);

    const handleFileChange = (event) => {
        setSelectedFile(event.target.files[0]);
    };

    const handleUpload = async () => {
        if (!selectedFile) {
            alert("Please select an image first!");
            return;
        }
    
        if (!transactionNumber) {
            alert("Transaction number is missing. Start a transaction first.");
            return;
        }
    
        const formData = new FormData();
        formData.append("image", selectedFile);
        formData.append("transaction_number", String(transactionNumber));
        let imageBlob = null; // Store image blob whether success or error
        let message = null;

        try {
            const controller = new AbortController()
            // 60 second timeout
            const timeoutId = setTimeout(() => controller.abort(), 60000)

            const response = await fetch(`${API_URL}/transact_image`, {
                method: "POST",
                body: formData,  // Don't set Content-Type manually
                headers: { "Accept": "application/json" },
            }, { signal: controller.signal });

            // Convert response to a blob (image format)
            imageBlob = await response.blob();
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            const imageUrl = URL.createObjectURL(imageBlob);

            setImageUrl(imageUrl);  // Pass image URL to parent
            updateTransaction();

            addLog(`Image Transacted successfully`); // ✅ Log success
        } catch (error) {
            addLog(`Transaction failed: Please remove any bad fruits and try again. ${message}`); // ✅ Log success

            if (imageBlob) {
                const imageUrl = URL.createObjectURL(imageBlob);
                setImageUrl(imageUrl); // Still display image even on error
            }
        }
    };
    
    return (
        <div>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Transact</button>
        </div>
    );
};

export default TransactionImageUploader;
