from django.views.generic import CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Sum
from .forms import HallForm, SessionForm, BookedSessionForm
from . import exceptions
from .misc import SuperUserRequired
from .models import Hall, Session, BookedSession


class CreateHallView(SuperUserRequired, CreateView):
    form_class = HallForm
    template_name = "create_hall.html"
    success_url = "/"

    def form_valid(self, form):
        form.save()
        messages.add_message(self.request, messages.SUCCESS, "Hall was created")
        return redirect("/")


class UpdateHallView(SuperUserRequired, UpdateView):
    form_class = HallForm
    model = Hall
    template_name = "update_hall.html"

    def form_valid(self, form):
        try:
            form.save()
        except exceptions.BookedSessionExistsException:
            messages.add_message(self.request, messages.ERROR, "Booked sessions for this hall exist")
            return redirect(self.request.path_info)
        else:
            messages.add_message(self.request, messages.SUCCESS, "Hall was updated")
            return redirect("/")


class CreateSessionView(SuperUserRequired, CreateView):
    form_class = SessionForm
    template_name = "create_session.html"
    success_url = "/"

    def form_valid(self, form):
        try:
            form.save()
        except exceptions.SessionsCollideException:
            messages.add_message(self.request, messages.ERROR, "Session collides with another one")
            return redirect(self.request.path_info)
        else:
            messages.add_message(self.request, messages.SUCCESS, "Session was created")
            return redirect("/")


class UpdateSessionView(SuperUserRequired, UpdateView):
    model = Session
    form_class = SessionForm
    template_name = "update_session.html"

    def form_valid(self, form):
        try:
            form.save()
        except exceptions.SessionsCollideException:
            messages.add_message(self.request, messages.ERROR, "Session collides with another one")
            return redirect(self.request.path_info)
        except exceptions.BookedSessionExistsException:
            messages.add_message(self.request, messages.ERROR, "Booked sessions for this session exist")
            return redirect(self.request.path_info)
        else:
            messages.add_message(self.request, messages.SUCCESS, "Session was updated")
            return redirect("/")


class CreateBookedSessionView(LoginRequiredMixin, CreateView):
    form_class = BookedSessionForm
    template_name = "create_booked_session.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["session"] = self.kwargs["s"]
        context["date"] = self.kwargs["date"]
        booked_sessions = BookedSession.objects.filter(session=context["session"],
                                                       date=context["date"]).aggregate(Sum("places"))
        places = booked_sessions["places__sum"]
        if not places:
            places = context["session"].hall.size
        else:
            places = context["session"].hall.size - places
        context["places"] = places
        return context


    def form_valid(self, form):
        try:
            form.save()
        except exceptions.NoFreePlacesException:
            messages.add_message(self.request, messages.ERROR, "No free places")
            return redirect(self.request.path_info)
        else:
            messages.add_message(self.request, messages.SUCCESS, "Session was booked")
            return redirect("/")




