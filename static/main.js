const PAGES = ["about_us", "get_to_know_me", "blog", "scheduling", "take_a_breath", "upcoming_projects"];
const PAGE_NAMES = ["About Us", "Get to Know Me", "Blog", "Scheduling", "Take a Breath", "Upcoming Projects"];

window.onload = function() {
    main();
}

function main() {
    let nav = document.getElementById("nav");
    for (var i = 0; i < PAGES.length; i += 1) {
        let link = document.createElement("span");
        link.setAttribute("class", "nav_link");
        link.setAttribute("id", "" + i);
        link.innerText = PAGE_NAMES[i];
        link.onclick = function(element) {
            navigate(element);
        }
        nav.appendChild(link);
    }
}

function navigate(element) {
    window.location.replace("/" + PAGES[parseInt(element.srcElement.getAttribute("id"))].replaceAll("_", "-"));
}