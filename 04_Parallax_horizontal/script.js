window.addEventListener("scroll", function() {
    let pageY = window.pageYOffset;
    let main = document.querySelector("main");
    main.style.backgroundPosition = `-${pageY * .90}px -100px`;
})