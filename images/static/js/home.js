// 修改表格行的背景色
flat_img();
function change_layout() {
    let layout = document.getElementById("layout").value;
    if (layout === "0") {
        document.getElementById("layout-table").style.display = "";
        // $(".detail").innerHTML
    } else if (layout === "1") {
        document.getElementById("layout-table").style.display = "none";
    } else if (layout === "2") {
        document.getElementById("layout-table").style.display = "none";
    } else if (layout === "3") {
        document.getElementById("layout-table").style.display = "none";
    }
}

function flat_img() {
    let s = "";
    for (let i=0; i<20; i++) {
        s = s + '<div><img src=\"/static/img/excel.png\"><p>sssssssss';
        s = s + i + '.png</p></div>';
    }
    document.getElementById("layout-img").innerHTML = s;
}