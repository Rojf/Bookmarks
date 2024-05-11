//------------------------------Login------------------------------

$('.message a').click(function(){
   $('form').animate({height: "toggle", opacity: "toggle"}, "slow");
});


//-----------------------------EndLogin-----------------------------


$(document).ready(function(){
    // Добавляем обработчик события click к кнопке с id "removeButton"
    $("#closeButton").click(function(){
        // Выберите элемент с классом "notification" и вызовите метод remove()
        $("#screen").remove();
    });
});


document.getElementById("logoutButton").addEventListener("click", function() {
  var csrfToken = this.dataset.csrf;
  fetch("/account/logout/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-CSRFToken": csrfToken
    },
    body: JSON.stringify({})
  })
  .then(response => {
    // Обработка перенаправления
    if (response.redirected) {
      window.location.href = response.url; // Перенаправление на указанный URL
    } else {
      // Обработка других ответов
      if (response.ok) {
        console.log("Logout successful");
      } else {
        console.error("Logout failed");
      }
    }
  })
  .catch(error => {
    console.error("Error:", error);
  });
});
