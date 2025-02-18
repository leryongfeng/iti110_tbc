import React, { useState } from "react";

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

        try {
            const response = await fetch("http://127.0.0.1:5000/transact_image", {
                method: "POST",
                body: formData,  // Don't set Content-Type manually
            });

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
            addLog(`Transaction failed: ${error.message}`); // ✅ Log success

            if (imageBlob) {
                const imageUrl = URL.createObjectURL(imageBlob);
                setImageUrl(imageUrl); // Still display image even on error
            }
        }
    };
    
    return (
        <div>
            <input type="file" accept="image/*" onChange={handleFileChange} />
            <button onClick={handleUpload}>Upload Image</button>
        </div>
    );
};

export default TransactionImageUploader;
