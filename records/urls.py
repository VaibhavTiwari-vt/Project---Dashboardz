from django.urls import path
from . import views

urlpatterns = [
    #No id url is passed so that if user just logged in , it will select the first present record to show.
    path("",views.main,name="records"),
    path("<int:id>/",views.main,name="records"), #Trailing slash is important here.
    path("privacy-policy",views.privacy_policy,name="privacy-policy"),
    path("add-table",views.AddTableView.as_view(),name="add-table"),
    path("add-table-data/<int:id>",views.AddTableDataView.as_view(),name="add-table-data"),
    path("edit-table-data",views.EditTableDataView.as_view(),name="edit-table-data"),
    path("delete-table-data/<int:id>",views.DeleteTableDataView,name="delete-table-data"),
]
