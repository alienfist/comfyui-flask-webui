let page = 1;
const perPage = 12;
let loading = false;
let noMoreData = false;
let imagesData = [];
let currentImageIndex = -1;
let userUuid = '';

document.addEventListener('DOMContentLoaded', () => {
    fetchUserUuid().then(() => {
        fetchImages();
    });
});

const fetchUserUuid = () => {
    return fetch('/api/get_user_uuid')
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user UUID');
            }
            return response.json();
        })
        .then(data => {
            userUuid = data.user_uuid;
            console.log('User UUID:', userUuid);
        })
        .catch(error => {
            console.error('Error fetching user UUID:', error);
        });
};

const fetchImages = () => {
    if (loading || noMoreData) return;
    loading = true;
    document.getElementById('loading').style.display = 'block';

    fetch(`/api/images?user_uuid=${userUuid}&page=${page}&per_page=${perPage}`)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch images');
            }
            return response.json();
        })
        .then(data => {
            if (data.images.length === 0) {
                noMoreData = true;
                document.getElementById('no-more-data').style.display = 'block';
            } else {
                const gallery = document.getElementById('gallery');
                data.images.forEach(image => {
                    imagesData.push(image);
                    const div = document.createElement('div');
                    div.classList.add('image-item');
                    div.innerHTML = `
                        <div class="image-title">
                            <p>${image.create_time}</p>
                            <span class="delete-icon" onclick="deleteImage('${image.id}', this)">🗑️</span>
                        </div>
                        <img src="${image.image_url}" alt="Image" onclick="zoomImage('${image.image_url}')">
                    `;
                    gallery.appendChild(div);
                });
                page++;
            }
        })
        .catch(error => {
            console.error('Error fetching images:', error);
        })
        .finally(() => {
            loading = false; // 这里确保在请求结束时重置 loading 状态
            document.getElementById('loading').style.display = 'none';
        });
};

document.querySelector('.work-area').addEventListener('scroll', () => {
    const main = document.querySelector('.work-area');
    if (main.scrollTop + main.clientHeight >= main.scrollHeight - 100) {
        fetchImages();
    }
});

const zoomImage = (imageUrl) => {
    currentImageIndex = imagesData.findIndex(image => image.image_url === imageUrl);
    const modal = document.getElementById('image-modal');
    const modalImg = document.getElementById('modal-img');
    modal.style.display = "flex"; // Use flex to center the content
    modalImg.src = imageUrl;
};

const changeImage = (direction) => {
    currentImageIndex += direction;
    if (currentImageIndex < 0) {
        currentImageIndex = imagesData.length - 1;
    } else if (currentImageIndex >= imagesData.length) {
        currentImageIndex = 0;
    }
    const modalImg = document.getElementById('modal-img');
    modalImg.src = imagesData[currentImageIndex].image_url;
};

const deleteImage = (imageId, element) => {
    const confirmation = window.confirm("Confirm to delete photo?");
    if (!confirmation) return;

    fetch(`/api/delete_image?image_id=${imageId}`, { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const imageItem = element.closest('.image-item');
                imageItem.remove();
                imagesData = imagesData.filter(image => image.id !== imageId);
            } else {
                console.error('Error deleting image:', data.message);
            }
        })
        .catch(error => console.error('Error deleting image:', error));
};

const closeModal = () => {
    const modal = document.getElementById('image-modal');
    modal.style.display = "none";
};

window.zoomImage = zoomImage;
window.changeImage = changeImage;
window.deleteImage = deleteImage;
window.closeModal = closeModal;
