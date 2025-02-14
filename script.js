document.getElementById('uploadForm').addEventListener('submit', function (e) {
    e.preventDefault(); // Prevent the form from submitting the traditional way
  
    const fileInput = document.getElementById('fileInput');
    const status = document.getElementById('status');
  
    if (fileInput.files.length === 0) {
      status.textContent = 'Please select a file to upload.';
      return;
    }
  
    const file = fileInput.files[0];
    status.textContent = `Uploading ${file.name}...`;
  
    // Simulate file upload (replace with actual backend API call)
    setTimeout(() => {
      status.textContent = `${file.name} uploaded successfully!`;
    }, 2000); // Simulate a 2-second delay
  });