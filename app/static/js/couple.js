document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder();
    loadSelectList("checkpoint");
    loadSelectList("lora1");
    loadSelectList("lora2");
});

function loadSelectList(selectID) {
    var selectContainer = document.getElementById(selectID);
    selectContainer.innerHTML = "";
    if (selectID === "checkpoint") {
        var selectList = COUPLE_CHECKPOINTS
        var defaultValue = "juggernautXL_v9Rdphoto2Lightning.safetensors"
    } else if (selectID === "lora1") {
        var selectList = LORAS
        var defaultValue = "SDXLFaeTastic2400.safetensors"
    } else if (selectID === "lora2") {
        var selectList = LORAS
        var defaultValue = "Harrlogos_v2.0.safetensors"
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
    const positivePrompt = document.getElementById('positivePrompt').value;
    const checkpoint = document.getElementById('checkpoint').value;
    const lora1 = document.getElementById('lora1').value;
    const lora2 = document.getElementById('lora2').value;
    const imageCount = document.getElementById('imageCountSlider').value;
    var removeBg = getSelectedRadioValue('removebg_radio');

    const imageLeftInput = document.getElementById('leftImageInput');
    if (imageLeftInput.files.length === 0) {
        alert('choose left image');
        return;
    }
    const imageLeftFile = imageLeftInput.files[0];

    const imageRightInput = document.getElementById('rightImageInput');
    if (imageRightInput.files.length === 0) {
        alert('choose right image');
        return;
    }
    const imageRightFile = imageRightInput.files[0];

    const imagePoseInput = document.getElementById('poseImageInput');
    if (imagePoseInput.files.length === 0) {
        alert('choose pose image');
        return;
    }
    const imagePoseFile = imagePoseInput.files[0];

    var formData = new FormData();
    formData.append('positive_prompt', positivePrompt);
    formData.append('checkpoint', checkpoint);
    formData.append('lora1', lora1);
    formData.append('lora2', lora2);
    formData.append('image_left_file', imageLeftFile);
    formData.append('image_right_file', imageRightFile);
    formData.append('image_pose_file', imagePoseFile);
    formData.append('image_count', imageCount);
    formData.append('remove_bg', removeBg);

    const controller = new AbortController();
    const signal = controller.signal;

    const timeoutId = setTimeout(() => {
        controller.abort();
        interruptTask();
        alert('timeout，please try again.');
    }, IMG2IMG_TIMEOUT);

    openLoading('Ai processing<br>please waiting...');
    startProgress(200, imageCount);

    fetch('/couple/generate', {
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
