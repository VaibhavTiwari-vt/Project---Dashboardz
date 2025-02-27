from django.urls import path
from . import views

urlpatterns = [
    path("",views.main,name="records"),
    path("privacy-policy",views.privacy_policy,name="privacy-policy"),
    path("add-table",views.AddTableView.as_view(),name="add-table"),
    path("add-table-data",views.AddTableDataView.as_view(),name="add-table-data"),
    path("edit-table-data",views.EditTableDataView.as_view(),name="edit-table-data"),
]
