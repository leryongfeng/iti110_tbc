import React, { useState } from "react";

const TransactionImageUploader = ({ transactionNumber, updateTransaction, setImageUrl }) => {
    const [selectedFile, setSelectedFile] = useState(null);
    const [uploadStatus, setUploadStatus] = useState("");

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
    
        try {
            const response = await fetch("http://127.0.0.1:5000/transact_image", {
                method: "POST",
                body: formData,  // Don't set Content-Type manually
            });
    
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
    
            // Convert response to a blob (image format)
            const imageBlob = await response.blob();
            const imageUrl = URL.createObjectURL(imageBlob);

            setUploadStatus("Upload successful!");
            setImageUrl(imageUrl);  // Pass image URL to parent
            updateTransaction();
        } catch (error) {
            setUploadStatus(`Upload failed: ${error.message}`);
        }
    };
    
    return (
        <div>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload Image</button>
            <p>{uploadStatus}</p>
        </div>
    );
};

export default TransactionImageUploader;
