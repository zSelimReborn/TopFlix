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
});