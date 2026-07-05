function applyCoverPageClass() {
  document.body.classList.toggle(
    "fp-cover-page",
    Boolean(document.querySelector(".fp-cover-full"))
  );
}

document.addEventListener("DOMContentLoaded", applyCoverPageClass);

if (typeof document$ !== "undefined") {
  document$.subscribe(applyCoverPageClass);
}
