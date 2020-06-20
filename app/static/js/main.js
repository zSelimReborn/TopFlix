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
    $(document).on("click", '.discussion-actions.upvotes .vote', function(e) {
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

                    // Se aveva già votato
                    if (wrapperBtn.hasClass('upvote')) {
                        // Se ha cliccato di nuovo su voto positivo rimuovo, altrimenti rimuovo upvote ed aggiungo downvote
                        if (value === 1) {
                            wrapperBtn.removeClass("already-upvoted").removeClass("upvote");
                        } else {
                            wrapperBtn.removeClass("upvote").addClass("downvote");
                        }
                    } else if (wrapperBtn.hasClass("downvote")) {
                        if (value === -1) {
                            wrapperBtn.removeClass("already-upvoted").removeClass("downvote");
                        } else {
                            wrapperBtn.removeClass("downvote").addClass("upvote");
                        }
                    } else {
                        wrapperBtn.addClass("already-upvoted");
                        let voteClass = (value === 1)? "upvote" : "downvote";
                        wrapperBtn.addClass(voteClass);
                    }
                }
            }
        });
    });
});