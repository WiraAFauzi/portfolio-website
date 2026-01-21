// ===============================
// Theme Toggle (Dark / Light)
// ===============================
const toggle = document.getElementById("darkToggle");

if (toggle) {
  toggle.addEventListener("click", () => {
    document.body.classList.toggle("dark");

    localStorage.setItem(
      "theme",
      document.body.classList.contains("dark") ? "dark" : "light"
    );
  });
}

// Load saved theme on page load
if (localStorage.getItem("theme") === "dark") {
  document.body.classList.add("dark");
}

// ===============================
// Render Wake-Up Banner Auto Hide
// ===============================
document.addEventListener("DOMContentLoaded", () => {
  const banner = document.getElementById("wake-banner");

  if (banner) {
    setTimeout(() => {
      banner.style.opacity = "0";
      banner.style.transition = "opacity 0.5s ease";

      setTimeout(() => {
        banner.remove();
      }, 600);
    }, 8000); // visible for 8 seconds
  }
});
