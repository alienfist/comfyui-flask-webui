document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder(2);
});

function refreshImages(images) {
    var imageCountValue = 2;
    var domain = location.origin;
    for (var i = 1; i <= imageCountValue; i++) {
        const imageUrl = domain + '/' + images[i-1];
        const placeholderElement = document.getElementById(`imagePlaceholder${i}`);
        placeholderElement.innerHTML = "";
        const imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.addEventListener('click', function() {
            zoomInImage(imageUrl);
        });
        placeholderElement.appendChild(imgElement);
    }
}

function generateImage() {
    const sourceImage = document.getElementById('sourceImageInput');
    const styleImage = document.getElementById('styleImageInput');

    if (sourceImage.files.length === 0) {
        alert('choose source image');
        return;
    }

    if (styleImage.files.length === 0) {
        alert('choose style image');
        return;
    }

    const sourceImageFile = sourceImage.files[0];
    const styleImageFile = styleImage.files[0];

    var formData = new FormData();
    formData.append('source_image_file', sourceImageFile);
    formData.append('style_image_file', styleImageFile);

    const controller = new AbortController();
    const signal = controller.signal;

    const timeoutId = setTimeout(() => {
        controller.abort();
        interruptTask();
        alert('timeout，please try again.');
    }, CHANGE_FACE_TIMEOUT);

    openLoading('Ai processing<br>please waiting...');
    startProgress(300, 1);

    fetch('/style_fusion/generate', {
        method: 'POST',
        body: formData,
        signal: signal
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                var progressBar = document.getElementById('progress-bar');
                progressBar.value = 100;
                const images = data.images_list;
                refreshImages(images);
            } else {
                console.log('Generate image failed:' + data.message);
            }
        })
        .catch(error => {
            console.error('Generate image failed:', error);
            alert('Error occurred during image generation.');
        })
        .finally(() => {
            closeLoading();
            clearTimeout(timeoutId);
            stopProgressUpdate();
        });
}
