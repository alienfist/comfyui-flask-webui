document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder();
    addStyleList();
    initRandom();
});

function initRandom() {
    var toggleElement = document.getElementById("toggle");
    var toggleText = document.getElementById("toggleText");
    toggleElement.checked = true;
    toggleText.textContent = "Open";
}

function addStyleList() {
    var styleContainer = document.getElementById("style");
    styleContainer.innerHTML = "";
    STICKER_STYLE.forEach(style => {
        var styleOption = document.createElement("option");
        styleOption.value = style.value;
        styleOption.text = style.text;
        if (style.value === "cartoon") {
          styleOption.selected = true;
        }
        styleContainer.appendChild(styleOption);
    });
}

function refreshStickers(stickers) {
    var imageCountValue = document.getElementById("imageCountSlider").value;
    var domain = location.origin;
    for (var i = 1; i <= imageCountValue; i++) {
        const imageUrl = domain + '/' + stickers[i-1];
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

function generateSticker() {
    const age = document.getElementById('age').value;
    const imageInput = document.getElementById('imageInput');
    const style = document.getElementById('style').value;
    const imageCount = document.getElementById('imageCountSlider').value;
    const descPrompt = document.getElementById('descPrompt').value;
    var gender = getSelectedRadioValue("gender_radio");
    var removeBg = getSelectedRadioValue("removebg_radio");

    if (imageInput.files.length === 0) {
        alert('Choose a person face image.');
        return;
    }
    const imageFile = imageInput.files[0];

    var formData = new FormData();
    formData.append('image_file', imageFile);
    formData.append('gender', gender);
    formData.append('age', age);
    formData.append('descPrompt', descPrompt);
    formData.append('style', style);
    formData.append('image_count', imageCount);
    formData.append('remove_bg', removeBg);

    const controller = new AbortController();
    const signal = controller.signal;

    const timeoutId = setTimeout(() => {
        controller.abort();
        interruptTask();
        alert('timeout，please try again.');
    }, STICKERS_TIMEOUT);

    openLoading('Ai processing<br>please waiting...');
    startProgress(200, imageCount);

    fetch('/stickers/generate', {
        method: 'POST',
        body: formData,
        signal: signal
    })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                var progressBar = document.getElementById('progress-bar');
                progressBar.value = 100;
                const stickers = data.stickers_list;
                refreshStickers(stickers);
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
