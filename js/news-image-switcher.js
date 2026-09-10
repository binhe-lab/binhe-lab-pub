(function () {
  "use strict";

  var switchers = document.querySelectorAll("[data-image-switcher]");

  switchers.forEach(function (switcher) {
    var dots = switcher.querySelectorAll("[data-image-dot]");
    var track = switcher.querySelector(".news-images__track");
    var startX = null;
    var startY = null;

    switcher.classList.add("news-images--enhanced");

    function showImage(index) {
      switcher.dataset.imageIndex = String(index);

      dots.forEach(function (dot, dotIndex) {
        dot.setAttribute("aria-current", String(dotIndex === index));
      });
    }

    dots.forEach(function (dot) {
      dot.addEventListener("click", function () {
        showImage(Number(dot.dataset.imageDot));
      });
    });

    track.addEventListener("pointerdown", function (event) {
      if (event.pointerType === "mouse") {
        return;
      }

      startX = event.clientX;
      startY = event.clientY;
    });

    track.addEventListener("pointerup", function (event) {
      if (startX === null || startY === null) {
        return;
      }

      var distanceX = event.clientX - startX;
      var distanceY = event.clientY - startY;

      if (Math.abs(distanceX) >= 45 && Math.abs(distanceX) > Math.abs(distanceY)) {
        showImage(distanceX < 0 ? 1 : 0);
      }

      startX = null;
      startY = null;
    });

    track.addEventListener("pointercancel", function () {
      startX = null;
      startY = null;
    });
  });
}());
