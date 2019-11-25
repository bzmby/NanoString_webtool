from django.contrib import admin
from .models import *
# Register your models here.

class FilesInline(admin.TabularInline):
    model = InputFile.files.through

class FilesAdmin(admin.ModelAdmin):
    inlines = [
        FilesInline,
    ]

class InputFileAdmin(admin.ModelAdmin):
    inlines = [
       FilesInline,
    ]
    exclude = ('files',)

class QCFilesInline(admin.TabularInline):
    model = QC.qc_files.through

class QCFilesAdmin(admin.ModelAdmin):
    inlines = [
        QCFilesInline,
    ]

class QCAdmin(admin.ModelAdmin):
    inlines = [
       QCFilesInline,
    ]
    exclude = ('qc_files',)

class GCFilesInline(admin.TabularInline):
    model = GroupComparison.gc_files.through

class GCFilesAdmin(admin.ModelAdmin):
    inlines = [
        GCFilesInline,
    ]

class GroupComparisonAdmin(admin.ModelAdmin):
    inlines = [
       GCFilesInline,
    ]
    exclude = ('gc_files',)

class VCFilesInline(admin.TabularInline):
    model = GeVolcano.vc_files.through

class VCFilesAdmin(admin.ModelAdmin):
    inlines = [
        VCFilesInline,
    ]

class GeVolcanoAdmin(admin.ModelAdmin):
    inlines = [
       VCFilesInline,
    ]
    exclude = ('vc_files',)



admin.site.register(InputFile, InputFileAdmin)
admin.site.register(QC, QCAdmin)
admin.site.register(QCFiles)
admin.site.register(Files)
admin.site.register(GCFiles)
admin.site.register(GroupComparison, GroupComparisonAdmin)
admin.site.register(GeVolcano, GeVolcanoAdmin)
