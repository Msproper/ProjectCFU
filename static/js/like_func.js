$(document).ready(function() {
  $(".heart_mark").click(function() {
    var recipeId = $(this).data("recipe-id");
    $.ajax({
      url: "/like/" + recipeId,
      type: "POST",
      success: function(data) {
        $("#recipe-" + recipeId).text(data.likes);
        var likeButton = $("#Heart_id_" + recipeId);
  if (likeButton.hasClass("heart_mark_liked")) {
    likeButton.removeClass("heart_mark_liked");
  } else {
    likeButton.addClass("heart_mark_liked");
  }
      }
    });
  });
});