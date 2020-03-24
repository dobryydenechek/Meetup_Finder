var tags = document.getElementById("tags");
var buttonsave = document.getElementById("buttonsave");
var buttonedit = document.getElementById("buttonedit");

function save() {


    var chek = 0;
    for (let index = 0; index < tags.children.length; index++) {
        const li = tags.children[index];
        if (li.getElementsByTagName("input")[0].checked) {
            chek++
            break
        }
    }
    if (!chek) {
        alert("Иди нахуй с такими тегами");
        return
    }
    for (let index = 0; index < tags.children.length; index++) {
        const li = tags.children[index];
        const chekbox = li.getElementsByTagName("input")[0];
        if (chekbox.checked) {
            chekbox.disabled = true;
        } else {
            li.hidden = true

        }
    }
    buttonsave.hidden = true;
    buttonedit.hidden = false;
}

function edit() {
    for (let index = 0; index < tags.children.length; index++) {
        const li = tags.children[index];
        const chekbox = li.getElementsByTagName("input")[0];
        chekbox.disabled = false;
        li.hidden = false;
    }
    buttonsave.hidden = false;
    buttonedit.hidden = true;
}