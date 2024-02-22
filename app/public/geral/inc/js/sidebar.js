let arrow = document.querySelectorAll(".bi-caret-down-fill");
for (var i = 0; i < arrow.length; i++) {
  arrow[i].addEventListener("click", (e)=>{
 let arrowParent = e.target.parentElement.parentElement;//selecting main parent of arrow
 arrowParent.classList.toggle("showMenu");
});
}
let sidebar = document.querySelector(".sidebar");
let sidebarBtn = document.querySelector(".logotype");
sidebarBtn.addEventListener("click", ()=>{
  sidebar.classList.toggle("close");
});