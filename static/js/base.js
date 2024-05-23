//------------------------------Login------------------------------



$(".message a[data-toggle]").on("click", function() {
    var params = JSON.parse($(this).attr("data-toggle"));

    var param1 = params.param1;
    var param2 = params.param2;
    var param3 = params.param3;

    if ($(param1).css('display') != 'block') {
        $(param2).animate({height: "toggle", opacity: "toggle"}, "slow");
    }
    $(param1).animate({height: "toggle", opacity: "toggle"}, "slow");

});

//-----------------------------EndLogin-----------------------------


//-------------------------------Password Reset-------------------------------

var currentPath = window.location.hash;

//console.log(currentPath);

function setActivePasswordReset(params) {
    var param1 = params.param1;
    var param2 = params.param2;

    if ($(param1).css('display') != 'block') {
        $(param2).animate({height: "toggle", opacity: "toggle"}, "slow");
    }
    $(param1).animate({height: "toggle", opacity: "toggle"}, "slow");
}

// Если текущий путь соответствует "settings/password-change/"
if (currentPath === '#password-reset') {
    setActivePasswordReset({"param1": ".password-recovery-form", "param2": ".login-form"});
}

//-------------------------------End Password Reset-------------------------------



//-----------------------------Notification-----------------------------



var successMessageElement = document.getElementById("successMessage");

if (successMessageElement) {
    var successMessage = successMessageElement.textContent;
    // Теперь у вас есть сообщение `success` в переменной successMessage
    console.log("Success message:", successMessage);
    // Вы можете выполнить здесь любые дополнительные действия с сообщением
}

function setNotification(param) {
    $(param).animate({height: "toggle", opacity: "toggle"}, "slow");
}

var successScreenElement = document.getElementById("screen");

if (successScreenElement) {
    setNotification("#screen");
}




$(document).ready(function(){
    // Добавляем обработчик события click к кнопке с id "removeButton"
    $("#closeButton").click(function(){
        // Выберите элемент с классом "notification" и вызовите метод remove()
        $("#screen").animate({height: "toggle", opacity: "toggle"}, "slow");

    });
});


//---------------------------End Notification---------------------------


//-------------------------------Log-out-------------------------------


var element = document.getElementById("logoutButton");

if (element) {
    document.getElementById("logoutButton").addEventListener("click", function() {
      const csrftoken = Cookies.get('csrftoken');
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
}


//-------------------------------End Log-out-------------------------------



//-------------------------------Settings Tabs-------------------------------


// Получаем текущий путь URL
//var currentPath = window.location.pathname;

var currentPath = window.location.hash;

// Функция для управления классами вкладок
function setActiveTab() {
    // Удаляем классы "active" и "show" со всех элементов с классом "tab-pane"
    $('.tab-pane').removeClass('active show');

    // Добавляем классы "active" и "show" к вкладке с ID, соответствующему текущему пути URL
    var tabId = '#account-change-password'
    $(tabId).addClass('active show');

    // Удаляем класс "action" у всех элементов <a> с классом "list-group-item"
    $('.list-group-item').removeClass('active');

    // Добавляем классы "active" и "show" к вкладке с ID, соответствующему текущему пути URL
    var tabId = 'a[href="#account-change-password"]';
    $(tabId).addClass('active');
}

// Если текущий путь соответствует "settings/password-change/"
if (currentPath === '#account-change-password') {
    setActiveTab();
}

//-------------------------------End Settings Tabs-------------------------------


