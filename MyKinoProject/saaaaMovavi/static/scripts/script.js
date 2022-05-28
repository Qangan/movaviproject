$(".btn-check").click(function () {
    chingching($(this).attr("id")-1)
})
function chingching(id) {
    $.get("http://localhost:3001/getdata", { "key": "data" }, function () {
        console.log("success");
    })
        .done(function (data) {
            console.log(data);
            $(".text").html(`<p class = "text-white">ID: ${data[id][0]} <br>Название: ${data[id][1]} <br>Зал: ${data[id][2]} <br>Дата проведения сеанса: ${data[id][3]} <br> Описание: ${data[id][4]}</p> <a class="btn btn-primary" href="/oplata?session=${data[id][0]}" role="button">Купить</a>`);
        })
    
};
$(".class");