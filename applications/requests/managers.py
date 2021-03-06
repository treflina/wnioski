from datetime import date, timedelta, datetime

from django.db import models
from django.db.models import Q


class RequestManager(models.Manager):
    '''Managers for Request Model'''

    mindate = datetime.strptime(f"{date.today().year}-01-01", "%Y-%M-%d").date()
    maxdate = date.today() + timedelta(days=21)

    # manager for listing employees requests
    def requests_to_accept(self, user):
        result = self.filter(
            Q(send_to_person=user) & Q(status='oczekujący')).order_by('-created')
        return result

    def requests_holiday_topmanager(self, user):
        result = self.filter(
            Q(type='W') & Q(end_date__gte=self.mindate) & Q(start_date__lte=self.maxdate)).exclude(author=user).order_by('-end_date')
        return result

    def allrequests_holiday_topmanager(self, user):
        result = self.filter(
            Q(type='W')).exclude(author=user).order_by('-end_date')
        return result

    def requests_holiday(self, user):
        result = self.filter(
            Q(author__manager=user) & Q(type='W') & Q(end_date__gte=self.mindate) & Q(start_date__lte=self.maxdate)).order_by('-end_date')
        return result


    def allrequests_holiday(self, user):
        result = self.filter(
            Q(author__manager=user) & Q(type='W')).order_by('-end_date')
        return result

    def hrallrequests_holiday(self):
        return self.filter(Q(type='W')).order_by('-end_date')
        

    def requests_other_topmanager(self, user):
        result = self.filter(
            (Q(type='WS') | Q(type='WN') | Q(type='DW')) & Q(start_date__gte=self.mindate)& Q(start_date__lte=self.maxdate)).exclude(author=user).order_by('-end_date')
        return result

    def allrequests_other_topmanager(self, user):
        result = self.filter(
            Q(type='WS') | Q(type='WN') | Q(type='DW')).exclude(author=user).order_by('-end_date')
        return result

    def allrequests_other(self, user):
        result = self.filter(
            Q(author__manager=user) & (Q(type='WS') | Q(type='WN') | Q(type='DW'))).order_by('-end_date')
        return result

    def hrallrequests_other(self):
        result = self.filter((Q(type='WS') | Q(type='WN') | Q(type='DW'))).order_by('-end_date')
        return result

    def requests_other(self, user):
        result = self.filter(
           (Q(author__manager=user) & (Q(type='WS') | Q(type='WN') | Q(type='DW')))& Q(start_date__gte=self.mindate)& Q(start_date__lte=self.maxdate)).order_by('-end_date')
        return result

    # managers for listing user requests

    def user_requests_holiday(self, user):
        result = self.filter(
            Q(author__id=user.id) & Q(type='W')).order_by('-created')
        return result

    def user_requests_other(self, user):
        result = self.filter(
            Q(author__id=user.id) & (Q(type='WS') | Q(type='WN') | Q(type='DW'))).order_by('-created')
        return result

    def requests_received_counter(self, user):
        """Manager that counts received requests with status 'to accept'. """
        employees_requests_received = self.filter(
            Q(send_to_person=user) & Q(status="oczekujący"))
        result_list = employees_requests_received.all()
        if len(result_list) == 0:
            result = ""
        elif len(result_list) == 1:
            result = "➊"
        elif len(result_list) == 2:
            result = "➋"
        elif len(result_list) == 3:
            result = "➌"
        elif len(result_list) == 4:
            result = "➍"
        elif len(result_list) == 5:
            result = "➎"
        elif len(result_list) == 6:
            result = "➏"
        elif len(result_list) == 7:
            result = "➐"
        elif len(result_list) == 8:
            result = "➑"
        elif len(result_list) == 9:
            result = "➒"
        elif len(result_list) == 10:
            result = "➓"
        elif len(result_list) > 10:
            result = "➓+"

        return result
