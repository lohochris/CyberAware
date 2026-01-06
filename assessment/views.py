from django.shortcuts import render, redirect

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
    scenarios = [
        {
            "text": (
                "You receive repeated messages on social media that insult you and make you feel uncomfortable. "
                "The sender continues even after you ask them to stop."
            ),
            "options": [
                {"value": "ignore", "label": "Ignore the messages"},
                {"value": "respond", "label": "Respond and ask them to stop"},
                {"value": "document", "label": "Save the messages as evidence"},
                {"value": "report", "label": "Report the behaviour to the platform"},
            ],
            "feedback": {
                "message": (
                    "When someone continues after you have asked them to stop, this behaviour may reasonably "
                    "be considered online abuse."
                ),
                "note": (
                    "Documenting behaviour can be helpful if the situation continues or escalates."
                ),
            },
        },
        {
            "text": (
                "Someone repeatedly posts mocking or hostile comments about you in the replies to a public post. "
                "The comments are visible to others and continue over time."
            ),
            "options": [
                {"value": "ignore", "label": "Ignore the comments"},
                {"value": "respond", "label": "Respond publicly"},
                {"value": "document", "label": "Take screenshots of the comments"},
                {"value": "report", "label": "Report the comments to the platform"},
            ],
            "feedback": {
                "message": (
                    "Public comments can increase emotional and reputational impact, even if they seem minor "
                    "when viewed individually."
                ),
                "note": (
                    "Saving evidence may help you decide what action to take later."
                ),
            },
        },
        {
            "text": (
                "You receive messages that imply negative consequences if you do not comply with certain requests. "
                "The tone feels intimidating, even though no direct threats are made."
            ),
            "options": [
                {"value": "ignore", "label": "Ignore the messages"},
                {"value": "respond", "label": "Ask for clarification"},
                {"value": "document", "label": "Save the messages"},
                {"value": "seek_help", "label": "Seek advice or support"},
            ],
            "feedback": {
                "message": (
                    "Intimidating or pressuring messages do not need to include explicit threats to be concerning."
                ),
                "note": (
                    "Trusting your discomfort is important when deciding how to respond."
                ),
            },
        },
        {
            "text": (
                "Someone shares your personal information or screenshots of private messages without your consent. "
                "You did not agree to this information being made public."
            ),
            "options": [
                {"value": "ignore", "label": "Do nothing"},
                {"value": "document", "label": "Save copies of what was shared"},
                {"value": "request_removal", "label": "Ask for the content to be removed"},
                {"value": "report", "label": "Report the content to the platform"},
            ],
            "feedback": {
                "message": (
                    "Sharing personal information without consent may represent a serious breach of privacy."
                ),
                "note": (
                    "Keeping records can support requests for removal or reporting."
                ),
            },
        },
        {
            "text": (
                "An individual continues to contact you across different platforms, even after you block them. "
                "New accounts or messages appear over time."
            ),
            "options": [
                {"value": "ignore", "label": "Ignore further contact"},
                {"value": "document", "label": "Keep a record of all contact"},
                {"value": "tighten_settings", "label": "Review privacy and security settings"},
                {"value": "seek_support", "label": "Seek external support"},
            ],
            "feedback": {
                "message": (
                    "Repeated unwanted contact across platforms may indicate escalation rather than isolated behaviour."
                ),
                "note": (
                    "Support organisations can help you think through next steps."
                ),
            },
        },
    ]

    step = request.session.get("scenario_step", 0)
    feedback = None

    if request.method == "POST":

        # Restart requested
        if "restart" in request.POST:
            request.session["scenario_step"] = 0
            return redirect("assessment:scenario_simulator")

        # Move to next scenario
        if "next" in request.POST:
            step += 1
            request.session["scenario_step"] = step
        else:
            feedback = scenarios[step]["feedback"]

    # Safety guard
    if step >= len(scenarios):
        request.session["scenario_step"] = len(scenarios) - 1

    return render(
        request,
        "scenario_simulator.html",
        {
            "scenario": scenarios[step],
            "step": step + 1,
            "feedback": feedback,
            "is_last": step == len(scenarios) - 1,
        },
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

def legal(request):
    return render(request, "legal.html")
