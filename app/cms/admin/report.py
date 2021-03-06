from posixpath import join as urljoin

from django.contrib import admin, messages
from django.utils import timezone
from django import forms
from django.core.exceptions import ValidationError
from emoji_picker.widgets import EmojiPickerTextInputAdmin, EmojiPickerTextareaAdmin
import requests
from admin_object_actions.admin import ModelAdminObjectActionsMixin
from admin_object_actions.forms import AdminObjectActionForm
from crum import get_current_request

from ..models.report import NotificationSent, Report, ReportFragment, ReportQuiz
from .attachment import trigger_attachments
from .fragment import FragmentModelForm, FragmentAdminInline
from .quiz import QuizModelForm, QuizAdminInline
from .news_base import NewsBaseAdmin, NewsBaseModelForm
from ..env import (
    REPORT_TRIGGER_URLS,
    BOT_SERVICE_ENDPOINT_FB,
    BOT_SERVICE_ENDPOINT_TG,
)


class ReportFragmentModelForm(FragmentModelForm):
    class Meta:
        model = ReportFragment
        fields = ["question", "text", "attachment", "attachment_preview", "link_wiki"]


class ReportFragmentAdminInline(FragmentAdminInline):
    model = ReportFragment
    form = ReportFragmentModelForm
    fields = ["question", "attachment", "attachment_preview", "text"]
    extra = 1


class ReportQuizModelForm(QuizModelForm):
    class Meta:
        model = ReportQuiz
        fields = [
            "correct_option",
            "quiz_option",
            "quiz_text",
            "attachment",
            "attachment_preview",
        ]


class ReportQuizInlineFormset(forms.models.BaseInlineFormSet):
    def is_valid(self):
        return super().is_valid() and not any([bool(e) for e in self.errors])

    def clean(self):

        super().clean()

        # get forms that actually have valid data
        option_count = 0
        correct_option_count = 0

        for form in self.forms:
            try:
                if form.cleaned_data and not form.cleaned_data.get("DELETE", False):
                    option_count += 1
                    if form.cleaned_data["correct_option"]:
                        correct_option_count += 1
            except AttributeError:
                # annoyingly, if a subform is invalid Django explicity raises
                # an AttributeError for cleaned_data
                pass
        if option_count == 1:
            raise forms.ValidationError(
                "Es müssen mindestens 2 Antworten für ein Quiz existieren!"
            )
        elif option_count > 1 and correct_option_count == 0:
            raise forms.ValidationError("Es gibt keine richtige Antwort!")
        elif option_count > 1 and correct_option_count != 1:
            raise forms.ValidationError("Es gibt mehr als eine richtige Antwort!")


class ReportQuizAdminInline(QuizAdminInline):
    model = ReportQuiz
    form = ReportQuizModelForm
    formset = ReportQuizInlineFormset

    extra = 0
    max_num = 3


class ReportModelForm(NewsBaseModelForm):

    headline = forms.CharField(
        label="Überschrift", widget=EmojiPickerTextInputAdmin, max_length=50
    )

    summary = forms.CharField(
        label="Telegram-Text",
        widget=EmojiPickerTextareaAdmin,
        max_length=850,
        required=False,
    )
    text = forms.CharField(
        label="Facebook-Text",
        widget=EmojiPickerTextareaAdmin,
        max_length=550,
        required=True,
    )

    class Meta:
        model = Report
        exclude = ()

    def get_initial_for_field(self, field, field_name):
        if field_name == "subtype":
            field.widget.can_delete_related = False
            field.widget.can_add_related = False
            field.widget.can_change_related = False

        return super().get_initial_for_field(field, field_name)

    def clean(self):
        # Check for subtype setting
        if self.cleaned_data["type"] == "last" and self.cleaned_data["subtype"] is None:
            raise ValidationError(
                {
                    "subtype": 'Wenn der Meldungstyp auf "🎨 Letzte Meldung" gesetzt ist, '
                    "muss der Subtyp ausgefüllt werden.",
                }
            )
        elif (
            self.cleaned_data["type"] != "last"
            and self.cleaned_data["subtype"] is not None
        ):
            self.cleaned_data["subtype"] = None

        if self.cleaned_data["type"] == "regular" and not self.cleaned_data["summary"]:
            raise ValidationError(
                {
                    "summary": "Der Telegram-Text muss für reguläre Meldungen ausgefüllt werden!",
                }
            )
        elif self.cleaned_data["type"] != "regular":
            self.cleaned_data["summary"] = None
        
        if self.cleaned_data["published"] and self.cleaned_data["type"] == "breaking" and self.cleaned_data["attachment"] is None:
            raise ValidationError(
                {
                    "attachment": 'Wenn der Meldungstyp auf "🚨 Breaking-Content" gesetzt ist, '
                    "muss ein Medien-Anhang angegeben werden.",
                }
            )

        return self.cleaned_data


class SendNotificationForm(AdminObjectActionForm):

    fb = forms.BooleanField(
        required=False,
        help_text="""Diese Benachrichtigung in Facebook senden?""",
        label="Facebook",
    )
    tg = forms.BooleanField(
        required=False,
        help_text="""Diese Benachrichtigung in Telegram senden?""",
        label="Telegram",
    )

    morning = forms.BooleanField(
        required=False,
        help_text="""Diese Benachrichtigung an Morgen-Abonnenten senden?""",
        label="☕ Morgen",
        initial=True,
    )
    evening = forms.BooleanField(
        required=False,
        help_text="""Diese Benachrichtigung an Abend-Abonnenten senden?""",
        label="🌙 Abend",
        initial=True,
    )
    breaking = forms.BooleanField(
        required=False,
        help_text="""Diese Benachrichtigung an Breaking-Abonnenten senden?""",
        label="🚨 Breaking",
        initial=True,
    )

    class Meta:
        model = Report
        fields = ()

    def do_object_action(self):
        try:
            if self.instance.notification_sent:
                raise Exception("Diese Benachrichtigung wurde bereits versendet!")
        except NotificationSent.DoesNotExist:
            pass

        notification_sent = NotificationSent(report=self.instance)

        for field, value in self.cleaned_data.items():
            setattr(notification_sent, field, value)

        notification_sent.save()

        timings = [
            t for t in ("morning", "evening", "breaking") if self.cleaned_data[t]
        ]
        failed = []

        for service, report_trigger_url in REPORT_TRIGGER_URLS.items():
            if not self.cleaned_data[service]:
                continue

            print("Triggering", service, "with", timings)

            r = requests.post(
                url=report_trigger_url,
                json={
                    "report": self.instance.id,
                    "options": {
                        "timings": timings,
                    },
                },
            )

            if not r.ok:
                failed.append(service.upper())

        if failed:
            raise Exception(
                f'Manuelles Senden für mindestens einen Bot ist fehlgeschlagen ({", ".join(failed)})'
            )


class ReportAdmin(ModelAdminObjectActionsMixin, NewsBaseAdmin):
    form = ReportModelForm
    change_form_template = "admin/cms/change_form_report.html"
    date_hierarchy = "created"
    list_filter = ["published", "type"]
    search_fields = ["headline"]
    list_display = (
        "report_type",
        "status",
        "headline",
        "created",
        "assets",
        "send_status",
        "notification_sent",
        "display_object_actions_list",
    )
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "display_object_actions_detail",
                    "type",
                    "subtype",
                    "published",
                    "genres",
                    "tags",
                )
            },
        ),
        (
            "Telegram & Facebook",
            {
                "classes": ("extrapretty", "all"),
                "fields": (
                    "headline",
                    "short_headline",
                    "link",
                ),
            },
        ),
        (
            "Telegram",
            {
                "classes": ("extrapretty", "telegram"),
                "fields": ("summary",),
            },
        ),
        (
            "Facebook",
            {
                "classes": ("extrapretty", "facebook"),
                "fields": (
                    "attachment",
                    "attachment_preview",
                    "text",
                ),
            },
        ),
    )
    # value 'audio' is supposed to be added to fields again, once the feature is communicated
    readonly_fields = ("display_object_actions_detail",)
    list_display_links = ("headline",)
    inlines = (
        ReportFragmentAdminInline,
        ReportQuizAdminInline,
    )

    def display_object_actions_list(self, obj=None):
        return self.display_object_actions(obj, list_only=True)

    display_object_actions_list.short_description = "Aktionen"

    def display_object_actions_detail(self, obj=None):
        return self.display_object_actions(obj, detail_only=True)

    display_object_actions_detail.short_description = "Aktionen"

    object_actions = [
        {
            "slug": "preview-report",
            "verbose_name": "Testen",
            "verbose_name_past": "tested",
            "form_method": "GET",
            "function": "preview",
        },
        {
            "slug": "breaking-report",
            "verbose_name": "🚨 Breaking-Content-Push jetzt senden",
            "verbose_name_past": "als Breaking-Content-Push gesendet",
            "form_method": "GET",
            "function": "send_breaking",
            "permission": "send_breaking",
        },
        {
            "slug": "evening-push-report",
            "verbose_name": "🌙 Abend-Push jetzt senden",
            "verbose_name_past": "🌙 Abend-Push gesendet",
            "form_method": "GET",
            "function": "send_evening_push",
            "permission": "send_evening_push",
        },
        {
            "slug": "notification",
            "verbose_name": "📨 Benachrichtigung senden",
            "verbose_name_past": "📨 Benachrichtigung gesendet",
            "form_class": SendNotificationForm,
            "permission": "send_notification",
            "fieldsets": (
                ("Produkte", {"fields": ("fb", "tg")}),
                (
                    "Empfänger - Markiere alle Felder, um eine Benachrichtigung an ALLE NUTZER*INNEN zu senden",
                    {
                        "fields": ("morning", "evening", "breaking"),
                    },
                ),
            ),
        },
    ]

    def preview(self, obj, form):
        request = get_current_request()
        profile = request.user.profile

        if not profile:
            error_message = "Bitte trage deine Nutzer-ID für Facebook und/oder Telegram in deinem Profil ein."
            raise Exception(error_message)

        failed = False

        if profile.psid:
            r = requests.post(
                url=urljoin(BOT_SERVICE_ENDPOINT_FB, "report"),
                json={
                    "report": obj.id,
                    "options": {
                        "preview": profile.psid,
                    },
                },
            )

            if not r.ok:
                messages.error(request, "Testen bei Facebook ist fehlgeschlagen.")
                failed = True

        else:
            messages.warning(
                request,
                "Bitte trage deine Facebook-ID in deinem Profil ein, um in Facebook testen zu können.",
            )

        if profile.tgid:
            r = requests.post(
                url=urljoin(BOT_SERVICE_ENDPOINT_TG, "report"),
                json={
                    "report": obj.id,
                    "options": {
                        "preview": profile.tgid,
                    },
                },
            )

            if not r.ok:
                messages.error(request, "Testen bei Telegram ist fehlgeschlagen.")
                failed = True

        else:
            messages.warning(
                request,
                "Bitte trage deine Telegram-ID in deinem Profil ein, um in Telegram testen zu können.",
            )

        if failed:
            raise Exception("Es ist ein Fehler aufgetreten.")

    def has_send_breaking_permission(self, request, obj=None):
        return (
            Report.Type(obj.type) is Report.Type.BREAKING
            and obj.published
            and Report.DeliveryStatus(obj.delivered_fb)
            is Report.DeliveryStatus.NOT_SENT
            and Report.DeliveryStatus(obj.delivered_tg)
            is Report.DeliveryStatus.NOT_SENT
        )

    def send_breaking(self, obj, form):
        if not self.has_send_breaking_permission(None, obj=obj):
            raise Exception("Nicht erlaubt")

        failed = []

        for service, report_trigger_url in REPORT_TRIGGER_URLS.items():
            r = requests.post(
                url=report_trigger_url,
                json={
                    "report": obj.id,
                },
            )

            if not r.ok:
                failed.append(service.upper())

        if failed:
            raise Exception(
                f'Breaking-Content für mindestens einen Bot ist fehlgeschlagen ({", ".join(failed)})'
            )

    def has_send_evening_push_permission(self, request, obj=None):
        return (
            Report.Type(obj.type) is Report.Type.EVENING
            and obj.published
            and Report.DeliveryStatus(obj.delivered_fb)
            is Report.DeliveryStatus.NOT_SENT
            and Report.DeliveryStatus(obj.delivered_tg)
            is Report.DeliveryStatus.NOT_SENT
        )

    def send_evening_push(self, obj, form):
        if not self.has_send_evening_push_permission(None, obj=obj):
            raise Exception("Nicht erlaubt")

        failed = []
        for service, report_trigger_url in REPORT_TRIGGER_URLS.items():
            r = requests.post(
                url=report_trigger_url,
                json={
                    "report": obj.id,
                },
            )

            if not r.ok:
                failed.append(service.upper())

        if failed:
            raise Exception(
                f'Breaking-Content für mindestens einen Bot ist fehlgeschlagen ({", ".join(failed)})'
            )

    def has_send_notification_permission(self, request, obj=None):

        return (
            Report.Type(obj.type) is Report.Type.NOTIFICATION
            and obj.published
            and not getattr(obj, "notification_sent", False)
            and Report.DeliveryStatus(obj.delivered_fb)
            is Report.DeliveryStatus.NOT_SENT
            and Report.DeliveryStatus(obj.delivered_tg)
            is Report.DeliveryStatus.NOT_SENT
        )

    def report_type(self, obj):
        if Report.Type(obj.type) == Report.Type.BREAKING:
            display = "🚨"
        elif Report.Type(obj.type) == Report.Type.REGULAR:
            display = "📰"
        elif Report.Type(obj.type) == Report.Type.LAST:
            display = f"🎨{obj.subtype.emoji}"
        elif Report.Type(obj.type) == Report.Type.EVENING:
            display = "🌙"
        elif Report.Type(obj.type) == Report.Type.NOTIFICATION:
            display = "📨"
        else:
            display = "?"

        return display

    def status(self, obj):
        if not obj.published:
            display = "✏️"
        else:
            display = "✅"

        return display

    def send_status(self, obj):
        if Report.Type(obj.type) not in (
            Report.Type.BREAKING,
            Report.Type.EVENING,
            Report.Type.NOTIFICATION,
        ):
            return ""

        notification_sent = getattr(obj, "notification_sent", None)

        display = ""

        if not notification_sent or notification_sent.fb:
            if (
                Report.DeliveryStatus(obj.delivered_fb)
                == Report.DeliveryStatus.NOT_SENT
            ):
                display += "FB: ❌️"
            elif (
                Report.DeliveryStatus(obj.delivered_fb) == Report.DeliveryStatus.SENDING
            ):
                display += "FB: 💬"
            else:
                display += "FB: ✅"

        if not notification_sent or notification_sent.tg:
            if (
                Report.DeliveryStatus(obj.delivered_tg)
                == Report.DeliveryStatus.NOT_SENT
            ):
                display += "  TG: ❌"
            elif (
                Report.DeliveryStatus(obj.delivered_tg) == Report.DeliveryStatus.SENDING
            ):
                display += "  TG: 💬"
            else:
                display += "  TG: ✅"

        return display

    send_status.short_description = "Sende-Status"
    report_type.short_description = "Typ"
    status.short_description = "Status"

    def assets(self, obj):
        assets = ""
        if obj.attachment and str(obj.attachment) != "":
            assets = "🖼️"

        if obj.link and str(obj.link) != "":
            assets += "🔗️"

        if obj.audio and str(obj.audio) != "":
            assets += "🔊"

        return assets

    def save_model(self, request, obj, form, change):
        obj.modified = timezone.now()
        if obj.published and obj.published_date is None:
            obj.published_date = timezone.now()

        original = None
        if obj.pk:
            original = obj.__class__.objects.get(pk=obj.pk)

        if not obj.author:
            obj.author = request.user.get_full_name()

        if "audio" in form.changed_data and obj.audio:
            audio_url = str(obj.audio)

            filename = audio_url.split("/")[-1]
            if not (filename.lower().endswith(".mp3")):
                messages.error(
                    request,
                    f"Das Audio hat das falsche Format. Akzeptierte Formate: *.mp3",
                )
                obj.audio = None

            else:
                success = trigger_attachments(audio_url)

                if success:
                    messages.success(
                        request, f"Anhang {obj.audio} wurde zu Facebook hochgeladen 👌"
                    )

                else:
                    messages.error(
                        request,
                        f"Anhang {obj.audio} konnte nicht zu Facebook hochgeladen werden",
                    )

                    obj.audio = None

        if not obj.published and obj.type == "breaking" and obj.attachment is None:
            messages.warning(
                request,
                "Der Breaking-Content-Push hat noch keinen Medien-Anhang.",
            )

        super().save_model(request, obj, form, change)

    def response_change(self, request, obj):
        if "_publish-save" in request.POST:
            obj.published = True
            if obj.published_date is None:
                obj.published_date = timezone.now()
            obj.save()
            self.message_user(request, "Die Meldung ist freigegeben.")
        return super().response_change(request, obj)

    def get_search_results(self, request, queryset, search_term):
        """
        Custom search results function that allows the custom autocomplete field in the PushModelForm
        to filter for specific reports.
        """
        if "report_type" in request.GET:
            queryset = queryset.filter(type=request.GET["report_type"])
        return super().get_search_results(request, queryset, search_term)


# Register your models here.
admin.site.register(Report, ReportAdmin)
