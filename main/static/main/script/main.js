function showhide(id) {
    var e = document.getElementById(id);
    var a = document.getElementById("filter-button-dynamic");
    e.style.display = (e.style.display == 'block') ? 'none' : 'block';
    a.value = (a.value == "Скрыть фильтр") ? "Фильтр" : "Скрыть фильтр";
}

function showhide_changeform(id) {
    var e = document.getElementById(id);
    e.style.display = (e.style.display == 'block') ? 'none' : 'block';
}
