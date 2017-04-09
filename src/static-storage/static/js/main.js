/**
 * Created by OllyD on 3/17/2017.
 */
//if ($('#wrapper').hasClass("menuNotDisplayed")){
//    Cookies.set("menuOutB","false");
//}
//else{
//    Cookies.set("menuOutB","true");
//}





console.log(localStorage.getItem("sideOpen"))

$(document).ready(function(){

    $(document.body).on("click", ".login", function(e){
     e.preventDefault();
     $("#loginModal").modal({})

});

    $(document.body).on("click", ".register", function(e){
     e.preventDefault();
     $("#registerModal").modal({})

});

      $(document.body).on("click", ".follow-btn", function(e){
      e.preventDefault()
      var this_ = $(this)
      var profileId = this_.attr("data-id")
      var followedUrl = '/api/accounts/' + profileId + '/follow/'

      // this_.text("Liked")
      $.ajax({
        method:"GET",
        url: followedUrl,
        success: function(data){
          if (data.following){
            this_.text("Unfollow " + data.follower_count)

          } else {
            this_.text("Follow " + data.follower_count)


          }
        },
        error: function(data){
            popUpLoginModal()
          console.log("error")
          console.log(data)
        }
      })
  })

});



function popUpLoginModal() {
        $("#loginModal").modal({})
    }

function popUpRegisterModal() {
        $("#registerModal").modal({})
    }

function preventModalClose() {
    $(document.body).on("click", "#regsubmit", function(e){
       e.preventDefault();
      // $("#registerModal").modal({"backdrop": "static"});
        //$('body').fadeOut(3000)
    })


}