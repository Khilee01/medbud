import React, { useEffect, useRef, useState } from "react";

const CameraScanner = () => {
    const videoRef = useRef(null);
    const canvasRef = useRef(null);
    const [medicineInfo, setMedicineInfo] = useState(null);
    const [capturedImage, setCapturedImage] = useState(null);
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState(null);
    const [cameraActive, setCameraActive] = useState(false);
    const [backendStatus, setBackendStatus] = useState(null);

    // Check backend status when component mounts
    useEffect(() => {
        checkBackendStatus();
        
        return () => {
            // Cleanup: stop tracks when component unmounts
            if (videoRef.current && videoRef.current.srcObject) {
                const tracks = videoRef.current.srcObject.getTracks();
                tracks.forEach(track => track.stop());
            }
        };
    }, []);

    // Function to check if backend is running
    const checkBackendStatus = async () => {
        try {
            const response = await fetch("http://localhost:5000/health", {
                method: "GET",
            });
            
            if (response.ok) {
                setBackendStatus("connected");
                setError(null);
            } else {
                setBackendStatus("error");
                setError("Backend service is not responding correctly");
            }
        } catch (error) {
            console.error("Backend connection error:", error);
            setBackendStatus("error");
            setError("Cannot connect to backend service. Please make sure the Python server is running.");
        }
    };

    // Function to start the camera
    const startCamera = async () => {
        try {
            // Check backend status first
            if (backendStatus !== "connected") {
                await checkBackendStatus();
                if (backendStatus !== "connected") {
                    return; // Don't start camera if backend isn't available
                }
            }
            
            // Stop any existing tracks
            if (videoRef.current && videoRef.current.srcObject) {
                const tracks = videoRef.current.srcObject.getTracks();
                tracks.forEach(track => track.stop());
            }

            const stream = await navigator.mediaDevices.getUserMedia({ 
                video: { facingMode: "environment" } // Use back camera if available
            });
            
            if (videoRef.current) {
                videoRef.current.srcObject = stream;
                setCameraActive(true);
                setError(null);
            }
        } catch (error) {
            console.error("Error accessing camera:", error);
            setError("Failed to access camera. Please check permissions.");
            setCameraActive(false);
        }
    };

    // Function to stop the camera
    const stopCamera = () => {
        if (videoRef.current && videoRef.current.srcObject) {
            const tracks = videoRef.current.srcObject.getTracks();
            tracks.forEach(track => track.stop());
            videoRef.current.srcObject = null;
            setCameraActive(false);
        }
    };

    // Function to capture and process the image
    const captureAndUploadImage = async () => {
        setIsLoading(true);
        setError(null);
        
        const canvas = canvasRef.current;
        const video = videoRef.current;

        if (canvas && video) {
            try {
                // Set canvas dimensions to match the video
                canvas.width = video.videoWidth;
                canvas.height = video.videoHeight;
                
                const context = canvas.getContext("2d");
                context.drawImage(video, 0, 0, canvas.width, canvas.height);

                // Get the image data URL and set it to state
                const imageDataUrl = canvas.toDataURL("image/jpeg");
                setCapturedImage(imageDataUrl);

                // Extract the base64 data
                const base64Data = imageDataUrl.split(',')[1];

                // Send to the API using the base64 data directly
                const response = await fetch("http://localhost:5000/upload", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        image_data: imageDataUrl
                    }),
                });

                const data = await response.json();
                
                if (response.ok) {
                    setMedicineInfo(data);
                    speakMedicineInfo(data.medicine, data.description);
                } else {
                    throw new Error(data.message || data.error || "Failed to process the image");
                }
                
                setIsLoading(false);
            } catch (error) {
                console.error("Error capturing/processing image:", error);
                setError(error.message || "Failed to process the image");
                setIsLoading(false);
                speakError();
            }
        }
    };

    // Function to convert medicine name and info to speech
    const speakMedicineInfo = (name, description) => {
        if (!window.speechSynthesis) return;
        
        const speech = new SpeechSynthesisUtterance();
        if (name) {
            speech.text = `The medicine is ${name}. ${description ? "Description: " + description : "No additional details available."}`;
        } else {
            speech.text = "Unable to identify the medicine.";
        }
        speech.lang = "en-US";
        speech.rate = 1;
        window.speechSynthesis.speak(speech);
    };

    // Function to speak error messages
    const speakError = () => {
        if (!window.speechSynthesis) return;
        
        const speech = new SpeechSynthesisUtterance();
        speech.text = "There was an error processing the image. Please try again with a clearer image.";
        speech.lang = "en-US";
        window.speechSynthesis.speak(speech);
    };

    return (
        <div className="container mx-auto p-4">
            <h2 className="text-2xl font-bold mb-4 text-center">Medicine Scanner</h2>
            
            {backendStatus === "error" && (
                <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                    <p className="font-bold">Backend Connection Error</p>
                    <p>{error}</p>
                    <button 
                        onClick={checkBackendStatus} 
                        className="mt-2 bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded"
                    >
                        Retry Connection
                    </button>
                </div>
            )}
            
            <div className="mb-4 relative">
                <video 
                    ref={videoRef} 
                    autoPlay 
                    playsInline 
                    className={`w-full max-w-md mx-auto border-2 rounded-lg ${cameraActive ? 'block' : 'hidden'}`}
                    style={{ height: "300px", objectFit: "cover" }}
                ></video>
                
                <canvas 
                    ref={canvasRef} 
                    className="hidden"
                ></canvas>
                
                {capturedImage && !cameraActive && (
                    <div className="mt-4 text-center">
                        <h3 className="text-lg font-semibold mb-2">Captured Image:</h3>
                        <img 
                            src={capturedImage} 
                            alt="Captured" 
                            className="mx-auto border rounded-lg shadow-md"
                            style={{ maxWidth: "100%", maxHeight: "300px" }}
                        />
                    </div>
                )}
                
                {isLoading && (
                    <div className="absolute inset-0 flex items-center justify-center bg-gray-800 bg-opacity-50 rounded-lg">
                        <div className="text-white">Processing...</div>
                    </div>
                )}
            </div>
            
            <div className="flex justify-center gap-4 mb-4">
                {!cameraActive ? (
                    <button 
                        onClick={startCamera} 
                        className="bg-blue-500 hover:bg-blue-600 text-white px-4 py-2 rounded-lg"
                        disabled={backendStatus === "error"}
                    >
                        Start Camera
                    </button>
                ) : (
                    <>
                        <button 
                            onClick={captureAndUploadImage} 
                            className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded-lg"
                            disabled={isLoading}
                        >
                            Scan Medicine
                        </button>
                        <button 
                            onClick={stopCamera} 
                            className="bg-red-500 hover:bg-red-600 text-white px-4 py-2 rounded-lg"
                            disabled={isLoading}
                        >
                            Stop Camera
                        </button>
                    </>
                )}
            </div>
            
            {error && backendStatus !== "error" && (
                <div className="bg-red-100 border-l-4 border-red-500 text-red-700 p-4 mb-4">
                    <p>{error}</p>
                </div>
            )}
            
            {medicineInfo && (
                <div className="bg-white p-4 rounded-lg shadow-md">
                    <h3 className="text-xl font-bold mb-2">{medicineInfo.medicine}</h3>
                    
                    {medicineInfo.description && (
                        <div className="mb-2">
                            <p className="font-semibold">Description/Dosage:</p>
                            <p>{medicineInfo.description}</p>
                        </div>
                    )}
                    
                    {medicineInfo.source && (
                        <div className="mt-4 text-sm text-gray-600">
                            <p>Source: {medicineInfo.source}</p>
                        </div>
                    )}
                    
                    {medicineInfo.uses && (
                        <div className="mb-2">
                            <p className="font-semibold">Uses:</p>
                            <p>{medicineInfo.uses}</p>
                        </div>
                    )}
                    
                    {medicineInfo.side_effects && (
                        <div className="mb-2">
                            <p className="font-semibold">Side Effects:</p>
                            <p>{medicineInfo.side_effects}</p>
                        </div>
                    )}
                    
                    {medicineInfo.warnings && (
                        <div>
                            <p className="font-semibold">Warnings:</p>
                            <p>{medicineInfo.warnings}</p>
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};

export default CameraScanner;