
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
    let ida = "data-ida"
    month.innerText=months[cm];
    year.innerText=cy;
    for (let index = 0; index < cells.length; index++) {
        const cell = cells[index];
        cell.removeAttribute(ida);
        cell.innerText="";
        cell.classList.remove("today");
        let ovs = cell.getElementsByClassName("event");
        for (let index = 0; index < ovs.length; index++) {
            const ov = ovs[index];
            cell.removeChild(ov);
        }
    }

    let start =getday(cy,cm)
    for (let index = start; index < getmonthdays(cy,cm)+start; index++) {
        const cell = cells[index];
        cell.innerText=index-start+1;
        let idday =cy+"-"+(cm+1)+"-"+(index-start+1);
        cell.setAttribute(ida,idday);
        let ov = events[idday];
        if(ov){
            for (let index = 0; index <ov.length; index++) {
                const element = ov[index];
                var ne =document.createElement("span");
                ne.innerText=element.name;
                ne.classList.add("event");
                ne.setAttribute(ida,idday);
                ne.setAttribute("data-ei",index)
                cell.appendChild(ne);
            }
            uptippy()
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

//
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
//


/*for (let index = 0; index < cells.length; index++) {
    const cell = cells[index];
    Popper.createPopper(cell,document.getElementById("detail"))
}
tippy('#cal td', {
    content:document.getElementById("detail").innerHTML,
    allowHTML: true,
    arrow:true,
    trigger: 'click',
    interactive: true,
    theme:"detail",
    onShow(instance){
        let ida =instance.reference.getAttribute("data-ida");
        console.log(instance);
        if(!ida){
            return false
        }
        instance.popper.getElementsByClassName("dataday")[0].innerText=new Date(ida).toLocaleDateString(undefined,{weekday:"long",year:"numeric",month:"long",day:"numeric"});
        let dayevent = events[ida];
        let dataevents =instance.popper.getElementsByClassName("dataevents")[0];
        dataevents.innerHTML="";

        for (let index = 0; index < dayevent.length; index++) {
            const event = dayevent[index];
            var ne =document.createElement("li");
            ne.innerText=event.name;
            dataevents.appendChild(ne)
        }
    }

  });*/
function uptippy(){
  tippy('#cal td .event', {
    content:document.getElementById("eventdetail").innerHTML,
    allowHTML: true,
    arrow:true,
    trigger: 'click',
    interactive: true,
    theme:"detail",
    onShow(instance){
        let ida =instance.reference.getAttribute("data-ida");
        let ei =instance.reference.getAttribute("data-ei");
        let event = events[ida][ei];
        instance.popper.getElementsByClassName("dataevent")[0].innerText=event.name;
       
    }

  });}
events["2020-3-17"]=[{name:"НАзвание мероприятия"},
{name:"Php Meetup"}];

update()