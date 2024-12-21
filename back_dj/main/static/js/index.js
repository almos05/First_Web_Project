const images = [
    "../images/Shoes block.png",
    "../images/supremeBoots.png"
];

let index = 0;

function prevImage() {
    index = (index - 1 + images.length) % images.length;
    updateImage();
}

function nextImage() {
    index = (index + 1) % images.length;
    updateImage();
}

function updateImage() {
    let imageElement = document.getElementById("shoesImage");
    imageElement.src = images[index];
}