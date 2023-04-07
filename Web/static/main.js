function sendTxtToServer() {
    var songTitle = $("#song_title_input").val();
    var singer = $("#singer_input").val();
    var lyrics = $("#lyrics_input").val();

    $.ajax({
        url: "/save_txt",
        method: "POST",
        data: {
            song_title: songTitle,
            singer: singer,
            lyrics: lyrics,
        },
        success: function (response) {
            console.log(response);
        },
        error: function (error) {
            console.error("Error:", error);
        }
    });
}

function updatePreviewImage() {
    var timestamp = new Date().getTime();
    $("#right img").attr("src", "/preview_image?timestamp=" + timestamp);
    
}

function checkImageUpdate() {
    var previewImage = document.getElementById("preview-image");
    var xhr = new XMLHttpRequest();
    xhr.open("HEAD", previewImage.src, true);
    xhr.onreadystatechange = function () {
        if (xhr.readyState == 4) {
            var lastModified = xhr.getResponseHeader("Last-Modified");
            if (previewImage.dataset.lastModified !== lastModified) {
                previewImage.src = previewImage.src.split("?")[0] + "?timestamp=" + new Date().getTime();
                previewImage.dataset.lastModified = lastModified;
            }
        }
    };
    xhr.send(null);
}


$(document).ready(function () {
    $("#btn_select_bg").click(function () {
        $("#select_bg").click();
    });
    $("#select_bg").on("change", function () {
            var file = this.files[0];
            var formData = new FormData();
            formData.append("file", file);
    
            $.ajax({
                url: "/upload_bg",
                method: "POST",
                data: formData,
                processData: false,
                contentType: false,
                success: function (response) {
                    console.log(response);
                },
                error: function (error) {
                    console.error("Error:", error);
                },
            });
    
            var reader = new FileReader();
            reader.onload = function (e) {
                $("#bg img").attr("src", e.target.result);
            };
            reader.readAsDataURL(file);
        });

    $("#btn_select_cover").click(function () {
        $("#select_cover").click();
    });
    $("#select_cover").on("change", function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append("file", file);
    
        $.ajax({
            url: "/upload_cover",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.error("Error:", error);
            },
        });
    
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#cover img").attr("src", e.target.result);
        };
        reader.readAsDataURL(file);
    });
    
    $("#btn_select_font").click(function () {
        $("#select_font").click();
        
    });
    $("#select_font").on("change", function () {
        var file = this.files[0];
        var formData = new FormData();
        formData.append("file", file);

        $.ajax({
            url: "/upload_font",
            method: "POST",
            data: formData,
            processData: false,
            contentType: false,
            success: function (response) {
                console.log(response);
            },
            error: function (error) {
                console.error("Error:", error);
            },
        });
        reader.readAsDataURL(file);
    });

    $("#select_bg").change(function () {
        var file = this.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#bg img").attr("src", e.target.result);
        };
        reader.readAsDataURL(file);
    });
    
    $("#select_cover").change(function () {
        var file = this.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
            $("#cover img").attr("src", e.target.result);
        };
        eader.readAsDataURL(file);
    });
    
    $("#select_font").change(function () {
        var file = this.files[0];
        var reader = new FileReader();
        reader.onload = function (e) {
        var fontName = "custom_font";
        var fontFace = new FontFace(fontName, e.target.result);
        fontFace.load().then(function () {
            document.fonts.add(fontFace);
            $("#preview_text").css("font-family", fontName);
            });
        };
        reader.readAsArrayBuffer(file);
    });

    $("#song_title_input").on("input", sendTxtToServer);
    $("#singer_input").on("input", sendTxtToServer);
    $("#lyrics_input").on("input", sendTxtToServer);

    $("#select_bg").on("input", updatePreviewImage);
    $("#select_cover").on("input", updatePreviewImage);
    $("#select_font").on("input", updatePreviewImage);
    $("#song_title_input").on("input", updatePreviewImage);
    $("#singer_input").on("input", updatePreviewImage);
    $("#lyrics_input").on("input", updatePreviewImage);

});

setInterval(checkImageUpdate, 1000);

   

