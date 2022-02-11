// 修改表格行的背景色
flat_img();
function change_layout() {
    let layout = document.getElementById("layout").value;
    if (layout === "0") {
        document.getElementById("layout-table").style.display = "";
        document.getElementById("layout-img").style.display = "none";
        // $(".detail").innerHTML
    } else if (layout === "1") {
        document.getElementById("layout-table").style.display = "none";
        document.getElementById("layout-img").style.display = "";
        $(".div-img").css({"width": "350px"});
    } else if (layout === "2") {
        document.getElementById("layout-table").style.display = "none";
        document.getElementById("layout-img").style.display = "";
        $(".div-img").css({"width": "200px"});
    } else if (layout === "3") {
        document.getElementById("layout-table").style.display = "none";
        document.getElementById("layout-img").style.display = "";
        $(".div-img").css({"width": "100px"});
    }
}

function flat_img() {
    let s = "";
    for (let i=0; i<20; i++) {
        s = s + '<div class="div-img"><img src=\"/static/img/excel.png\"><textarea title="sssssssssssssss">dddddddss';
        s = s + i + '.png</textarea></div>';
    }
    document.getElementById("layout-img").innerHTML = s;
}