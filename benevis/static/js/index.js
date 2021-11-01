// like unlike 

function makeOrRemoveVote(){
    $(document).ready(function(){
        $(".like").on("click", function(){
            const csrf = document.getElementsByName('csrfmiddlewaretoken');
    
            const likeBtn = $(this).children("i")
            const twt_id = likeBtn.attr("data-twitte-id");
            const can_like = likeBtn.attr("data-can-like");
            const span_count = $(this).children("span")
    
    
            let url, data;
    
            if(can_like == 'True'){
                url = `/twittes/like/${twt_id}/`;
            }else if(can_like == "False"){
                url = `/twittes/unlike/${twt_id}/`;            
            }else{
                url = "/accounts/login/";
            }
    
            data  = {
                "csrfmiddlewaretoken" : csrf[0].value,
            }
            
    
    
            if(url != "/accounts/login/"){
                $.ajax({
                    url : url,
                    method : 'POST',
                    data : data,
                    success : function(data){
                        if(data["status"] == "ok"){
                            like_count = parseInt(span_count.text())
                            let new_count;
        
                            if(url.includes("unlike")){
                                likeBtn.attr("data-can-like", "True");
                                likeBtn.removeClass("red")
                                if(like_count !== 0){
                                    new_count = like_count -1;
                                }
                                
                            }else{
                                likeBtn.attr("data-can-like", "False");
                                new_count = like_count + 1;                        
                                likeBtn.addClass("red");                        
                            }
                            
                            span_count.html(new_count);
                        }
                    }
                })
            }else{
                window.location.replace(url);
            }
        })
    })
}


// share & comment buttons
function shareClick(){
    $(document).ready(function(){

        $(".comment").on("click", function(){
            let raw_link = $(this).parent().parent().children("a")[0].getAttribute("href");
            
            window.location.replace(raw_link);
        });
        
        $(".share").on("click", function(){
            let raw_link = $(this).parent().parent().children("a")[0].getAttribute("href");
            const twitte_link = window.location.host + raw_link;
            
            if(!navigator.clipboard){
                var $temp = $("<input>");
                $("body").append($temp);
                $temp.val(twitte_link).select();
                document.execCommand("copy");
                $temp.remove();
                $(".share-alert").fadeIn(100);
                $(".share-alert").fadeOut(1000);
                
            }else{
                navigator.clipboard.writeText(twitte_link).then(
                    function(){
                        $(".share-alert").fadeIn(100);
                        $(".share-alert").fadeOut(3000);
                    }
                ).catch(
                    function(){
                        $(".share-alert-message").text("خطا در کپی کردن لینک !");
                        $(".share-alert").removeClass("alert-success").addClass("alert-warning");
                        $(".share-alert").fadeIn(100);                        
                        $(".share-alert").fadeOut(3000);
                    }
                )
            }

        })
    })
}


function checkRTL(){
    var rtlChar = /[\u0590-\u083F]|[\u08A0-\u08FF]|[\uFB1D-\uFDFF]|[\uFE70-\uFEFF]/mg;
    
    $(".card-body-paragraph").each(function(index){
        const isRTL = $(this).text().match(rtlChar);

        if(isRTL !== null) {
            $(this).parent().css("text-align", "right");
        }else {
            $(this).parent().css("text-align", "left");
        }
    })
    
}


checkRTL();
makeOrRemoveVote();
shareClick()


var infinite = new Waypoint.Infinite({
    element: $('.infinite-container')[0],

    offset: 'bottom-in-view',

    onBeforePageLoad: function () {
        $('.loading').show();
    },

    onAfterPageLoad: function () {
        $('.loading').hide();

        // check rtl
        checkRTL();
        // like
        $(".like").unbind('click');
        makeOrRemoveVote();
        // share
        $(".share").unbind('click');
        shareClick()
    }
});


$(document).ready(function(){
    const url = $("#searchQueryForm").attr("action");
    const myInput = $("#Query");

    $("#searchQueryForm").on("submit", function(e){
        e.preventDefault();
    });

    $(myInput).on("keyup", function(event){
        event.preventDefault();
        const Query = myInput.val();

        if(Query == ""){
            $(".result ul li").remove();
        }
        $.ajax({
            url: url,
            method : 'GET',
            data: {
                "query" : Query,
            },
            success : function(data){
                if(data["users"]){
                    $(".result ul li").remove();

                    for(const item of data["users"]){
                        const listItem = $(`<a href='/accounts/${item[0]}'><li style='margin-top: 16px;margin-left: 7px;'>${item[0]}</li></a>`);
                        $(".result ul").append(listItem);
                    }
                }
            }
        });
    })
});
