const iconMap = {
  playstore: "/static/icons/playstore.svg",
  appstore: "/static/icons/appstore.svg",
  github: "/static/icons/github.svg",
  website: "/static/icons/website.svg"
};

fetch("/api/projects")
  .then(res => res.json())
  .then(data => {
    const container = document.getElementById("projects");

    data.forEach(project => {
      const card = document.createElement("div");
      card.className = "project-card";

      const linksHTML = Object.entries(project.links)
        .map(([key, url]) => `
          <a href="${url}" target="_blank" class="icon-link" title="${key}">
            <img src="${iconMap[key]}" alt="${key}">
          </a>
        `)
        .join("");

      const techHTML = project.tech_stack
        .map(tech => `<span class="tech-pill">${tech}</span>`)
        .join("");

      card.innerHTML = `
        <h3>${project.title}</h3>
        <p>${project.description}</p>

        <div class="tech-stack">
          ${techHTML}
        </div>

        <div class="project-links">
          ${linksHTML}
        </div>
      `;

      container.appendChild(card);
    });
  });
