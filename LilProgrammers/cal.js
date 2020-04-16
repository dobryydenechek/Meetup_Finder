var tags = document.getElementById("tags");
var buttonsave = document.getElementById("buttonsave");
var buttonedit = document.getElementById("buttonedit");
var buttonnext = document.getElementById("buttonnext");
var buttonprev = document.getElementById("buttonprev");
var month = document.getElementById("month");
var year = document.getElementById("year");
var months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"];
var cells = document.getElementById("cal").getElementsByTagName("td");
var events = {};
var cm = new Date().getMonth();
var cy = new Date().getFullYear();
var tagsdata ={};
var tagschek =[];
function getday(y, m) {
    var day = new Date(y, m, 1).getDay()
    day--
    if (day < 0) {
        day = 6
    }
    return day
}

function getmonthdays(y, m) {
    return 32 - new Date(y, m, 32).getDate();
}

function update() {
    let ida = "data-ida"
    month.innerText = months[cm];
    year.innerText = cy;
    for (let index = 0; index < cells.length; index++) {
        const cell = cells[index];
        cell.removeAttribute(ida);
        cell.innerText = "";
        cell.classList.remove("today");
        let ovs = cell.getElementsByClassName("event");
        for (let index = 0; index < ovs.length; index++) {
            const ov = ovs[index];
            cell.removeChild(ov);
        }
    }
    
    let start = getday(cy, cm);
    for (let index = start; index < getmonthdays(cy, cm) + start; index++) {
        const cell = cells[index];
        cell.innerText = index - start + 1;
        let idday = cy + "-" + (cm + 1) + "-" + (index - start + 1);
        cell.setAttribute(ida, idday);
    }
    if (cy == new Date().getFullYear() && cm == new Date().getMonth()) {
        cells[new Date().getDate() + start - 1].classList.add("today")
    }
    let promis = axios.get(`events/${cy}-${cm+1}.json`);
    promis.then(function(respons){
        for (let index = 0; index < respons.data.length; index++) {
            const event = respons.data[index];
            events[event.id]=event;
            let ne = document.createElement("span");
            ne.innerText = event.title;
            ne.classList.add("event");
            ne.setAttribute(ida, event.date);
            ne.setAttribute("data-ei",event.id)
            cells[new Date(event.date).getDate() + start - 1].appendChild(ne);
        }
        uptippy()
        filter()
    })
}

function upteg() {
    var promis = axios.get("tegs.json");
    promis.then(function (response) {
        var tags = document.getElementById("tags");
        tags.innerHTML = "";
        for (let index = 0; index < response.data.length; index++) {
            const teg = response.data[index];
            var li = document.createElement("li");
            li.classList.add("tags");
            li.setAttribute("data-id",teg.id);
            li.innerHTML = '<label class="container font"><span class="svap">     </span><input type="checkbox"><span class="checkmark"></span></label>';
            li.getElementsByClassName("svap")[0].innerText = teg.tl_title;
            tags.appendChild(li);
            tagsdata[teg.id]=teg;
        }
    })
}

function nextmonth() {
    cm++;
    if (cm > 11) {
        cm = 0;
        cy++
    }
    update();
}

function prevmonth() {
    cm--;
    if (cm < 0) {
        cm = 11;
        cy--
    }
    update();
}
function filter(){
    
    let calevents=document.getElementsByClassName("event")
    
    for (let index = 0; index < calevents.length; index++) {
        const element = calevents[index];
        element.classList.remove("hidden")
        if(!tagschek.length){
            continue
        }
        let eventdata = events[element.getAttribute("data-ei")];
        let flag =false;
        
        for (let index = 0; index < eventdata.tags.length; index++) {
            const id = eventdata.tags[index];

            for (let index = 0; index < tagschek.length; index++) {
                const chek = tagschek[index];
                if(chek==id){
                    flag=true;
                    break
                }
            }
            if (flag){break}
        }
        if(!flag){
            element.classList.add("hidden")
        }
    }
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
    tagschek=[];
    for (let index = 0; index < tags.children.length; index++) {
        const li = tags.children[index];
        const chekbox = li.getElementsByTagName("input")[0];
        if (chekbox.checked) {
            chekbox.disabled = true;
            tagschek.push(li.getAttribute("data-id"))
        } else {
            li.hidden = true
        }
    }
    buttonsave.hidden = true;
    buttonedit.hidden = false;
    filter()
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

function uptippy() {
    tippy('#cal td .event', {
        content:
     `
    <div class="detail" > 
      <h4 class="dataevent"></h4>
      <p class="time"></p>
      <p class="description"></p>
      <span class="city"></span>,
      <span class="streetname"></span>,
      <span class="houseNumber"></span>,
      <span class="letter"></span>
      <p class="placeName"></p>
      <div class="datatags"> </div>
      <button onclick="window.location='#mailing'">Я пойду</button>
    </div>
    `,
        allowHTML: true,
        arrow: true,
        trigger: 'click',
        interactive: true,
        theme: "detail",
        onShow(instance) {
            let ei = instance.reference.getAttribute("data-ei");
            let event = events[ei];
            instance.popper.getElementsByClassName("dataevent")[0].innerText = event.title;
            instance.popper.getElementsByClassName("description")[0].innerText = event.description;
            instance.popper.getElementsByClassName("time")[0].innerText = event.time;
            instance.popper.getElementsByClassName("city")[0].innerText = event.city;
            instance.popper.getElementsByClassName("streetname")[0].innerText = event.streetname;
            instance.popper.getElementsByClassName("houseNumber")[0].innerText = event.houseNumber;
            instance.popper.getElementsByClassName("letter")[0].innerText = event.letter;
            instance.popper.getElementsByClassName("placeName")[0].innerText = event.placeName;
            instance.popper.getElementsByClassName("datatags")[0].innerHTML="";
            for (let index = 0; index < event.tags.length; index++) {
                const tag = event.tags[index];
                var span = document.createElement("span");
                span.innerText = tagsdata[tag].tl_title;
                instance.popper.getElementsByClassName("datatags")[0].appendChild(span);
            }
            
        }
    });
}

upteg()
update()