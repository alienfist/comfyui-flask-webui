document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder(1);
});

function refreshImages(images) {
    var domain = location.origin;
    const imageUrl = images[0];
    const placeholderElement = document.getElementById("imagePlaceholder");
    placeholderElement.innerHTML = "";
    const imgElement = document.createElement('img');
    imgElement.src = domain + "/" + imageUrl;
    imgElement.addEventListener('click', function() {
        zoomInImage(imageUrl);
    });
    placeholderElement.appendChild(imgElement);
}

function getSelectedRadioValue(radioName) {
    var radioButtons = document.getElementsByName(radioName);
    var selectedValue = "";
    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked) {
            selectedValue = radioButtons[i].value;
            break;
        }
    }
    return selectedValue;
}

function generateImage() {
    const sourceImage = document.getElementById('sourceImageInput');
    const targetImage = document.getElementById('targetImageInput');
    var removeBg = getSelectedRadioValue("removebg_radio");

    if (sourceImage.files.length === 0) {
        alert('Choose source image.');
        return;
    }

    if (targetImage.files.length === 0) {
        alert('Choose target image.');
        return;
    }

    const sourceImageFile = sourceImage.files[0];
    const targetImageFile = targetImage.files[0];

    var formData = new FormData();
    formData.append('source_image_file', sourceImageFile);
    formData.append('target_image_file', targetImageFile);
    formData.append('remove_bg', removeBg);

    const controller = new AbortController();
    const signal = controller.signal;

    const timeoutId = setTimeout(() => {
        controller.abort();
        interruptTask();
        alert('timeout，please try again.');
    }, CHANGE_FACE_TIMEOUT);

    openLoading('Ai processing<br>please waiting...');
    startProgress(300, 1);

    fetch('/change_face/generate', {
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
