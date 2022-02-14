// 修改表格行的背景色
let all_icons = {
    "folder": "imageres_3.ico",
    "docx": "docx.png",
    "xlsx": "excel.png",
    "pptx": "ppt.png",
    "mp3": "imageres_1004.ico",
    "mp4": "imageres_1005.ico",
    "jpg": "imageres_1003.ico",
    "txt": "imageres_1002.ico",
    "pdf": "pdf.png"
};
let folder_window = '<div class="modal-content"><div class="modal-header"><span class="close">&times;</span><h2 id="title-name">新建文件夹</h2></div><div class="modal-body"><div><label>名称：</label><input id="folder_name" type="text" placeholder="请输入名称"></div></div><div class="modal-footer"><a class="cancel">取消</a><a class="submit">确定</a></div></div>';
let move_folder = '<div class="move-content"><div class="modal-header"><span class="close">&times;</span><h2 id="title-name">移动文件</h2></div><div class="modal-body"><div><label>移动到目录：</label><input id="folder_name" type="text" placeholder="请选择目标目录" value="/" name="520" readonly></div><div><label>选择目录：</label><div id="folder-tree"><ul class="domtree"><li onclick="get_folders(\'520\')">/</li><ul id="520"></ul></ul></div></div></div><div class="modal-footer"><a class="cancel">取消</a><a class="submit">确定</a></div></div>'
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
    document.getElementById("myModal").innerHTML = folder_window;
    let folder_id = document.getElementById("current_path").getAttribute("name");
    if (!folder_id) {
        folder_id = 520;
    }
    connect_modal(folder_id, '新建文件夹', 'folder/create');
}
function rename_folder(folder_id) {
    document.getElementById("myModal").innerHTML = folder_window;
    connect_modal(folder_id, '重命名文件夹', 'folder/rename');
}
function rename_file(file_id) {
    document.getElementById("myModal").innerHTML = folder_window;
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
        modal.innerHTML = '';
        modal.style.display = "none";
    }
    cancel_a.onclick = function() {
        modal.innerHTML = '';
        modal.style.display = "none";
    }

    submit_a.onclick = function() {
        let folder_name = document.getElementById("folder_name").value;

        if (!folder_name) {
            $.Toast('请填写文件夹名称哦 ~ ', 'error');
            return;
        }

        rename(folder_name, folder_id, url);
        modal.innerHTML = '';
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.innerHTML = '';
            modal.style.display = "none";
        }
    }
}
function move_to_folder(file_id, file_type) {
    let modal = document.getElementById('moving');
    modal.innerHTML = move_folder;
    let close_a = document.getElementsByClassName("close")[0];
    let cancel_a = document.getElementsByClassName("cancel")[0];
    let submit_a = document.getElementsByClassName("submit")[0];

    get_folders('520');

    modal.style.display = "block";

    close_a.onclick = function() {
        modal.innerHTML = '';
        modal.style.display = "none";
    }
    cancel_a.onclick = function() {
        modal.innerHTML = '';
        modal.style.display = "none";
    }

    submit_a.onclick = function() {
        let to_id = document.getElementById("folder_name").name;
        let post_data = {
            from_id: file_id,
            to_id: to_id,
            move_type: file_type
        }
        $.ajax({
            type: "POST",
            url: "folder/move",
            data: post_data,
            dataType: "json",
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

        modal.innerHTML = '';
        modal.style.display = "none";
    }

    window.onclick = function(event) {
        if (event.target === modal) {
            modal.innerHTML = '';
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
                refresh_folder();
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}
function get_root_folder() {
    // 重置文件夹id
    document.getElementById("current_path").setAttribute("name", "520");
    // 重置文件路径
    document.getElementById("current_path").setAttribute("value", "");
    // 重置查询文件格式
    document.getElementById("search").setAttribute("name", "");
    let sorted_type = document.getElementById("sort_type").value;
    let sorted = document.getElementById("sorted").value;
    get_files("520", sorted, sorted_type, 1, '', 'file/get');
}
function click_folder(folder_id, name) {
    let current_path = document.getElementById("current_path").getAttribute("value");
    let sorted_type = document.getElementById("sort_type").value;
    let sorted = document.getElementById("sorted").value;
    document.getElementById("current_path").setAttribute("name", folder_id);

    if (!name) {
        document.getElementById("current_path").setAttribute("value", "");
    } else {
        if (current_path) {
            document.getElementById("current_path").setAttribute("value", current_path + ' > ' + name);
        } else {
            document.getElementById("current_path").setAttribute("value", name);
        }
    }
    get_files(folder_id, sorted, sorted_type, 1, '', 'file/get');
}
function refresh_folder(page_num) {
    let folder_id = document.getElementById("current_path").getAttribute("name");
    let file_format = document.getElementById("search").getAttribute("name");
    let sorted_type = document.getElementById("sort_type").value;
    let sorted = document.getElementById("sorted").value;
    if (file_format) {
        get_files(folder_id, sorted, sorted_type, page_num, file_format, 'file/getByFormat');
    }
    else {
        get_files(folder_id, sorted, sorted_type, page_num, file_format, 'file/get');
    }
}
function get_files(folder_id, sorted, sorted_type, page_num, file_format, url) {
    let page_size = 20;
    let layout = document.getElementById("layout").value;
    if (layout === '1') {page_size = 12;}
    if (layout === '2') {page_size = 21;}
    if (layout === '3') {page_size = 50;}
    let post_data = {
        id: folder_id,
        page: page_num,
        format: file_format,
        page_size: page_size,
        sorted: sorted,
        sorted_type: sorted_type
    };

    $.ajax({
        type: "POST",
        url: url,
        data: post_data,
        dataType: "json",
        success: function (data) {
            if (data['code'] === 0) {
                // $.Toast(data['msg'], 'success');
                change_layout(data['data']['data']);
                PagingManage($('#paging'), data['data']['total_page'], data['data']['page'], 'refresh_folder(')
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}

function recent_file() {
    // 重置文件夹id
    document.getElementById("current_path").setAttribute("name", "520");
    // 重置文件路径
    document.getElementById("current_path").setAttribute("value", "");
    // 重置查询文件格式
    document.getElementById("search").setAttribute("name", "");

    let page_size = 20;
    let layout = document.getElementById("layout").value;
    if (layout === '1') {page_size = 12;}
    if (layout === '3') {page_size = 50;}
    $.ajax({
        type: "GET",
        url: "file/get/recent?page=" + page_size,
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                change_layout(data['data']);
                $('#paging').html('');
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
            s = s + '<td><button class="actions" onclick="rename_folder(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions" onclick="move_to_folder(\'' + results[i]['pk'] + '\', \'folder\')">移动</button><button class="actions" onclick="delete_folder(\'' + results[i]['pk'] + '\')">删除</button></td></tr>';
        }
        if (results[i]['model'] === "myfiles.files") {
            s = s + '<tr><td style="text-align: center;"><input type="checkbox"></td>';
            s = s + '<td><img src="static/img/' + all_icons[results[i]['fields']['format']] + '">' + results[i]['fields']['name'] + '</td>';
            s = s + '<td>' + results[i]['fields']['size'] + ' KB</td>';
            s = s + '<td>' + results[i]['fields']['format'] + '</td>';
            s = s + '<td>' + results[i]['fields']['create_time'].replace('T', ' ') + '</td>';
            s = s + '<td>' + results[i]['fields']['update_time'].replace('T', ' ') + '</td>';
            s = s + '<td><button class="actions" onclick="rename_file(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions">下载</button><button class="actions" onclick="move_to_folder(\'' + results[i]['pk'] + '\', \'file\')">移动</button><button class="actions" onclick="delete_file(\'' + results[i]['pk'] + '\')">删除</button></td></tr>';
        }
    }
    document.getElementById("tbody").innerHTML = s;
}
function flat_img(results) {
    let s = "";
    let type_icon = 'folder';
    for (let i=0; i<results.length; i++) {
        if (results[i]['model'] === "myfiles.catalog") {
            s = s + '<div class="div-img"><div onclick="click_folder(\'' + results[i]['pk'] + '\',\'' + results[i]['fields']['name'] + '\')"><img src="/static/img/' + all_icons['folder'] + '"></div><div class="checkoutbox"><input type="checkbox"></div>';
            s = s + '<textarea id="' + results[i]['pk'] + '" name="' + type_icon + '" onfocusout="textarea_mouseout(this.id, this.name)" title="' + results[i]['fields']['name'] + '">'+ results[i]['fields']['name'] +'</textarea></div>';
        }
        if (results[i]['model'] === "myfiles.files") {
            s = s + '<div class="div-img"><div><img src="/static/img/' + all_icons[results[i]['fields']['format']] + '"></div><div class="checkoutbox"><input type="checkbox"></div>';
            s = s + '<textarea id="' + results[i]['pk'] + '" name="' + type_icon + '" onfocusout="textarea_mouseout(this.id, this.name)" title="' + results[i]['fields']['name'] + '">' + results[i]['fields']['name'] + '</textarea></div>';
        }
    }
    document.getElementById("layout-img").innerHTML = s;
}

function delete_folder(folder_id) {
    let answer = confirm('确定删除文件夹吗？');
    if (!answer) {
        return;
    }
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
    let answer = confirm('确定删除文件吗？');
    if (!answer) {
        return;
    }
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
function search_file(page_num) {
    let word = document.getElementById("search").value.trim();
    if (!word) {
        $.Toast('请输入搜索关键字词', 'warning');
        return;
    }
    // 重置文件夹id
    document.getElementById("current_path").setAttribute("name", "520");
    // 重置文件路径
    document.getElementById("current_path").setAttribute("value", "");
    let page_size = 20;
    let layout = document.getElementById("layout").value;
    if (layout === '1') {page_size = 12;}
    if (layout === '2') {page_size = 21;}
    if (layout === '3') {page_size = 50;}
    let post_data = {
        key_word: word,
        page: page_num,
        page_size: page_size
    }
    $.ajax({
        type: "POST",
        url: "file/search",
        data: post_data,
        dataType: "json",
        success: function (data) {
            if (data['code'] === 0) {
                $.Toast(data['msg'], 'success');
                let s = "";
                let results = data['data']['data'];
                for (let i=0; i<results.length; i++) {
                    if (results[i]['model'] === "myfiles.catalog") {
                        s = s + '<tr><td style="text-align: center;"><input type="checkbox"></td>';
                        s = s + '<td onclick="click_folder(\'' + results[i]['pk'] + '\',\'' + results[i]['fields']['name'] + '\')"><img src="static/img/' + all_icons['folder'] + '">' + results[i]['fields']['name'] + '</td><td></td><td>文件夹</td>';
                        s = s + '<td>' + results[i]['fields']['create_time'].replace('T', ' ') + '</td>';
                        s = s + '<td>' + results[i]['fields']['update_time'].replace('T', ' ') + '</td>';
                        s = s + '<td><button class="actions" onclick="rename_folder(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions" onclick="move_to_folder(\'' + results[i]['pk'] + '\', \'file\')">移动</button><button class="actions" onclick="delete_folder(\'' + results[i]['pk'] + '\')">删除</button><button class="actions" onclick="find_origin_path(\'' + results[i]['pk'] + '\')">文件位置</button></td></tr>';
                    }
                    if (results[i]['model'] === "myfiles.files") {
                        s = s + '<tr><td style="text-align: center;"><input type="checkbox"></td>';
                        s = s + '<td><img src="static/img/' + all_icons[results[i]['fields']['format']] + '">' + results[i]['fields']['name'] + '</td>';
                        s = s + '<td>' + results[i]['fields']['size'] + ' KB</td>';
                        s = s + '<td>' + results[i]['fields']['format'] + '</td>';
                        s = s + '<td>' + results[i]['fields']['create_time'].replace('T', ' ') + '</td>';
                        s = s + '<td>' + results[i]['fields']['update_time'].replace('T', ' ') + '</td>';
                        s = s + '<td><button class="actions" onclick="rename_file(\'' + results[i]['pk'] + '\')">重命名</button><button class="actions">下载</button><button class="actions" onclick="move_to_folder(\'' + results[i]['pk'] + '\', \'file\')">移动</button><button class="actions" onclick="delete_file(\'' + results[i]['pk'] + '\')">删除</button><button class="actions" onclick="find_origin_path(\'' + results[i]['fields']['parent'] + '\')">文件位置</button></td></tr>';
                    }
                }
                document.getElementById("tbody").innerHTML = s;
                PagingManage($('#paging'), data['data']['total_page'], data['data']['page'], 'search_file(')
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}

function find_origin_path(folder_id, is_return) {
    $.ajax({
        type: "GET",
        url: "folder/getPath?id=" + folder_id,
        success: function (data) {
            if (data['code'] === 0) {
                if (is_return) {
                    let full_path = data['data'];
                    if (full_path === '当前文件在根目录') {full_path = '/';}
                    document.getElementById("folder_name").setAttribute("value", full_path);
                    document.getElementById("folder_name").setAttribute("name", folder_id);
                } else {
                    $.Toast(data['msg'], 'success');
                    alert('文件路径：' + data['data']);
                }
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

function files_format(file_format) {
    document.getElementById("search").setAttribute("name", file_format);
    // 重置文件夹id
    document.getElementById("current_path").setAttribute("name", "520");
    // 重置文件路径
    document.getElementById("current_path").setAttribute("value", "");
    refresh_folder();
}

function get_folders(folder_id) {
    find_origin_path(folder_id, 'folder');
    $.ajax({
        type: "GET",
        url: "folder/get?id=" + folder_id,
        success: function (data) {
            if (data['code'] === 0) {
                let s = '';
                for (let i=0; i<data['data'].length; i++) {
                    s = s + '<li onclick="get_folders(\'' + data['data'][i]['pk'] + '\')">' + data['data'][i]['fields']['name'] + '</li><ul id="' + data['data'][i]['pk'] + '"></ul>'
                }
                document.getElementById(folder_id).innerHTML = s;
            } else {
                $.Toast(data['msg'], 'error');
                return;
            }
        }
    })
}

function upload_file() {
    let fileUpload_input = document.getElementById("fileUpload-input");
    fileUpload_input.click();

    fileUpload_input.onchange = function (event) {
        document.getElementById("fileUpload-form").submit();
        let files = event.target.files;
        console.log(files);
        console.log(files[0].size)
    }
}
