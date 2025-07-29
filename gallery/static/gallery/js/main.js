    // Handle image preview for upload
    const imageInput = document.getElementById('id_image');
    if (imageInput) {
        imageInput.addEventListener('change', function() {
            const file = this.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function(e) {
                    const previewContainer = document.getElementById('image-preview');
                    if (previewContainer) {
                        previewContainer.innerHTML = '';
                        const img = document.createElement('img');
                        img.src = e.target.result;
                        img.classList.add('thumbnail');
                        previewContainer.appendChild(img);
                    }
                };
                reader.readAsDataURL(file);
            }
        });
    }

    // Handle share functionality
    const shareButtons = document.querySelectorAll('.share-btn');
    shareButtons.forEach(btn => {
        btn.addEventListener('click', function() {
            const photoId = this.dataset.photoId;
            const photoTitle = this.dataset.photoTitle;
            const photoUrl = window.location.origin + `/photo/${photoId}/`;
            
            if (navigator.share) {
                navigator.share({
                    title: photoTitle,
                    url: photoUrl
                }).catch(error => console.error('Error sharing:', error));
            } else {
                // Fallback for browsers that don't support Web Share API
                const tempInput = document.createElement('input');
                document.body.appendChild(tempInput);
                tempInput.value = photoUrl;
                tempInput.select();
                document.execCommand('copy');
                document.body.removeChild(tempInput);
                
                alert('Link copied to clipboard: ' + photoUrl);
            }
        });
    });

    // Get CSRF token
    function getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='));
        return cookieValue ? cookieValue.split('=')[1] : '';
    }


    fetch('/get-categories/')
    .then(response => response.json())
    .then(data => {
        let dropdown = document.getElementById("category-dropdown");
        dropdown.innerHTML = '<option value="">Select a Category</option>';
        data.categories.forEach(category => {
            let option = document.createElement("option");
            option.value = category.id;
            option.textContent = category.name;
            dropdown.appendChild(option);
        });
    });
