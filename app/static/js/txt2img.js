document.addEventListener('DOMContentLoaded', function() {
    addImagePlaceholder();
    loadSelectList("style");
    loadSelectList("checkpoint");
    loadSelectList("lora1");
    loadSelectList("lora2");
    loadSelectList("lora3");
});

function loadSelectList(selectID) {
    var selectContainer = document.getElementById(selectID);
    selectContainer.innerHTML = "";
    if (selectID === "style") {
        var selectList = TXT2IMAGE_STYLE
        var defaultValue = "base"
    } else if (selectID === "checkpoint") {
        var selectList = CHECKPOINTS
        var defaultValue = "sd_xl_base_1.0.safetensors"
    } else if (selectID === "lora1") {
        var selectList = LORAS
        var defaultValue = ""
    } else if (selectID === "lora2") {
        var selectList = LORAS
        var defaultValue = ""
    } else if (selectID === "lora3") {
        var selectList = LORAS
        var defaultValue = ""
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

        // Create corner object
        const badgeElement = document.createElement('span');
        badgeElement.className = 'corner-badge';
        badgeElement.textContent = i;

        // Create image object
        const imgElement = document.createElement('img');
        imgElement.src = imageUrl;
        imgElement.addEventListener('click', function() {
            zoomInImage(imageUrl);
        });

        // Add corner and images
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
    const negativePrompt = document.getElementById('negativePrompt').value;
    const style = document.getElementById('style').value;
    const scale = document.getElementById('imageScale').innerText;
    const lora1 = document.getElementById('lora1').value;
    const lora1_weight = document.getElementById('lora1Weight').value;
    const lora2 = document.getElementById('lora2').value;
    const lora2_weight = document.getElementById('lora2Weight').value;
    const lora3 = document.getElementById('lora3').value;
    const lora3_weight = document.getElementById('lora3Weight').value;
    const checkpoint = document.getElementById('checkpoint').value;
    const imageCount = document.getElementById('imageCountSlider').value;
    var removeBg = getSelectedRadioValue("removebg_radio");

    if (!positivePrompt) {
        alert('please input positive prompt.');
        return;
    }

    var formData = new FormData();
    formData.append('positive_prompt', positivePrompt);
    formData.append('negative_prompt', negativePrompt);
    formData.append('style', style);
    formData.append('scale', scale);
    formData.append('lora1', lora1);
    formData.append('lora1_weight', lora1_weight);
    formData.append('lora2', lora2);
    formData.append('lora2_weight', lora2_weight);
    formData.append('lora3', lora3);
    formData.append('lora3_weight', lora3_weight);
    formData.append('checkpoint', checkpoint);
    formData.append('image_count', imageCount);
    formData.append('remove_bg', removeBg);

    // AbortController object
    const controller = new AbortController();
    const signal = controller.signal;

    // Set timeout handling
    const timeoutId = setTimeout(() => {
        controller.abort(); // interrupt request
        interruptTask();
        alert('timeout，please try again.');
    }, TXT2IMG_TIMEOUT);

    // Pop-up
    openLoading('Ai processing<br>please waiting...');
    startProgress(100, imageCount);

    fetch('/txt2img/generate', {
        method: 'POST',
        body: formData,
        signal: signal // Send abortSignal to fetch
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

function clearPlaceholder(id) {
    document.getElementById(id).placeholder = '';
}
