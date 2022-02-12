// 修改表格行的背景色
let all_icons = {
    "folder": "imageres_3.ico",
    "docx": "docx.png",
    "doc": "docx.png",
    "xlsx": "excel.png",
    "pptx": "ppt.png",
    "mp3": "imageres_1004.ico",
    "mp4": "imageres_1005.ico",
    "avi": "imageres_1005.ico",
    "jpg": "imageres_1003.ico",
    "png": "imageres_1003.ico",
    "bmp": "imageres_1003.ico",
    "txt": "imageres_1002.ico",
    "pdf": "pdf.png"
};
refresh_folder();
function change_layout(results) {
    let layout = document.getElementById("layout").value;
    if (layout === "0") {
        document.getElementById("layout-table").style.display = "";
        document.getElementById("layout-img").style.display = "none";
        display_files(results);
        // $(".detail").innerHTML
    } else if (layout === "1") {
        document.getElementById("layout-table").style.display = "none";
        document.getElementById("layout-img").style.display = "";
        flat_img(results);
        $(".div-img").css({"width": "350px"});
        $(".checkoutbox input").css({"zoom": "230%"});
    } else if (layout === "2") {
        document.getElementById("layout-table").style.display = "none";
        document.getElementById("layout-img").style.display = "";
        flat_img(results);
        $(".div-img").css({"width": "200px"});
        $(".checkoutbox input").css({"zoom": "150%"});
    } else if (layout === "3") {
        document.getElementById("layout-table").style.display = "none";
        document.getElementById("layout-img").style.display = "";
        flat_img(results);
        $(".div-img").css({"width": "100px"});
        $(".checkoutbox input").css({"zoom": "100%"});
    }
}

function textarea_onfocus(taa) {
    console.log(taa);
}
function textarea_mouseout(file_id, file_type) {
    let file_name = document.getElementById(file_id).value;
    if (file_type === 'folder') {
        rename(file_name, file_id, 'folder/rename');
    } else {
        rename(file_name, file_id, 'file/rename');
    }
}

function create_folder() {
    let folder_id = document.getElementById("current_path").getAttribute("name");
    if (!folder_id) {
        folder_id = 520;
    }
    connect_modal(folder_id, '新建文件夹', 'folder/create');
}
function rename_folder(folder_id) {
    connect_modal(folder_id, '重命名文件夹', 'folder/rename');
}
function rename_file(file_id) {
    connect_modal(file_id, '重命名文件', 'file/rename');
}
function connect_modal(folder_id, name, url) {
    document.getElementById('title-name').innerText = name;
    let modal = document.getElementById('myModal');
    let close_a = document.getElementsByClassName("close")[0];
    let cancel_a = document.getElementsByClassName("cancel")[0];
    let submit_a = document.getElementsByClassName("submit")[0];

    modal.style.display = "block";

    close_a.onclick = function() {
        modal.style.display = "none";
    }
    cancel_a.onclick = function() {
        modal.style.display = "none";
    }

    submit_a.onclick = function() {
        let folder_name = document.getElementById("folder_name").value;

        if (!folder_name) {
            $.Toast('请填写文件夹名称哦 ~ ', 'error');
            return;
        }

        rename(folder_name, folder_id, url);
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    }
}
function rename(folder_name, folder_id, url) {
    let post_data = {
        name: folder_name,
        id: folder_id
    }

    $.ajax({
        type: "POST",
        url: url,
        data: post_data,
        dataType: "json",
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                document.getElementById("folder_name").value = "";
                refresh_folder();
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}
function get_root_folder() {
    document.getElementById("current_path").setAttribute("name", "520");
    document.getElementById("current_path").setAttribute("value", "");
    let sorted_type = document.getElementById("sort_type").value;
    let sorted = document.getElementById("sorted").value;
    get_files("520", sorted, sorted_type);
}
function click_folder(folder_id, name) {
    let current_path = document.getElementById("current_path").getAttribute("value");
    let sorted_type = document.getElementById("sort_type").value;
    let sorted = document.getElementById("sorted").value;
    document.getElementById("current_path").setAttribute("name", folder_id);

    if (!name) {
        document.getElementById("current_path").setAttribute("value", "");
    } else {
        document.getElementById("current_path").setAttribute("value", current_path + '/' + name);
    }
    get_files(folder_id, sorted, sorted_type);
}
function refresh_folder() {
    let folder_id = document.getElementById("current_path").getAttribute("name");
    let sorted_type = document.getElementById("sort_type").value;
    let sorted = document.getElementById("sorted").value;
    get_files(folder_id, sorted, sorted_type);
}
function get_files(folder_id, sorted, sorted_type) {
    let post_data = {
        id: folder_id,
        sorted: sorted,
        sorted_type: sorted_type
    };

    $.ajax({
        type: "POST",
        url: "getFiles",
        data: post_data,
        dataType: "json",
        success: function (data) {
            if (data['code'] === 0) {
                // $.Toast(data['msg'], 'success');
                change_layout(data['data']);
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}

function recent_file() {
    $.ajax({
        type: "GET",
        url: "getRecentFiles",
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                display_files(data['data']);
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}

function display_files(results) {
    let s = "";
    for (let i=0; i<results.length; i++) {
        if (results[i]['model'] === "myfiles.catalog") {
            s = s + '<tr><td style="text-align: center;"><input type="checkbox"></td>';
            s = s + '<td onclick="click_folder(\'' + results[i]['pk'] + '\',\'' + results[i]['fields']['name'] + '\')"><img src="static/img/' + all_icons['folder'] + '">' + results[i]['fields']['name'] + '</td><td></td><td>文件夹</td>';
            s = s + '<td>' + results[i]['fields']['create_time'].replace('T', ' ') + '</td>';
            s = s + '<td>' + results[i]['fields']['update_time'].replace('T', ' ') + '</td>';
            s = s + '<td><button class="actions" onclick="rename_folder(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions">移动</button><button class="actions" onclick="delete_folder(\'' + results[i]['pk'] + '\')">删除</button></td></tr>';
        }
        if (results[i]['model'] === "myfiles.files") {
            s = s + '<tr><td style="text-align: center;"><input type="checkbox"></td>';
            s = s + '<td><img src="static/img/' + all_icons[results[i]['fields']['format']] + '">' + results[i]['fields']['name'] + '</td>';
            s = s + '<td>' + results[i]['fields']['size'] + ' KB</td>';
            s = s + '<td>' + results[i]['fields']['format'] + '</td>';
            s = s + '<td>' + results[i]['fields']['create_time'].replace('T', ' ') + '</td>';
            s = s + '<td>' + results[i]['fields']['update_time'].replace('T', ' ') + '</td>';
            s = s + '<td><button class="actions" onclick="rename_file(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions">下载</button><button class="actions">移动</button><button class="actions" onclick="delete_file(\'' + results[i]['pk'] + '\')">删除</button></td></tr>';
        }
    }
    document.getElementById("tbody").innerHTML = s;
}
function flat_img(results) {
    let s = "";
    let type_icon = 'folder';
    for (let i=0; i<results.length; i++) {
        if (results[i]['model'] === "myfiles.catalog") {type_icon = 'folder';}
        if (results[i]['model'] === "myfiles.files") {type_icon = results[i]['fields']['format'];}
        s = s + '<div class="div-img"><div><img src="/static/img/' + all_icons[type_icon] + '"></div><div class="checkoutbox"><input type="checkbox"></div>';
        s = s + '<textarea id="' + results[i]['pk'] + '" name="' + type_icon + '" onfocusout="textarea_mouseout(this.id, this.name)" title="' + results[i]['fields']['name'] + '">'+ results[i]['fields']['name'] +'</textarea></div>';
    }
    document.getElementById("layout-img").innerHTML = s;
}

function delete_folder(folder_id) {
    $.ajax({
        type: "GET",
        url: "folder/delete?id=" + folder_id,
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                refresh_folder();
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}
function delete_file(file_id) {
    $.ajax({
        type: "GET",
        url: "file/delete?id=" + file_id,
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                refresh_folder();
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}
function search_file() {
    let word = document.getElementById("search").value;
    $.ajax({
        type: "GET",
        url: "file/search?key_word=" + word,
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                let s = "";
                let results = data['data'];
                for (let i=0; i<results.length; i++) {
                    if (results[i]['model'] === "myfiles.catalog") {
                        s = s + '<tr><td style="text-align: center;"><input type="checkbox"></td>';
                        s = s + '<td onclick="click_folder(\'' + results[i]['pk'] + '\',\'' + results[i]['fields']['name'] + '\')"><img src="static/img/' + all_icons['folder'] + '">' + results[i]['fields']['name'] + '</td><td></td><td>文件夹</td>';
                        s = s + '<td>' + results[i]['fields']['create_time'].replace('T', ' ') + '</td>';
                        s = s + '<td>' + results[i]['fields']['update_time'].replace('T', ' ') + '</td>';
                        s = s + '<td><button class="actions" onclick="rename_folder(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions">移动</button><button class="actions" onclick="delete_folder(\'' + results[i]['pk'] + '\')">删除</button><button class="actions" onclick="find_origin_path(\'' + results[i]['pk'] + '\')">文件位置</button></td></tr>';
                    }
                    if (results[i]['model'] === "myfiles.files") {
                        s = s + '<tr><td style="text-align: center;"><input type="checkbox"></td>';
                        s = s + '<td><img src="static/img/' + all_icons[results[i]['fields']['format']] + '">' + results[i]['fields']['name'] + '</td>';
                        s = s + '<td>' + results[i]['fields']['size'] + ' KB</td>';
                        s = s + '<td>' + results[i]['fields']['format'] + '</td>';
                        s = s + '<td>' + results[i]['fields']['create_time'].replace('T', ' ') + '</td>';
                        s = s + '<td>' + results[i]['fields']['update_time'].replace('T', ' ') + '</td>';
                        s = s + '<td><button class="actions" onclick="rename_file(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions">下载</button><button class="actions">移动</button><button class="actions" onclick="delete_file(\'' + results[i]['pk'] + '\')">删除</button><button class="actions" onclick="find_origin_path(\'' + results[i]['fields']['parent'] + '\')">文件位置</button></td></tr>';
                    }
                }
                document.getElementById("tbody").innerHTML = s;
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}

function find_origin_path(file_id) {
    $.ajax({
        type: "GET",
        url: "findOriginPath?id=" + file_id,
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                alert('文件所在目录：' + data['data']);
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}

function return_folder() {
    let folder_id = document.getElementById("current_path").getAttribute("name");
    let folder_name = document.getElementById("current_path").getAttribute("value");
    if (folder_id === '520') {
        return;
    }
    $.ajax({
        type: "GET",
        url: "folder/return?id=" + folder_id + "&name=" + folder_name,
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                document.getElementById("current_path").setAttribute("name", data['data']['id']);
                document.getElementById("current_path").setAttribute("value", data['data']['name']);
                refresh_folder();
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}
