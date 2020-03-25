
var tags = document.getElementById("tags");
var buttonsave = document.getElementById("buttonsave");
var buttonedit = document.getElementById("buttonedit");
var buttonnext = document.getElementById("buttonnext");
var buttonprev = document.getElementById("buttonprev");
var month = document.getElementById("month");
var year = document.getElementById("year");
var months = ["Январь","Февраль","Март","Апрель","Май","Июнь","Июль","Август","Сентябрь","Октябрь","Ноябрь","Декабрь"];
var cells =document.getElementById("cal").getElementsByTagName("td"); 
var events ={};

var cm = new Date().getMonth();
var cy = new Date().getFullYear()




function getday(y,m){
    var day = new Date(y,m,1).getDay()
    day--
    if(day<0){
        day=6
    }
    return day
}

function getmonthdays (y,m){
    return 32 - new Date(y,m, 32).getDate();
    }
function update(){
    month.innerText=months[cm];
    year.innerText=cy;
    for (let index = 0; index < cells.length; index++) {
        const cell = cells[index];
        cell.innerText=""
        cell.classList.remove("today")
        let ovs = cell.getElementsByClassName("event")
        for (let index = 0; index < ovs.length; index++) {
            const ov = ovs[index];
            cell.removeChild(ov)
        }
    }
    let start =getday(cy,cm)
    for (let index = start; index < getmonthdays(cy,cm)+start; index++) {
        const cell = cells[index];
        cell.innerText=index-start+1;
        let ov = events[cy+"-"+(cm+1)+"-"+(index-start+1)]
        if(ov){
            for (let index = 0; index <Math.min( 3,ov.length); index++) {
                const element = ov[index];
                var ne =document.createElement("span");
                ne.innerText=element.name;
                ne.classList.add("event")
                cell.appendChild(ne)
            }
        }
    }
    if(cy==new Date().getFullYear() && cm==new Date().getMonth()){
        cells[ new Date().getDate()+start-1].classList.add("today")
    }
}





function nextmonth(){
    cm++;
    if(cm>11){
        cm=0;
        cy++
    }
    update();
}
function prevmonth(){
    cm--;
    if(cm<0){
        cm=11;
        cy--
    }
    update();
}


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




events["2020-3-17"]=[{name:"dfgdfgfdsg dfgfdg fdgdf gdfg dfg df"},
{name:"6546879356846516 8796465 4968746 84634596874"}];
update()