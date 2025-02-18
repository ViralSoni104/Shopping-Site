function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken');

function get_sort(){
    $.ajax({
        type: "POST",
        url: "{% url 'category' sitemap%}",
        data:{
            'csrfmiddlewaretoken': csrftoken,
            'sort_filter':document.getElementById("name").value
        },
        dataType: 'json',
        beforeSend: function() {
        
        },
        success: function(data){
        }
    });
}

//function to check all errors and replace same error to avoid printing same errors on webpage
function get_all_errors(className,idName,data){
    var spans = document.getElementsByClassName(className);
    results=[];
    if(!spans){
      $(idName).html(data.error_msg);
    }
    else{
      error_exsist=0;
      for(var i = 0; i < spans.length; i++){
        if(spans[i].innerHTML==data.error_msg)
          error_exsist=error_exsist+1;
      }
      if(error_exsist==0){
        data.error_msg=data.error_msg+"<br/>";
        $(idName).html(data.error_msg);
      }
      else
        $(idName).html('');
    }
  }

//show password toggle function
function showPass_func(className,idName){
    var classDot=".";
    var className=classDot.concat(className," ","a");
    var icon_class=className.concat(" ",".showPassword");
    $(className).on('click', function(event) {
        event.preventDefault();
        if($(idName).attr("type") == "text"){
            $(idName).attr('type', 'password');
            $(icon_class).removeClass('active');
        }else if($(idName).attr("type") == "password"){
            $(icon_class).addClass('active');
            $(idName).attr('type', 'text');
        }
    });
}

function validate_name(id,error_id){
    //email validation onchane for register form
    $(function(){
        $(id).on('change', function(){
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/validateName/",
                data:{
                    'csrfmiddlewaretoken': csrftoken,
                    'contact_name':document.getElementById(id.substr(1,id.length)).value
                },
                dataType: 'json',
                beforeSend: function() {
                
                },
                success: function(data){
                    if(data.is_valid)
                    {
                        $(error_id).html('');
                    }
                    else{
                        $(error_id).html(data.error_msg);
                    }
                }
            });
        })
    });
}

function validate_email(id,email_error_id){
    //email validation onchane for register form
    $(function(){
        $(id).on('change', function(){
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/validateEmail/",
            data:{
                'csrfmiddlewaretoken': csrftoken,
                'email_id':document.getElementById(id.substr(1,id.length)).value
            },
            dataType: 'json',
            beforeSend: function() {
            
            },
            success: function(data){
                if(data.is_valid)
                {
                    $(email_error_id).html('');
                }
                else{
                    $(email_error_id).html(data.error_msg);
                }
            }
        });
        })
    });
}
function password_check(id,re_id){

    //main password error for register form
    $(function(){
        $(id).on('change', function(){
            comparePass();
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/validatePass/",
                data:{
                    'csrfmiddlewaretoken': csrftoken,
                    'password':document.getElementById(id.substr(1,id.length)).value
                },
                dataType: 'json',
                beforeSend: function() {
                },
                success: function(data){
                    if(data.is_valid)
                    {
                        $('#pass_error').html('');
                    }
                    else{
                        get_all_errors('error','#pass_error',data);
                    }
                }
            });
        })
    });

    //check password is entirely numeric or not
    $(function(){
        $(id).on('change', function(){
            $.ajax({
                type: "POST",
                url: "http://127.0.0.1:8000/numericPass/",
                data:{
                    'csrfmiddlewaretoken': csrftoken,
                    'password':document.getElementById(id.substr(1,id.length)).value
                },
                dataType: 'json',
                beforeSend: function() {
                },
                success: function(data){
                    if(data.is_valid)
                    {
                        $('#numeric_pass_error').html('');
                    }
                    else{
                        get_all_errors('error','#numeric_pass_error',data);
                    }
                }
            });
        })
    });

    //check password is comman or not
    $(function(){
        $(id).on('change', function(){
            $.ajax({
                type: "POST",
                url: 'http://127.0.0.1:8000/commanPass/',
                data:{
                    'csrfmiddlewaretoken': csrf_token,
                    'password':document.getElementById(id.substr(1,id.length)).value
                },
                dataType: 'json',
                beforeSend: function() {
                },
                success: function(data){
                    if(data.is_valid)
                    {
                        $('#comman_pass_error').html('');
                    }
                    else{
                        get_all_errors('error','#comman_pass_error',data);
                    }
                }
            });
        })
    });
    function comparePass(){
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:8000/comparePass/",
            data:{
                'csrfmiddlewaretoken': csrftoken,
                'password1':document.getElementById(id.substr(1,id.length)).value,
                'password2':document.getElementById(re_id.substr(1,re_id.length)).value
            },
            dataType: 'json',
            beforeSend: function() {
                
            },
            success: function(data){
                if(data.is_valid)
                {
                $('#confirm_pass_error').html('');
                }
                else{
                get_all_errors('error','#confirm_pass_error',data);
                }
            }
        });
    }
    //re-password compare with main password for register form
    $(function(){
        $(re_id).on('change', function(){
            comparePass();
        })
    });
}