from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory="App/View/templates")
class SiteController:
    def Home(self, request):
        return template.TemplateResponse("login.html", {"request": request})
    def Admin(self, request):
        return template.TemplateResponse("admin.html", {"request": request})
    def User(self, request):
        return template.TemplateResponse("user.html", {"request": request})