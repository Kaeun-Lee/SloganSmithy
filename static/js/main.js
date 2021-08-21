const toggleBtn = document.querySelector(".navbar__toogleBtn");
const menu = document.querySelector(".navbar__menu");
const icons = document.querySelector(".navbar__icons");

$(function () {
  $("#fullpage").fullpage({
    //options here
    autoScrolling: true,
    scrollHorizontally: true,
    navigation: true,
    NavigationPosition: "right",
  });
});

toggleBtn.addEventListener("click", () => {
  menu.classList.toggle("active");
  icons.classList.toggle("active");
});

const slideValue = document.querySelector(".valueNumber");
const inputSlider = document.querySelector(".valueInput");
inputSlider.oninput = () => {
  let value = inputSlider.value;
  slideValue.textContent = value;
  slideValue.style.left = (value * 10) / 7 + "%";
  slideValue.classList.add("show");
};
inputSlider.onblur = () => {
  slideValue.classList.remove("show");
};

window.onload = () => {
  const openButtons = Array.from(document.getElementsByClassName("open"));
  console.log(openButtons);
  const modal = document.querySelector(".modal");
  const overlay = modal.querySelector(".modal__overlay");
  const closeBtn = modal.querySelector("button");
  const openModal = (e) => {
    // console.log(e);
    const trgText = e.target.innerText;
    const modalTextObj = document.querySelector("#sloganModalText");
    modal.classList.remove("hidden");
    modalTextObj.innerText = trgText;
  };
  const closeModal = () => {
    modal.classList.add("hidden");
  };
  overlay.addEventListener("click", closeModal);
  closeBtn.addEventListener("click", closeModal);
  openButtons.map((obj) => {
    obj.addEventListener("click", openModal);
  });
};
