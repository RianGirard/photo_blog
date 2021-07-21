// following ajax setup runs so that any ajax request will automatically insert/use a crsf_token (which is a cookie)
$.ajaxSetup({
    beforeSend: function beforeSend(xhr, settings) {
        function getCookie(name) {
            let cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                const cookies = document.cookie.split(';');
                for (let i = 0; i < cookies.length; i += 1) {
                    const cookie = jQuery.trim(cookies[i]);
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (`${name}=`)) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            // Only send the token to relative URLs i.e. locally.
            xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
        }
    },
});

$(document).on("click", ".js-toggle-modal", function(e) {
    e.preventDefault()
    $(".js-modal").toggleClass("hidden")
})
.on("click", ".js-submit", function(e) {
    e.preventDefault()
    const title = $(".js-post-title").val().trim()
	const desc = $(".js-post-desc").val().trim()

    const $btn = $(this)

    if(!title.length) {
        return False
    }
    if(!desc.length) {
        return False
    }
    $btn.prop("disabled", true).text("Posting!")
    $.ajax({
        type: 'POST',
        url: $(".js-post-form").data("post-url"),
        data: {
            title: title,
            desc: desc,
            author: $(this).data("username"),  
            published: 'yes',
        },
        success: (dataHtml) => {
            $(".js-modal").addClass("hidden");
            $(".js-post-title").val('');
            $(".js-post-desc").val('');
            $("#posts-container").prepend(dataHtml);
            $btn.prop("disabled", false).text("New Post");
        },
        error: (error) => {
            console.warn(error)
            $btn.prop("disabled", false).text("Error");
        }
    });
})
$(document).ready(function(){

    $('.delete_comment').submit(function(e){
        e.preventDefault()
        $.ajax({
            url: '/delete_comment',
            method: 'POST',
            data: $(this).serialize(),
            success: function(serverResponse){
                location.reload();
            }
        })
    })

    $('.enter_comment').submit(function(e){
        e.preventDefault()
        $.ajax({
            url: '/enter_comment',
            method: 'POST',
            data: $(this).serialize(),
            success: function(serverResponse){
                location.reload();
            }
        })
    })

})