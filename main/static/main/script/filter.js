$("#id_ceh").change(function () {
    var objectId = $(this).val();
    if (objectId === "Участок связи №20"){
        $("#id_uchastok").prop('disabled', 'true')
    }
    else {
        $("#id_uchastok").removeAttr('disabled')
    }
    $.ajax({
        url: "/ajax/load-objects/",
        data: {
            'ceh': objectId
    },
    success: function (data) {
        $("#id_object").html(data);
    }
    });
    $.ajax({
        url: "/ajax/load-uchastok/",
        data: {
            'ceh': objectId
    },
    success: function (data) {
        $("#id_uchastok").html(data);
    }
    });
});
$("#id_uchastok").change(function () {
    var objectId = $(this).val();
    if (objectId !== ""){
        $("#id_ceh").prop('disabled', 'true')
    }
    else {
        $("#id_ceh").removeAttr('disabled')
    }
    $.ajax({
        url: "/ajax/load-object-uchastok/",
        data: {
            'uchastok': objectId
        },
    success: function (data) {
        $("#id_object").html(data);
    }
    });
});
$("#id_object").change(function () {
    var objectId = $(this).val();
    if (objectId !== ""){
        $("#id_ceh").prop('disabled', 'true')
        $("#id_uchastok").prop('disabled', 'true')
    }
    else {
        $("#id_ceh").removeAttr('disabled')
        $("#id_uchastok").removeAttr('disabled')
    }
});
