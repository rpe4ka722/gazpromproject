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


function richFunction() {
    var a = document.getElementById('select_rich');
    var e = document.getElementById('rich_add');
    var b = document.getElementById('select_rich_button');
    if (a.value == "Добавить") {
         e.style.display = 'block';
         b.setAttribute("form", "rich_add");
         b.value = 'Добавить';
    }
    else {
         e.style.display = 'none';
         b.setAttribute("form", "rich_select_form");
         b.value = 'Изменить';
    }
}

function regFunction() {
    var a = document.getElementById('select_registration');
    var e = document.getElementById('registration_add');
    var b = document.getElementById('select_registration_button');
    if (a.value == "Добавить") {
         e.style.display = 'block';
         b.setAttribute("form", "registration_add");
         b.value = 'Добавить';
    }
    else {
         e.style.display = 'none';
         b.setAttribute("form", "registration_select_form");
         b.value = 'Изменить';
    }
}


function equipFunction() {
    var a = document.getElementById('select_equipment');
    var e = document.getElementById('equipment_add_form');
    var b = document.getElementById('equipment_select_button');
    if (a.value == "Добавить") {
         e.style.display = 'block';
         b.setAttribute("form", "equipment_add_form");
         b.value = 'Добавить';
    }
    else {
         e.style.display = 'none';
         b.setAttribute("form", "equipment_select_form");
         b.value = 'Изменить';
    }
}


function inventoryFunction() {
    var a = document.getElementById('select_inventory');
    var e = document.getElementById('inventory_add');
    var b = document.getElementById('select_inventory_button');
    var c = document.getElementById('add_inventory');
    if (a.value == "Добавить") {
         e.style.display = 'block';
         b.setAttribute("form", "inventory_add");
         b.value = 'Добавить';
         c.style.marginTop='320px';
    }
    else {
         e.style.display = 'none';
         b.setAttribute("form", "inventory_select_form");
         b.value = 'Изменить';
         c.style.marginTop='0';
    }
}