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
