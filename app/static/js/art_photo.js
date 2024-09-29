document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder();
});

function refreshImages(images) {
    var imageCountValue = document.getElementById("imageCountSlider").value;
    var domain = location.origin;
    for (var i = 1; i <= imageCountValue; i++) {
        const imageUrl = domain + '/' + images[i-1];
        const placeholderElement = document.getElementById(`imagePlaceholder${i}`);
        placeholderElement.innerHTML = "";

        const badgeElement = document.createElement('span');
        badgeElement.className = 'corner-badge';
        badgeElement.textContent = i;

        const imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.addEventListener('click', function() {
            zoomInImage(imageUrl);
        });

        placeholderElement.appendChild(badgeElement);
        placeholderElement.appendChild(imgElement);
    }
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
    const scale = document.getElementById('imageScale').innerText;
    const positivePrompt = document.getElementById('positivePrompt').value;
    const imageCount = document.getElementById('imageCountSlider').value;
    var gender = getSelectedRadioValue("gender_radio");

    const imageInput = document.getElementById('imageInput');
    if (imageInput.files.length === 0) {
        alert('Please choose an image.');
        return;
    }
    const imageFile = imageInput.files[0];

    var formData = new FormData();
    formData.append('positive_prompt', positivePrompt);
    formData.append('image_file', imageFile);
    formData.append('scale', scale);
    formData.append('image_count', imageCount);
    formData.append('gender', gender);

    const controller = new AbortController();
    const signal = controller.signal;

    const timeoutId = setTimeout(() => {
        controller.abort();
        interruptTask();
        alert('timeout，please try again.');
    }, IMG2IMG_TIMEOUT);

    openLoading('Ai processing<br>please waiting...');
    startProgress(100, imageCount);

    fetch('/art_photo/generate', {
        method: 'POST',
        body: formData,
        signal: signal
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                var progressBar = document.getElementById('progress-bar');
                progressBar.value = 100;
                const images_list = data.images_list;
                refreshImages(images_list);
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
