document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder(2);
    loadSelectList("style");
    loadSelectList("divergence");
});

function loadSelectList(selectID) {
    var selectContainer = document.getElementById(selectID);
    selectContainer.innerHTML = "";
    if (selectID === "style") {
        var selectList = IMG2IMG_STYLE
        var defaultValue = "comic1"
    } else if (selectID === "divergence") {
        var selectList = IMG2IMG_DIVERGENCE
        var defaultValue = "0.5"
    }
    selectList.forEach(select => {
        var selectOption = document.createElement("option");
        selectOption.value = select.value;
        selectOption.text = select.text;
        if (select.value === defaultValue) {
          selectOption.selected = true;
        }
        selectContainer.appendChild(selectOption);
    });
}

function refreshImages(images) {
    var imageCountValue = 2;
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

function generateImage() {
    const style = document.getElementById('style').value;
    const divergence = document.getElementById('divergence').value;
    const positivePrompt = document.getElementById('positivePrompt').value;

    const imageInput = document.getElementById('imageInput');
    if (imageInput.files.length === 0) {
        alert('Choose an image.');
        return;
    }
    const imageFile = imageInput.files[0];

    var formData = new FormData();
    formData.append('positive_prompt', positivePrompt);
    formData.append('image_file', imageFile);
    formData.append('style', style);
    formData.append('divergence', divergence);

    const controller = new AbortController();
    const signal = controller.signal;

    const timeoutId = setTimeout(() => {
        controller.abort();
        interruptTask();
        alert('timeout，please try again.');
    }, IMG2IMG_TIMEOUT);

    openLoading('Ai processing<br>please waiting...');
    startProgress(150, 4);

    fetch('/img2img/generate', {
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
