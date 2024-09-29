function openLoading (text) {
    document.getElementById('loadingText').innerHTML = text;
    document.getElementById('loadingOverlay').style.display = 'block';
}

function closeLoading () {
    document.getElementById('loadingOverlay').style.display = 'none';
}

function redirectToHomepage() {
  window.location.href = '/';
}

// Zoom in image
function zoomInImage(imageUrl) {
    var zoomOverlay = document.getElementById('zoomOverlay');
    var imgElement = zoomOverlay.querySelector('img');
    imgElement.setAttribute('src', imageUrl);
    imgElement.onload = function() {
        var width = imgElement.width;
        var height = imgElement.height;
        var containerWidth = zoomOverlay.offsetWidth;
        var containerHeight = zoomOverlay.offsetHeight;
        var aspectRatio = width / height;
        if (width > containerWidth || height > containerHeight) {
            if (containerWidth / containerHeight > aspectRatio) {
                imgElement.classList.add('zoomed-width');
                imgElement.classList.remove('zoomed-height');
            } else {
                imgElement.classList.add('zoomed-height');
                imgElement.classList.remove('zoomed-width');
            }
        } else {
            imgElement.classList.remove('zoomed-width');
            imgElement.classList.remove('zoomed-height');
        }
        zoomOverlay.style.display = 'block';
    };
    zoomOverlay.onclick = function() {
        zoomOverlay.style.display = 'none';
    };
}

// get constants
function fetchConstants(constantName) {
    return fetch('/api/constants', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: constantName })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        return response.json();
    })
    .then(data => {
        if (data.error) {
            console.error('Error:', data.error);
            return null;
        }
        const constantData = data[constantName];
        console.log(`${constantName}:`, constantData);
        return constantData;
    })
    .catch(error => {
        console.error('Error fetching constants:', error);
        return null;
    })
}

// interrupt task
function interruptTask() {
        fetch('/interrupt', {
        method: 'POST',
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            alert('Task cancelled');
        } else {
            console.log('Task cancellation failed: ' + data.message);
        }
    })
    .catch(error => {
        console.error('Task cancellation failed:', error);
    })
    .finally(() => {
        closeLoading();
    });
}

// Fake progress bar
var stopProgress = false; // stop flag: control progress bar

async function startProgress(unit, imageCountValue) {
    // unit:ms
    var progressBar = document.getElementById('progress-bar');
    progressBar.value = 0;
    var progress = 0;
    stopProgress = false; // reset stop flag
    while (progress < 96) {
        await new Promise(function(resolve) {
            setTimeout(function() {
                progress += 1;
                progressBar.value = progress;
                resolve();
            }, parseInt(unit * imageCountValue));
        });

        if (stopProgress) {
            progressBar.value = 0; // clear progress value
            return;
        }
    }
}

function stopProgressUpdate() {
    stopProgress = true;
    var progressBar = document.getElementById('progress-bar');
    progressBar.value = 0;
}

function previewImage(input, type = "") {
    const imagePreview = document.getElementById("imagePreview" + type);
    const imagePreviewContainer = document.getElementById("imagePreviewContainer" + type);
    const clearContainer = document.getElementById("clearImage" + type);
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        reader.onload = function (e) {
            imagePreview.src = e.target.result;
            imagePreviewContainer.style.display = "block";
            clearContainer.style.display = "block";
        };
        reader.readAsDataURL(input.files[0]);
    } else {
        imagePreviewContainer.style.display = "none";
        clearContainer.style.display = "none";
    }
}

function clearImagePreview(type = "") {
    var imagePreview = document.getElementById("imagePreview" + type);
    var imagePreviewContainer = document.getElementById("imagePreviewContainer" + type);
    var clearContainer = document.getElementById("clearImage" + type);
    if (imagePreview) {imagePreview.src = "#";}
    if (imagePreviewContainer) {imagePreviewContainer.style.display = "none";}
    if (clearContainer) {clearContainer.style.display = "none";}
}

function updateImageCount(value) {
    document.getElementById("imageCount").innerText = value;
    addImagePlaceholder();
}

function updateImageSlider(value) {
    document.getElementById("imageCountSlider").value = value;
    addImagePlaceholder();
}

function updateImageScale(value) {
    document.getElementById("imageScale").innerText = IMAGE_SCALE[value];
}

function addImagePlaceholder(imageCountValue = null) {
    var placeholderContainer = document.getElementById("placeholderContainer");
    placeholderContainer.innerHTML = "";

    if (imageCountValue === null) {
        imageCountValue = document.getElementById("imageCountSlider").value;
    }

    imageCountValue = parseInt(imageCountValue, 10);
    if (isNaN(imageCountValue) || imageCountValue < 1) {
        console.error("Invalid image count value:", imageCountValue);
        return;
    }

    for (var i = 1; i <= imageCountValue; i++) {
        var placeholder = document.createElement("div");
        placeholder.classList.add("imagePlaceholder");
        placeholder.classList.add("imagePlaceholderNum" + imageCountValue);
        placeholder.id = `imagePlaceholder${i}`;
        placeholderContainer.appendChild(placeholder);
    }
}
