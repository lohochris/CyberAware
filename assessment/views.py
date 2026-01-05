from django.shortcuts import render

# Create your views here.
def assess(request):
    return render(request, "assess.html")


def decision_tool(request):
    result = None

    if request.method == "POST":
        selected = request.POST.getlist("behaviours")

        if not selected:
            result = {
                "message": (
                    "Not selecting any options is completely okay. "
                    "Many adults feel unsure whether something counts as online abuse."
                ),
                "guidance": (
                    "You may still find it helpful to explore the learning resources."
                ),
            }
        elif len(selected) <= 2:
            result = {
                "message": (
                    "Some of the behaviours you selected are commonly associated "
                    "with online abuse or harassment."
                ),
                "guidance": (
                    "You may want to learn more about your options."
                ),
            }
        else:
            result = {
                "message": (
                    "Several behaviours you selected are widely recognised "
                    "as forms of online abuse."
                ),
                "guidance": (
                    "You may wish to explore practical actions or support options."
                ),
            }

    return render(request, "decision_tool.html", {"result": result})

def scenario_simulator(request):
    feedback = None

    if request.method == "POST":
        choice = request.POST.get("response")

        feedback_map = {
            "ignore": {
                "message": (
                    "Choosing not to respond can sometimes prevent escalation, "
                    "especially if the behaviour is low-level or one-off."
                ),
                "note": "However, it may not be effective if the behaviour continues."
            },
            "respond": {
                "message": (
                    "Responding directly may feel instinctive, but it can sometimes "
                    "escalate the situation."
                ),
                "note": "If you respond, keeping messages factual and non-confrontational is safer."
            },
            "document": {
                "message": (
                    "Documenting evidence is widely recommended and carries low risk."
                ),
                "note": "Screenshots and timestamps can be useful if you later decide to report."
            },
            "report": {
                "message": (
                    "Reporting through platform tools or organisations can be appropriate, "
                    "particularly for repeated or serious abuse."
                ),
                "note": "Outcomes vary, and responses are not always immediate."
            }
        }

        feedback = feedback_map.get(choice)

    return render(
        request,
        "scenario_simulator.html",
        {"feedback": feedback}
    )

def action_pathway(request):
    pathway = None

    if request.method == "POST":
        role = request.POST.get("role")
        platform = request.POST.get("platform")
        severity = request.POST.get("severity")

        steps = []

        # Step 1: Immediate safety
        if severity in ["high", "uncertain"]:
            steps.append("Pause and prioritise your safety. Avoid immediate confrontation if you feel distressed.")

        # Step 2: Evidence
        steps.append("Document evidence (screenshots, URLs, timestamps). Keep copies securely.")

        # Step 3: Platform-specific guidance
        platform_map = {
            "social": "Use in-platform reporting and blocking tools. Review community standards.",
            "work": "Check organisational policies and consider HR or a trusted manager.",
            "email": "Preserve headers and messages; avoid replying; consider filtering or blocking.",
            "messaging": "Block the sender and report within the app if the behaviour persists."
        }
        steps.append(platform_map.get(platform, "Consider available reporting and safety tools on the platform."))

        # Step 4: Role-based guidance
        if role == "bystander":
            steps.append("Choose low-risk support actions: report content, offer private support, avoid public escalation.")
        else:
            steps.append("Decide whether reporting or seeking support feels appropriate for you at this stage.")

        # Step 5: External support
        steps.append("If the behaviour continues or escalates, explore external support options listed in the Support section.")

        pathway = steps

    return render(request, "action_pathway.html", {"pathway": pathway})

def bystander_tool(request):
    guidance = None

    if request.method == "POST":
        concern = request.POST.get("concern")

        responses = {
            "unsure": {
                "title": "It is okay to be unsure",
                "steps": [
                    "You are not expected to act immediately or perfectly.",
                    "Observe whether the behaviour is repeated or escalating.",
                    "Learning more before acting is a valid choice."
                ]
            },
            "fear": {
                "title": "Concern about escalation is common",
                "steps": [
                    "Avoid public confrontation if it may worsen the situation.",
                    "Use platform reporting tools where available.",
                    "Consider offering private support to the affected person."
                ]
            },
            "not_know": {
                "title": "You do not need to know the person to help",
                "steps": [
                    "Reporting abusive content can be done anonymously on many platforms.",
                    "You can support safer online spaces without direct contact.",
                    "Choosing not to engage directly is still a form of boundary-setting."
                ]
            },
            "responsibility": {
                "title": "Responsibility can be shared",
                "steps": [
                    "Online harm is a collective issue, not an individual burden.",
                    "Small actions, such as reporting, can contribute to change.",
                    "It is acceptable to prioritise your own safety."
                ]
            }
        }

        guidance = responses.get(concern)

    return render(request, "bystander_tool.html", {"guidance": guidance})