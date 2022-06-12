console.log("hello")
const sakralne=document.getElementById('Sakralne');
const pomnik=document.getElementById('Pomniki');
const zabytki=document.getElementById('Zabytki');
const muzea=document.getElementById('Muzea');
const all=document.getElementById("all");
const elemets=document.querySelectorAll('.Muzea');
const elemets2=document.querySelectorAll('.Sakralne');
const elemets3=document.querySelectorAll('.Pomniki');
const elements4=document.querySelectorAll('.Zabytki')

function show(item){
    item.classList.remove('deactive');
}
function hide(item){
    item.classList.add('deactive');
}
sakralne.addEventListener("click", function (){
    elemets.forEach(hide);
    elemets2.forEach(show);
    elemets3.forEach(hide);
    elements4.forEach(hide)
})
muzea.addEventListener("click", function (){
    elemets.forEach(show);
    elemets2.forEach(hide);
    elemets3.forEach(hide);
    elements4.forEach(hide)
})
zabytki.addEventListener("click", function (){
    elemets.forEach(hide);
    elemets2.forEach(hide);
    elemets3.forEach(hide);
    elements4.forEach(show)
})
pomnik.addEventListener("click", function (){
    elemets.forEach(hide);
    elemets2.forEach(hide);
    elemets3.forEach(show);
    elements4.forEach(hide)
})
all.addEventListener("click", function (){
    elemets.forEach(show);
    elemets2.forEach(show);
    elemets3.forEach(show);
    elements4.forEach(show)
})