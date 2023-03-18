from django.contrib import admin
from django.db.models import Count

from post.models import Post, Images, Tags, Status


class TagFilter(admin.SimpleListFilter):
    title = 'Tags'
    parameter_name = 'tag'

    def lookups(self, request, model_admin):
        tags = Tags.objects.annotate(num_objects=Count('post')).filter(num_objects__gt=0)
        return [(tag.tag, tag.tag) for tag in tags]

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(tags__tag=self.value())
        return queryset


class PostImageInline(admin.TabularInline):
    model = Images
    extra = 3


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'tags_list', 'likes', 'dislikes')
    search_fields = ('title', )
    list_filter = (TagFilter,)
    inlines = [PostImageInline]

    def tags_list(self, obj):
        return ", ".join([tag.tag for tag in obj.tags.all()])

    def likes(self, obj):
        return obj.status.filter(like=True).count()

    def dislikes(self, obj):
        return obj.status.filter(dislike=True).count()


admin.site.register(Post, PostAdmin)
admin.site.register(Tags)
admin.site.register(Status)

