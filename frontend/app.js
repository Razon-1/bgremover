let currentProcessedImage = null;

async function processImage() {
  const imageInput = document.getElementById('image');
  const bgType = document.getElementById('bgType').value;
  const bgColor = document.getElementById('bgColor').value;
  const model = document.getElementById('model').value;
  const processBtn = document.getElementById('processBtn');
  const statusMsg = document.getElementById('statusMsg');
  const statusText = document.getElementById('statusText');
  const errorMsg = document.getElementById('errorMsg');
  const errorText = document.getElementById('errorText');
  const resultContainer = document.getElementById('resultContainer');

  if (!imageInput.files.length) {
    errorText.textContent = "❌ Please select an image first!";
    errorMsg.classList.remove('hidden');
    return;
  }

  // Hide error and result, show status
  errorMsg.classList.add('hidden');
  resultContainer.classList.add('hidden');
  processBtn.disabled = true;
  statusMsg.classList.remove('hidden');
  statusText.textContent = "Processing... please wait ⏳";

  console.log("Starting image processing...");
  console.log("Image:", imageInput.files[0].name, "Size:", imageInput.files[0].size);

  const formData = new FormData();
  formData.append('image', imageInput.files[0]);
  formData.append('background_type', bgType);
  formData.append('background_value', bgColor);
  formData.append('model', model);

  try {
    console.log("Sending to: http://127.0.0.1:8000/api/process/");
    
    const response = await fetch('http://127.0.0.1:8000/api/process/', {
      method: 'POST',
      body: formData,
      headers: {
        'Accept': 'application/json'
      }
    });

    console.log("Response status:", response.status);
    console.log("Response headers:", response.headers);
    
    if (!response.ok) {
      const errorData = await response.text();
      throw new Error(`HTTP ${response.status}: ${errorData}`);
    }

    const data = await response.json();
    console.log("Response received:", data);

    if (data.image) {
      console.log("✅ Image processed successfully!");
      currentProcessedImage = data.image;
      document.getElementById('result').src = data.image;
      resultContainer.classList.remove('hidden');
      statusMsg.classList.add('hidden');
    } else {
      throw new Error(data.error || "No image returned");
    }
  } catch (error) {
    console.error("❌ Error:", error.message);
    console.error("Stack:", error.stack);
    errorText.textContent = "❌ Error: " + error.message;
    errorMsg.classList.remove('hidden');
    statusMsg.classList.add('hidden');
  } finally {
    processBtn.disabled = false;
  }
}

function downloadImage() {
  if (!currentProcessedImage) {
    alert("No image to download");
    return;
  }

  const link = document.createElement('a');
  link.href = currentProcessedImage;
  link.download = 'processed_image_' + new Date().getTime() + '.png';
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}
