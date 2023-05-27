from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import ToDoList, Category


def redirect_view(request):
    return redirect("/category")


def todo(request):
    # запрашиваем все объекты todo через менеджер объектов
    todos = ToDoList.objects.all()
    categories = Category.objects.all()  # так же получаем все Категории

    if request.method == "POST":  # проверяем то что метод именно POST
        if "Add" in request.POST:  # проверяем метод добавления todo
            title = request.POST["description"]  # сам текст
            # дата, до которой должно быть закончено дело
            date = str(request.POST["date"])
            # категория, которой может выбрать или создать пользователь.
            category = request.POST["category_select"]
            content = title + " -- " + date + " " + category  # полный склеенный контент
            Todo = ToDoList(title=title, content=content, due_date=date,
                            category=Category.objects.get(name=category))
            Todo.save()  # сохранение нашего дела
            # перегрузка страницы (ну вот так у нас будет устроено очищение формы)
            return redirect("/todo")
        if "Delete" in request.POST:  # если пользователь собирается удалить одно дело
            # берем список выделенные дел, которые мы собираемся удалить
            checkedlist = request.POST.getlist('checkedbox')
            for i in range(len(checkedlist)):  # мне почему-то не нравится эта конструкция
                todo = ToDoList.objects.filter(id=int(checkedlist[i]))
                todo.delete()  # удаление дела
    return render(request, "todo.html", {"todos": todos, "categories": categories})


def category(request):
    categories = Category.objects.all()  # запрашиваем все объекты Категорий
    if request.method == "POST":  # проверяем что это метод POST
        if "Add" in request.POST:  # если собираемся добавить
            name = request.POST["name"]  # имя нашей категории
            category = Category(name=name)  # у нашей категории есть только имя
            category.save()  # сохранение нашей категории
            return redirect("/category")
        if "Delete" in request.POST:  # проверяем есть ли удаление
            # немного изменил название массива в отличии от todo, что бы было меньше путаницы в коде
            check = request.POST.getlist('check')
            for i in range(len(check)):
                try:
                    сateg = Category.objects.filter(id=int(check[i]))
                    сateg.delete()  # удаление категории
                except BaseException:  # вне сомнения тут нужно нормально переписать обработку ошибок, но на первое время хватит и этого
                    return HttpResponse('<h1>Сначала удалите карточки с этими категориями)</h1>')
    return render(request, "category.html", {"categories": categories})
# Create your views here.
