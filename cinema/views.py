from datetime import datetime, date
from django.views.generic import CreateView, UpdateView, ListView
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.db.models import Sum, F
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
        session = self.kwargs["s"]
        date = self.kwargs["date"]
        context["session"] = session
        context["date"] = date
        booked_sessions = BookedSession.objects.filter(session=session,
                                                       date=date).aggregate(Sum("places"))
        places = booked_sessions["places__sum"]
        if not places:
            places = context["session"].hall.size
        else:
            places = context["session"].hall.size - places
        context["places"] = places
        return context

    def form_valid(self, form):
        try:
            booked_session = form.save(commit=False)
            booked_session.user = self.request.user
            booked_session.session = self.kwargs["s"]
            booked_session.date = self.kwargs["date"]
            booked_session.save()
        except exceptions.NoFreePlacesException:
            messages.add_message(self.request, messages.ERROR, "No free places")
            return redirect(self.request.path_info)
        except exceptions.DateExpiredException:
            messages.add_message(self.request, messages.ERROR, "Date expired")
            return redirect(self.request.path_info)
        except exceptions.NotEnoughMoneyException:
            messages.add_message(self.request, messages.ERROR, "Not enough money")
            return redirect(self.request.path_info)
        else:
            messages.add_message(self.request, messages.SUCCESS, "Session was booked")
            return redirect("/")


class HallList(SuperUserRequired, ListView):
    model = Hall
    template_name = "hall_list.html"
    paginate_by = 50


class SessionList(SuperUserRequired, ListView):
    template_name = "session_list.html"
    model = Session
    paginate_by = 50


class ClientSessionList(ListView):
    model = Session
    template_name = "user_session_list.html"
    paginate_by = 50

    def get_queryset(self):
        query_set = super().get_queryset()
        url_date = self.kwargs["date"]
        query_set = query_set.filter(start_date__lte=url_date, end_date__gte=url_date)
        sort_options = ["start_time", "price"]
        sort = self.kwargs.get("sort", None)
        if sort in sort_options:
            query_set = query_set.order_by(sort)
        return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        url_date = self.kwargs["date"]
        context["date"] = url_date
        return context


class UserBookedSessionsList(LoginRequiredMixin, ListView):
    model = BookedSession
    template_name = "booked_sessions_list.html"
    paginate_by = 50

    def get_queryset(self):
        query_set = super().get_queryset()
        query_set = query_set.filter(user=self.request.user)
        return query_set

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        total_spent = context["object_list"].aggregate(total=Sum(F("session__price") * F("places")))["total"]
        if not total_spent:
            total_spent = 0
        context["total_spent"] = total_spent
        return context


