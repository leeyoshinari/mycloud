let testEditor = editormd("editormd", {
        width  : "90%",
        height : 720,
        path   : '../static/editor.md/lib/',
        toolbar_autofixed: true,
        codeFold: true,
        searchReplace: true,
        emoji: true,
        sequenceDiagram: true,
        taskList: true,
        tocm: true,
        // tex: true,
        flowChart: true,
        htmlDecode: "style,script,iframe",
        saveHTMLToTextarea: true,
        imageUpload: true,
        imageFormats: ["jpg", "jpeg", "png", "bmp", "gif"],
    });
testEditor.onload = function () {
    console.log(testEditor.getMarkdown());
}