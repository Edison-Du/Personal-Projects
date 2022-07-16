$(document).on("submit", "#login-form", function(event){
    event.preventDefault(); 

    var _error = $("#form-error")
    var form = $("#login-form").serializeArray();
    var data = {}

    $.each(form, function(i, field){
        data[field.name] = field.value;
    });

    if (data["username"].length > 16) {
        _error.text("Username cannot be more than 16 characters.");
        _error.show();
        return;
    } else if (data["password"].length < 8) {
        _error.text("Password must be at least 8 characters.");
        _error.show();
        return;
    } 

    _error.hide();

    $.ajax({
        type: "POST",
        url: "ajax/verify-user.php",
        data: data,
        dataType: "json",
        async: true
    }).done(function(data){
        if (data["error"] !== undefined) {
            _error.text(data["error"]);
            _error.show();
        } else {
            window.location = "index.php";
        }
    }).fail(function(data) {
        _error.text("An error has occured with the server, your request may not be processed at this time.");
        _error.show();
    });
});