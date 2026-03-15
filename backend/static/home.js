// Intro text animation
const words = ["Hi", "I", "am", "Mohit"];
const container = document.getElementById("intro-text");
let index = 0;

function showNextWord() {
    container.innerHTML = "";

    if (index < words.length - 1) {
    const span = document.createElement("span");
    span.className = "intro-word";
    span.textContent = words[index];
    container.appendChild(span);
    index++;
    setTimeout(showNextWord, 900);
    } else {
    const span = document.createElement("span");
    span.className = "final-name";
    span.textContent = words[index];
    container.appendChild(span);
    }
}

showNextWord();

// Scroll reveal for about cards
const cards = document.querySelectorAll('.about-card');

const observer = new IntersectionObserver(
    (entries) => {
    entries.forEach((entry) => {
        if (entry.isIntersecting) {
        entry.target.classList.add('show');
        }
    });
    },
    { threshold: 0.2 }
);

cards.forEach((card, index) => {
    card.style.transitionDelay = `${index * 0.15}s`;
    observer.observe(card);
});

// Infinite horizontal skills scroll
const skills = [
    "HTML",
    "CSS",
    "JavaScript",
    "Python",
    "Machine Learning",
    "Computer Vision",
    "Automation",
    "Data Analysis"
];

const track = document.getElementById("skillsTrack");

[...skills, ...skills].forEach(skill => {
    const item = document.createElement("div");
    item.className = "skill-item";
    item.textContent = skill;
    track.appendChild(item);
});