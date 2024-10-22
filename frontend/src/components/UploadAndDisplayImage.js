// inspired by https://stackoverflow.com/questions/43692479/how-to-upload-an-image-in-react-js
import React, { useState, useRef } from "react";

// Define a functional component named UploadAndDisplayImage
const UploadAndDisplayImage = () => {
  // Define a state variable to store the selected image
  const [selectedImage, setSelectedImage] = useState(null);
  const inputFileRef = useRef(null);

  const handleRemoveImage = () => {
    setSelectedImage(null); // Clear the selected image from state
    if (inputFileRef.current) {
      inputFileRef.current.value = ""; // Reset the input field
    }
  };

  // Return the JSX for rendering
  return (
    <div>
      {/* Header */}
      Image:

      {/* Conditionally render the selected image if it exists */}
      {selectedImage && (
        <div>
          {/* Display the selected image */}
          <img
            alt="not found"
            width={"250px"}
            src={URL.createObjectURL(selectedImage)}
          />
          <br /> <br />
          {/* Button to remove the selected image */}
          <button onClick={handleRemoveImage}>Remove</button>
        </div>
      )}

      <br />

      {/* Input element to select an image file */}
      {!selectedImage && (
        <input
        type="file"
        name="myImage"
        ref={inputFileRef}
        // Event handler to capture file selection and update the state
        onChange={(event) => {
          console.log(event.target.files[0]); // Log the selected file
          setSelectedImage(event.target.files[0]); // Update the state with the selected file
        }}
      />
      )}
    </div>
  );
};

// Export the UploadAndDisplayImage component as default
export default UploadAndDisplayImage;