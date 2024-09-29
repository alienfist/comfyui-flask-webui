document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder(2);
    loadSelectList("idPhotoSize");
    loadSelectList("idPhotoClothing");
    loadSelectList("idPhotoColor");
    loadSelectList("idPhotoExposure");
    loadSelectList("idPhotoLayNum");
});

function loadSelectList(selectID) {
    var selectContainer = document.getElementById(selectID);
    selectContainer.innerHTML = "";
    if (selectID === "idPhotoSize") {
        var selectList = ID_PHOTO_SIZE
        var defaultValue = "1寸"
    } else if (selectID === "idPhotoClothing") {
        var selectList = ID_PHOTO_CLOTHING
        var defaultValue = "(Black suit jacket with white shirt underneath:1.5), "
    } else if (selectID === "idPhotoColor") {
        var selectList = ID_PHOTO_COLOR
        var defaultValue = "white"
    } else if (selectID === "idPhotoExposure") {
        var selectList = ID_PHOTO_EXPOSURE
        var defaultValue = "10"
    } else if (selectID === "idPhotoLayNum") {
        var selectList = ID_PHOTO_LAY_NUM
        var defaultValue = "6"
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
        const imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.addEventListener('click', function() {
            zoomInImage(imageUrl);
        });
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
    const idPhotoColor = document.getElementById('idPhotoColor').value;
    const idPhotoClothing = document.getElementById('idPhotoClothing').value;
    const idPhotoSize = document.getElementById('idPhotoSize').value;
    const idPhotoExposure = document.getElementById('idPhotoExposure').value;
    const idPhotoLayNum = document.getElementById('idPhotoLayNum').value;
    const descPrompt = document.getElementById('descPrompt').value;
    var beauty = getSelectedRadioValue("beauty_radio");

    const faceImageInput = document.getElementById('faceImageInput');
    if (faceImageInput.files.length === 0) {
        alert('Choose a person face image.');
        return;
    }
    const faceImageFile = faceImageInput.files[0];

    const poseImageInput = document.getElementById('poseImageInput');
    if (poseImageInput.files.length === 0) {
        alert('Choose a person pos image.');
        return;
    }
    const poseImageFile = poseImageInput.files[0];

    var formData = new FormData();
    formData.append('face_image_file', faceImageFile);
    formData.append('pose_image_file', poseImageFile);
    formData.append('id_photo_color', idPhotoColor);
    formData.append('id_photo_clothing', idPhotoClothing);
    formData.append('id_photo_size', idPhotoSize);
    formData.append('id_photo_exposure', idPhotoExposure);
    formData.append('id_photo_lay_num', idPhotoLayNum);
    formData.append('desc_prompt', descPrompt);
    formData.append('beauty', beauty);

    const controller = new AbortController();
    const signal = controller.signal;

    const timeoutId = setTimeout(() => {
        controller.abort();
        interruptTask();
        alert('timeout，please try again.');
    }, ID_PHOTO_TIMEOUT);

    openLoading('Ai processing<br>please waiting...');
    startProgress(200, 4);

    fetch('/id_photo/generate', {
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
