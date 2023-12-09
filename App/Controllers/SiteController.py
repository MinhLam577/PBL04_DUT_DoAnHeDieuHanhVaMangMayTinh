from fastapi.templating import Jinja2Templates
template = Jinja2Templates(directory="App/View/templates")
class SiteController:
    def index(self, request):
        return template.TemplateResponse("index.html", {"request": request})
    def Login(self, request):
        return template.TemplateResponse("login.html", {"request": request})
    def LoginSuccess(self, request, userType: str | None = None):
        if(userType == 'admin'):
            return template.TemplateResponse("admin2.html", {"request": request})
        else:
            return template.TemplateResponse("user.html", {"request": request})