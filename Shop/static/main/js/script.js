var sliderIndex = 1;
showSlides(sliderIndex);

function plusSlide(n){
    sliderIndex+=n;
    showSlides(sliderIndex);
}

function currentSlide(n){
    sliderIndex = n;
    showSlides(sliderIndex);
}
function showSlides(n){
    var slides = document.getElementsByClassName("mySlide");
    var dots = document.getElementsByClassName("dot")
    if(n>slides.length){
        sliderIndex=1;
    }
    if(n<1){
        sliderIndex = slides.length;
    }
    for(var i = 0;i<slides.length;i++){
        slides[i].style.display = "none";
    }
    for(var i = 0;i<dots.length;i++){
        dots[i].className = dots[i].className.replace("dot active","dot");
    }
    slides[sliderIndex-1].style.display = "block";
    dots[sliderIndex-1].className += " active";
}