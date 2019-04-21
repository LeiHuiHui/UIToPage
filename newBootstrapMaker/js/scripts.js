var webpage = "";

function supportstorage() {
    if (typeof window.localStorage == 'object')
        return true;
    else
        return false;
}

function handleSaveLayout() {
    var e = $(".demo").html();
    if (!stopsave && e != window.demoHtml) {
        stopsave++;
        window.demoHtml = e;
        saveLayout();
        stopsave--;
    }
}

var layouthistory;

function saveLayout() {
    var data = layouthistory;
    if (!data) {
        data = {};
        data.count = 0;
        data.list = [];
    }
    if (data.list.length > data.count) {
        for (i = data.count; i < data.list.length; i++)
            data.list[i] = null;
    }
    data.list[data.count] = window.demoHtml;
    data.count++;
    if (supportstorage()) {
        localStorage.setItem("layoutdata", JSON.stringify(data));
    }
    layouthistory = data;
    //console.log(data);
    /*$.ajax({  
    	type: "POST",  
    	url: "/build/saveLayout",  
    	data: { layout: $('.demo').html() },  
    	success: function(data) {
    		//updateButtonsVisibility();
    	}
    });*/
}

function downloadLayout() {

    $.ajax({
        type: "POST",
        url: "/build/downloadLayout",
        data: { layout: $('#download-layout').html() },
        success: function(data) { window.location.href = '/build/download'; }
    });
}

function downloadHtmlLayout() {
    $.ajax({
        type: "POST",
        url: "/build/downloadLayout",
        data: { layout: $('#download-layout').html() },
        success: function(data) { window.location.href = '/build/downloadHtml'; }
    });
}

function undoLayout() {
    var data = layouthistory;
    //console.log(data);
    if (data) {
        if (data.count < 2) return false;
        window.demoHtml = data.list[data.count - 2];
        data.count--;
        $('.demo').html(window.demoHtml);
        if (supportstorage()) {
            localStorage.setItem("layoutdata", JSON.stringify(data));
        }
        return true;
    }
    return false;
    /*$.ajax({  
    	type: "POST",  
    	url: "/build/getPreviousLayout",  
    	data: { },  
    	success: function(data) {
    		undoOperation(data);
    	}
    });*/
}

function redoLayout() {
    var data = layouthistory;
    if (data) {
        if (data.list[data.count]) {
            window.demoHtml = data.list[data.count];
            data.count++;
            $('.demo').html(window.demoHtml);
            if (supportstorage()) {
                localStorage.setItem("layoutdata", JSON.stringify(data));
            }
            return true;
        }
    }
    return false;
    /*
    $.ajax({  
    	type: "POST",  
    	url: "/build/getPreviousLayout",  
    	data: { },  
    	success: function(data) {
    		redoOperation(data);
    	}
    });*/
}

function handleJsIds() {
    handleModalIds();
    handleAccordionIds();
    handleCarouselIds();
    handleTabsIds()
}

// function handleAccordionIds() {
//     var e = $(".demo #myAccordion");
//     var t = randomNumber();
//     var n = "accordion-" + t;
//     var r;
//     e.attr("id", n);
//     e.find(".accordion-group").each(function(e, t) {
//         r = "accordion-element-" + randomNumber();
//         $(t).find(".accordion-toggle").each(function(e, t) {
//             $(t).attr("data-parent", "#" + n);
//             $(t).attr("href", "#" + r)
//         });
//         $(t).find(".accordion-body").each(function(e, t) {
//             $(t).attr("id", r)
//         })
//     })
// }

function handleAccordionIds() {
    var e = $(".demo #myAccordion");
    var t = randomNumber();
    var n = "panel-" + t;
    var r;
    e.attr("id", n);
    e.find(".panel").each(function(e, t) {
        r = "panel-element-" + randomNumber();
        $(t).find(".panel-title").each(function(e, t) {
            $(t).attr("data-parent", "#" + n);
            $(t).attr("href", "#" + r)
        });
        $(t).find(".panel-collapse").each(function(e, t) {
            $(t).attr("id", r)
        })
    })
}

function handleCarouselIds() {
    var e = $(".demo #myCarousel");
    var t = randomNumber();
    var n = "carousel-" + t;
    e.attr("id", n);
    e.find(".carousel-indicators li").each(function(e, t) {
        $(t).attr("data-target", "#" + n)
    });
    e.find(".left").attr("href", "#" + n);
    e.find(".right").attr("href", "#" + n)
}

function handleModalIds() {
    var e = $(".demo #myModalLink");
    var t = randomNumber();
    var n = "modal-container-" + t;
    var r = "modal-" + t;
    e.attr("id", r);
    e.attr("href", "#" + n);
    e.next().attr("id", n)
}

function handleTabsIds() {
    var e = $(".demo #myTabs");
    var t = randomNumber();
    var n = "tabs-" + t;
    e.attr("id", n);
    e.find(".tab-pane").each(function(e, t) {
        var n = $(t).attr("id");
        var r = "panel-" + randomNumber();
        $(t).attr("id", r);
        $(t).parent().parent().find("a[href=#" + n + "]").attr("href", "#" + r)
    })
}

function randomNumber() {
    return randomFromInterval(1, 1e6)
}

function randomFromInterval(e, t) {
    return Math.floor(Math.random() * (t - e + 1) + e)
}

function gridSystemGenerator() {
    $(".lyrow .preview input").bind("keyup", function() {
        var e = 0;
        var t = "";
        var n = $(this).val().split(" ", 12);
        $.each(n, function(n, r) {
            e = e + parseInt(r);
            t += '<div class="span' + r + ' column"></div>'
        });
        if (e == 12) {
            $(this).parent().next().children().html(t);
            $(this).parent().prev().show()
        } else {
            $(this).parent().prev().hide()
        }
    })
}

function configurationElm(e, t) {
    $(".demo").delegate(".configuration > a", "click", function(e) {
        e.preventDefault();
        var t = $(this).parent().next().next().children();
        $(this).toggleClass("active");
        t.toggleClass($(this).attr("rel"))
    });
    $(".demo").delegate(".configuration .dropdown-menu a", "click", function(e) {
        e.preventDefault();
        var t = $(this).parent().parent();
        // console.log($(this));
        var n = t.parent().parent().next().next().children();
        if ($(this).attr("class") && $(this).attr("class").match("addonchildren") != null) {
            n = t.parent().parent().next().next().children().children();
        }
        t.find("li").removeClass("active");
        $(this).parent().addClass("active");
        var r = "";
        t.find("a").each(function() {
            r += $(this).attr("rel") + " "
        });
        t.parent().removeClass("open");
        n.removeClass(r);
        n.addClass($(this).attr("rel"))
    })
}

function removeElm() {
    $(".demo").delegate(".remove", "click", function(e) {
        e.preventDefault();
        $(this).parent().remove();
        if (!$(".demo .lyrow").length > 0) {
            clearDemo()
        }
    })
}

function clearDemo() {
    $(".demo").empty();
    layouthistory = null;
    if (supportstorage())
        localStorage.removeItem("layoutdata");
}

function removeMenuClasses() {
    $("#menu-layoutit li button").removeClass("active")
}

function changeStructure(e, t) {
    $("#download-layout ." + e).removeClass(e).addClass(t)
}

function cleanHtml(e) {
    $(e).parent().append($(e).children().html())
}

function downloadLayoutSrc() {
    var e = "";
    $("#download-layout").children().html($(".demo").html());
    var t = $("#download-layout").children();
    t.find(".preview, .configuration, .drag, .remove").remove();
    t.find(".lyrow").addClass("removeClean");
    t.find(".box-element").addClass("removeClean");
    t.find(".lyrow .lyrow .lyrow .lyrow .lyrow .removeClean").each(function() {
        cleanHtml(this)
    });
    t.find(".lyrow .lyrow .lyrow .lyrow .removeClean").each(function() {
        cleanHtml(this)
    });
    t.find(".lyrow .lyrow .lyrow .removeClean").each(function() {
        cleanHtml(this)
    });
    t.find(".lyrow .lyrow .removeClean").each(function() {
        cleanHtml(this)
    });
    t.find(".lyrow .removeClean").each(function() {
        cleanHtml(this)
    });
    t.find(".removeClean").each(function() {
        cleanHtml(this)
    });
    t.find(".removeClean").remove();
    $("#download-layout .column").removeClass("ui-sortable");
    $("#download-layout .row-fluid").removeClass("clearfix").children().removeClass("column");
    if ($("#download-layout .container").length > 0) {
        changeStructure("row-fluid", "row")
    }
    formatSrc = $.htmlClean($("#download-layout").html(), {
        format: true,
        allowedAttributes: [
            ["id"],
            ["class"],
            ["data-toggle"],
            ["data-target"],
            ["data-parent"],
            ["role"],
            ["data-dismiss"],
            ["aria-labelledby"],
            ["aria-hidden"],
            ["data-slide-to"],
            ["data-slide"]
        ]
    });
    $("#download-layout").html(formatSrc);
    $("#downloadModal textarea").empty();
    $("#downloadModal textarea").val(formatSrc)
    webpage = formatSrc;
}

var currentDocument = null;
var timerSave = 1000;
var stopsave = 0;
var startdrag = 0;
var demoHtml = $(".demo").html();
var currenteditor = null;
$(window).resize(function() {
    $("body").css("min-height", $(window).height() - 90);
    $(".demo").css("min-height", $(window).height() - 160)
});

function restoreData() {
    if (supportstorage()) {
        layouthistory = JSON.parse(localStorage.getItem("layoutdata"));
        if (!layouthistory) return false;
        window.demoHtml = layouthistory.list[layouthistory.count - 1];
        if (window.demoHtml) $(".demo").html(window.demoHtml);
    }
}

function initContainer() {
    $(".demo, .demo .column").sortable({
        connectWith: ".column",
        opacity: .35,
        handle: ".drag",
        start: function(e, t) {
            if (!startdrag) stopsave++;
            startdrag = 1;
        },
        stop: function(e, t) {
            if (stopsave > 0) stopsave--;
            startdrag = 0;
        }
    });
    configurationElm();
}
$(document).ready(function() {
    CKEDITOR.disableAutoInline = true;
    restoreData();
    var contenthandle = CKEDITOR.replace('contenteditor', {
        language: 'en',
        contentsCss: ['css/bootstrap3_3_6.css'],
        allowedContent: true
    });
    $("body").css("min-height", $(window).height() - 50);
    $(".demo").css("min-height", $(window).height() - 130);
    $(".sidebar-nav .lyrow").draggable({
        connectToSortable: ".demo",
        helper: "clone",
        handle: ".drag",
        start: function(e, t) {
            if (!startdrag) stopsave++;
            startdrag = 1;
        },
        drag: function(e, t) {
            t.helper.width(400)
        },
        stop: function(e, t) {
            $(".demo .column").sortable({
                opacity: .35,
                connectWith: ".column",
                start: function(e, t) {
                    if (!startdrag) stopsave++;
                    startdrag = 1;
                },
                stop: function(e, t) {
                    if (stopsave > 0) stopsave--;
                    startdrag = 0;
                }
            });
            if (stopsave > 0) stopsave--;
            startdrag = 0;
        }
    });
    $(".sidebar-nav .box").draggable({
        connectToSortable: ".column",
        helper: "clone",
        handle: ".drag",
        start: function(e, t) {
            if (!startdrag) stopsave++;
            startdrag = 1;
        },
        drag: function(e, t) {
            t.helper.width(400)
        },
        stop: function() {
            handleJsIds();
            if (stopsave > 0) stopsave--;
            startdrag = 0;
        }
    });
    initContainer();
    $('body.edit .demo').on("click", "[data-target=#editorModal]", function(e) {
        e.preventDefault();
        currenteditor = $(this).parent().parent().find('.view');
        var eText = currenteditor.html();
        contenthandle.setData(eText);
    });
    $("#savecontent").click(function(e) {
        e.preventDefault();
        currenteditor.html(contenthandle.getData());
    });
    $("[data-target=#downloadModal]").click(function(e) {
        e.preventDefault();
        downloadLayoutSrc();
    });
    $("[data-target=#shareModal]").click(function(e) {
        e.preventDefault();
        handleSaveLayout();
    });
    $("#download").click(function() {
        downloadLayout();
        return false
    });
    $("#downloadhtml").click(function() {
        downloadHtmlLayout();
        return false
    });
    $("#edit").click(function() {
        $("body").removeClass("devpreview sourcepreview");
        $("body").addClass("edit");
        removeMenuClasses();
        $(this).addClass("active");
        return false
    });
    $("#clear").click(function(e) {
        e.preventDefault();
        clearDemo()
    });
    $("#devpreview").click(function() {
        $("body").removeClass("edit sourcepreview");
        $("body").addClass("devpreview");
        removeMenuClasses();
        $(this).addClass("active");
        return false
    });
    $("#sourcepreview").click(function() {
        $("body").removeClass("edit");
        $("body").addClass("devpreview sourcepreview");
        removeMenuClasses();
        $(this).addClass("active");
        return false
    });
    $("#fluidPage").click(function(e) {
        e.preventDefault();
        changeStructure("container", "container-fluid");
        $("#fixedPage").removeClass("active");
        $(this).addClass("active");
        downloadLayoutSrc()
    });
    $("#fixedPage").click(function(e) {
        e.preventDefault();
        changeStructure("container-fluid", "container");
        $("#fluidPage").removeClass("active");
        $(this).addClass("active");
        downloadLayoutSrc()
    });
    $(".nav-header").click(function() {
        $(".sidebar-nav .boxes, .sidebar-nav .rows").hide();
        $(this).next().slideDown()
    });
    $('#undo').click(function() {
        stopsave++;
        if (undoLayout()) initContainer();
        stopsave--;
    });
    $('#redo').click(function() {
        stopsave++;
        if (redoLayout()) initContainer();
        stopsave--;
    });
    $("#active-sidebar-right").click(function() {
        $("body").addClass("show-right-sidebar");
        removeMenuClasses();
        $(this).addClass("active");
    });
    $("#close-sidebar-right").click(function() {
        $("body").removeClass("show-right-sidebar");
        removeMenuClasses();
        $(this).addClass("active");
    });
    // var $ui_image_form = $("#ui_image_form");
    var $UIinput = $("#ui_image_input");
    var $UIimageul = $("#ui_image_ul");
    var $submitUIButton = $("#submit_ui_button");
    var tmpl = '<li class="ui-image-content" style="background-image:url(#url#)"></li>';

    $UIinput.on("change", function(e) {
        var src, url = window.URL || window.webkitURL || window.mozURL,
            files = e.target.files;
        var file = files[0];
        if (url) {
            src = url.createObjectURL(file);
        } else {
            src = e.target.result;
        }

        $UIimageul.empty();
        $UIimageul.append($(tmpl.replace('#url#', src)));
    });

    $submitUIButton.click(function(e) {
        $UIimageul.empty();
        if (e.preventDefault) e.preventDefault();
        var form_data = new FormData();
        form_data.append("ui_image", $UIinput[0].files[0]);
        // var form_data = new FormData($ui_image_form[0]);
        console.log(form_data);
        $.ajax({
            // url: "http://127.0.0.1:8000/sample",
            url: "http://231548t35n.51mypc.cn:57795/sample",
            // url: "http://10.24.81.115:8000/sample",
            type: "POST",
            async: true,
            cache: false,
            processData: false, //用于对data参数进行序列化处理 这里必须false
            contentType: false, //必须
            dataType: 'json',
            // data: new FormData($ui_image_form[0]),
            data: form_data,
            success: function(data) {
                alert("请求成功");
                console.log(data);
                if (data.status === 1) {
                    // 隐藏modal
                    $('#importUIModal').modal('hide');
                    // var resp = JSON.parse(data); # data already an Object
                    var new_demo = data.main;

                    // 将demo下的元素替换成服务器返回的代码
                    $demo = $("#demo_panel");
                    $demo.html(new_demo);
                }

            },
            error: function(XHR, errorInfo) {
                console.log(errorInfo);
                alert("上传失败");
            }
        })
    });
    removeElm();
    gridSystemGenerator();
    setInterval(function() {
        handleSaveLayout()
    }, timerSave)
})

function saveHtml() {
    webpage = '<!DOCTYPE html><html>\n<head>\n<script src="https://cdn.bootcss.com/jquery/2.1.4/jquery.min.js"></script>\n<link href="https://cdn.bootcss.com/twitter-bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet">\n<script src="https://cdn.bootcss.com/twitter-bootstrap/3.3.6/js/bootstrap.min.js"></script>\n</head>\n<body>\n' + webpage + '\n</body>\n</html>'
        /* FM aka Vegetam Added the function that save the file in the directory Downloads. Work only to Chrome Firefox And IE*/
    if (navigator.appName == "Microsoft Internet Explorer" && window.ActiveXObject) {
        var locationFile = location.href.toString();
        var dlg = false;
        with(document) {
            ir = createElement('iframe');
            ir.id = 'ifr';
            ir.location = 'about.blank';
            ir.style.display = 'none';
            body.appendChild(ir);
            with(getElementById('ifr').contentWindow.document) {
                open("text/html", "replace");
                charset = "utf-8";
                write(webpage);
                close();
                document.charset = "utf-8";
                dlg = execCommand('SaveAs', false, locationFile + "webpage.html");
            }
            return dlg;
        }
    } else {
        webpage = webpage;
        var blob = new Blob([webpage], { type: "text/html;charset=utf-8" });
        saveAs(blob, "webpage.html");
    }
}