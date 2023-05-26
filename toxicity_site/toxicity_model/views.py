import os

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import RegisterForm
from .logging_folder.logger_func import log_to_file_and_console
from .model.dl_model import fit_model, predict_model
from .models import UserRequests


class SiteUser:
    text_params = ["Text", "Toxic", "Severe Toxic", "Obscene", "Threat", "Insult", "Identity Hate"]

    def home(self, request, *args, **kwargs):
        log_to_file_and_console("Start project")
        # self.tm.fit()
        fit_model()
        return render(request, "home.html")

    def user_page(self, request, *args, **kwargs):
        text = request.POST.get("comment")
        if text:
            return self.get_request_result(request, *args, **kwargs)

        log_to_file_and_console("Show request page")

        title = "Enter your message"
        return render(request, "make_requests.html", {"title": title})

    def get_request_result(self, request, *args, **kwargs):
        log_to_file_and_console("Compute user request")
        text = request.POST.get("comment")
        result = predict_model(text)
        result = dict(zip(self.text_params[1:], list(result[0])))

        current_user_id = request.user.id
        ur = UserRequests(username_id=current_user_id,
                          request_text=text,
                          toxic=result["Toxic"],
                          severe_toxic=result["Severe Toxic"],
                          obscene=result["Obscene"],
                          threat=result["Threat"],
                          insult=result["Insult"],
                          identity_hate=result["Identity Hate"])
        ur.save()
        log_to_file_and_console("Add new user-request record")

        title = "Result of processing"
        return render(request, "request_result.html", {"text": text,
                                                       "result": result,
                                                       "title": title})

    def get_requests(self, request, *args, **kwargs):
        log_to_file_and_console("Get all user's requests results")
        current_user_id = request.user.id
        user_reqs = UserRequests.objects.filter(username_id=current_user_id)

        texts = [(ur.request_text,
                  f'{ur.toxic:.2f}',
                  f'{ur.severe_toxic:.2f}',
                  f'{ur.obscene:.2f}',
                  f'{ur.threat:.2f}',
                  f'{ur.insult:.2f}',
                  f'{ur.identity_hate:.2f}') for ur in user_reqs]

        title = "Requests History"
        return render(request, "requests_history.html", {"texts": texts,
                                                         "text_params": self.text_params,
                                                         "title": title})

    def save_to_json(self, request, *args, **kwargs):
        log_to_file_and_console("Save to json")

        DIR_NAME = os.path.dirname(os.path.abspath(__file__))
        current_user_id = request.user.id
        data = list(UserRequests.objects.filter(username_id=current_user_id).values())
        response = JsonResponse(data, safe=False)
        # "users_requests_files"
        current_user_id = request.user.id
        file_name = "_".join(["requests", "user", f"{current_user_id}.json"])
        file_name = os.path.join(DIR_NAME, "users_requests_files", file_name)
        with open(file_name, mode="wb") as f:
            f.write(response.content)

        return redirect("make_request")


class RegisterUser(CreateView):
    form_class = RegisterForm
    template_name = os.path.join("registration", "sign_up.html")
    success_url = reverse_lazy("user_page")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def form_valid(self, form):
        log_to_file_and_console("Create new user")
        user = form.save()
        login(self.request, user)
        return redirect('user_page')


class LoginUser(LoginView):
    form_class = AuthenticationForm
    template_name = os.path.join("registration", "login.html")

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return dict(list(context.items()))

    def get_success_url(self):
        log_to_file_and_console("User logs in")
        return reverse_lazy("user_page")


def logout_user(request):
    current_user_id = request.user.id
    log_to_file_and_console(f"User {current_user_id} logs out")
    logout(request)
    return redirect('login')







