from distutils.util import strtobool

from cms.models.report import Report, ReportFragment

from .tags import TagSerializer
from .fragments import ModelViewSetWithFragments, ModelSerializerWithFragments, \
    ReportFragmentSerializer
from .genres import GenreSerializer


class ReportSerializer(ModelSerializerWithFragments):
    tags = TagSerializer(many=True, read_only=True)
    genres = GenreSerializer(many=True, read_only=True)
    fragment_serializer_class = ReportFragmentSerializer

    class Meta:
        model = Report
        fields = (
            'id', 'type', 'created', 'published_date', 'modified', 'is_quiz', 'genres',
            'tags', 'headline', 'summary', 'short_headline', 'audio', 'text', 'media', 'media_original',
            'media_alt', 'media_note', 'link', 'published', 'delivered_fb', 'author',
        )


class ReportViewSet(ModelViewSetWithFragments):
    """
    API endpoint that allows users to be viewed or edited.
    """
    serializer_class = ReportSerializer
    filter_fields = ('genres', 'tags')

    def get_queryset(self):
        if self.request.user and self.request.user.is_authenticated:
            return Report.objects.order_by('-created')
        else:
            return Report.objects.filter(published=True).order_by('-created')
