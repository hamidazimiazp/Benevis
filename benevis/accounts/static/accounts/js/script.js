// #fix follower and following show
$(document).ready(function(){
    $("#btn-following").on('click', function(){
        if ($("#followers").hasClass("show active")){
            $("#followers").removeClass("show active");
        }
        if($("#followers-tab").hasClass("active")){                
            $("#followers-tab").removeClass("active");
        }
        $("#following").addClass('show active');
        $("#following-tab").addClass('active');
    });

    $("#btn-followers").on('click', function(){
        if ($("#following").hasClass("show active")){
            $("#following").removeClass("show active");
        }
        if($("#following-tab").hasClass("active")){                
            $("#following-tab").removeClass("active");
        }
        $("#followers").addClass('show active');
        $("#followers-tab").addClass('active');
    });

    $("#following-tab").on('click', function(){
        if(!$("#following-tab").hasClass("active show")){
            $("#followers-tab").removeClass("active show");
            $("#followers-tab").attr("aria-selected", "false");
            $("#following-tab").addClass("active show");
            $("#following-tab").attr("aria-selected", "true");

            if($("#followers").hasClass("active")){                
                $("#followers").removeClass("show active");
            }
            $("#following").addClass('show active');
        }
    });
    $("#followers-tab").on('click', function(){
        if(!$("#followers-tab").hasClass("active show")){
            $("#following-tab").removeClass("active show");
            $("#following-tab").attr("aria-selected", "false");
            $("#followers-tab").addClass("active show");
            $("#followers-tab").attr("aria-selected", "true");

            if($("#following").hasClass("active")){                
                $("#following").removeClass("show active");
            }
            $("#followers").addClass('show active');
        }
    });
});;


// edit profile 
$(document).ready(function(){
    $("#submit-profile-edit").on("click", function(){
        
        const progressBox = $("#progressBox");
        const progressH2 = $("#progress-title");
        const profileEditForm = $("#profileEditForm");

        let username = $("#id_username").val();
        let first_name = $("#id_first_name").val();
        let last_name = $("#id_last_name").val();
        let bio = $("#id_bio").val();
        let age = $("#id_age").val();
        let phone = $("#id_phone").val();
        let avatar = document.getElementById('id_avatar');

        const csrf = document.getElementsByName('csrfmiddlewaretoken');
        const img_data = avatar.files[0];
        // const url = URL.createObjectURL(img_data)
        
        const fd = new FormData();
        fd.append('csrfmiddlewaretoken', csrf[0].value);
        fd.append('avatar', img_data);
        fd.append('username', username);
        fd.append('last_name', last_name);
        fd.append('first_name', first_name);
        fd.append('age', age);
        fd.append('bio', bio);
        fd.append('phone', phone);

        $(".progres-cover").show();
        $(".progres-cover").css("display", "flex");


        $.ajax({
            url : profileEditForm.action,
            method : 'POST',
            enctype : "multipart/form-data",
            data : fd,

            xhr: function(){
                const xhr = new window.XMLHttpRequest();
                xhr.upload.addEventListener('progress', e =>{
                    if (e.lengthComputable) {
                        const percent = e.loaded / e.total * 100
                        progressBox.html(`<div class="progress-bar" role="progressbar" style="width: ${percent}%" aria-valuenow="${percent}" aria-valuemin="0" aria-valuemax="100">${percent.toFixed(1)}%</div>`);
                        if(percent > 90){
                            progressH2.text("لطفا صبر کنید");
                        }
                    }
                });
                return xhr;
            },
            success : function(response){
                progressH2.text("اطلاعات با موفقیت بروز شد! درحال بروز رسانی داشبورد")
                 
                $(".progres-cover").css("display", "none");
                if(response["username"]){
                    location.assign(`/accounts/${response["username"]}/`); 
                }
            },
            error : function(error){

            },
            cache: false,
            contentType: false,
            processData: false,
        });
    })
});


// follow
$(document).ready(function(){
    $("#AJfollowing-btn").on("click", function(e){

        const csrf = document.getElementsByName('csrfmiddlewaretoken');
        
        let userID = $(this).attr("data-id");
        let follow = $(this).attr("data-value");

        let url, btn_text, btn_class, data_value

        
        if(follow == 'follow'){
            url = "/accounts/follow/user/";
            btn_text = "لغو دنبال کردن";
            data_value = "unfollow"
            btn_class = "btn btn-danger text-white";
        }else{
            url = "/accounts/unfollow/user/";
            btn_text = "دنبال کردن";
            data_value = "follow"
            btn_class = "btn btn-primary text-white";
        }

        const data  = {
            "userID" : userID,
            "csrfmiddlewaretoken" : csrf[0].value,
        }

        $.ajax({
            url : url,
            method : 'POST',
            data : data,
            success : function(data){
                if(data["status"] == "ok"){
                    $("#AJfollowing-btn").text(btn_text);
                    $("#AJfollowing-btn").attr('class', btn_class);
                    $("#AJfollowing-btn").attr('data-value', data_value);
                }
            }
        })
    });
});
