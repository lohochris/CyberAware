from django.urls import path
from . import views

app_name = "assessment"

urlpatterns = [
    # Entry page for assessment section
    path("", views.assess, name="assess"),

    # Decision tool: "Is this abuse or harassment?"
    path("is-this-abuse/", views.decision_tool, name="decision_tool"),

    # Scenario-based learning tool
    path("scenario-simulator/", views.scenario_simulator, name="scenario_simulator"),

    # Step-by-step action and reporting guidance
    path("action-pathway/", views.action_pathway, name="action_pathway"),

    # Bystander intervention tool
    path("bystander-tool/", views.bystander_tool, name="bystander_tool"),
]
