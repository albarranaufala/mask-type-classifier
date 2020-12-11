const baseUrl = 'https://mask-type-classifier.herokuapp.com/';
const inputFile = document.querySelector('input[type="file"]');
const img = document.getElementById('img-preview');
const button = document.querySelector("button");
const loadingIndicator = document.querySelector(".loading-indicator");
const errorIndicator = document.querySelector(".error");
const result = document.querySelector(".result");

inputFile.addEventListener('change', function() {
    if (this.files && this.files[0]) {
        img.classList.remove('d-none');
        img.src = URL.createObjectURL(this.files[0]);

                
    } else {
        img.classList.add('d-none');
    }
});

button.addEventListener('click', function(){
    if (inputFile.files && inputFile.files[0]) {
        const data = new FormData();
        data.append('file', inputFile.files[0]);
        predictImage(data);
    } else {
        errorIndicator.classList.remove('d-none');
        errorIndicator.textContent = "Harap pilih dulu foto yang mau di deteksi";
    }
});

function predictImage(data){
    loadingIndicator.classList.remove('d-none');
    button.classList.add('d-none');
    errorIndicator.classList.add('d-none');

    fetch(`${baseUrl}/predict`, {
        method: 'POST',
        body: data
    })
    .then(response => response.json())
    .then(response => {
        loadingIndicator.classList.add('d-none');
        button.classList.remove('d-none');
        result.classList.remove('d-none');
        result.textContent = `Hmm.. Menurut saya itu masker ${response.class_name}`
    })
    .catch(error => {
        loadingIndicator.classList.add('d-none');
        button.classList.remove('d-none');
        errorIndicator.classList.remove('d-none');
        errorIndicator.innerText = "Memprediksi gambar gagal, mungkin internet kamu burik";
        console.log(error);
    })
}