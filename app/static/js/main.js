$(function() {
    $(".tab-wrapper .tab-titles .tab-title").on("click", function() {
        let titleClicked = $(this);
        let wrapper = titleClicked.closest(".tab-wrapper");
        wrapper.find(".tab-title").removeClass("active");

        let tabs = wrapper.find(".tab").removeClass("active");
        let tabSelector = titleClicked.data("target");

        let tab = $(tabSelector);
        tab.addClass("active");
        titleClicked.addClass("active");
    });

    // Gestione upvote
    $(".discussion-actions.upvotes .vote").on("click", function(e) {
        e.preventDefault();

        let btn = $(this);
        let url = btn.attr("href");
        let value = btn.hasClass("upvote")? 1 : -1;

        $.ajax({
            url: url,
            method: "POST",
            data: {
                upvote_value: value
            },

            complete: function(response) {
                let res = JSON.parse(response.responseText);
                if (res["success"] === true) {
                    let wrapperBtn = btn.closest(".upvotes");
                    let upvoteText = wrapperBtn.find(".current-upvotes").text(res["value"]);
                }
            }
        });
    });
});