from django.db import models
import os

class Files(models.Model):
    upload_file = models.FileField(upload_to='uploads/input_file/%Y/%m/%d/', null=False, blank=False)

# Create your models here.
class InputFile(models.Model):
    status_choices = (
        ("NEW", "NEW"),
        ("DONE", "DONE"),
    )
    slug = models.SlugField(max_length=50, null=False, blank=False)
    files = models.ManyToManyField('Files')
    status = models.CharField(max_length=4,
                  choices=status_choices,
                  default="NEW")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'input_file'
        verbose_name_plural = '1 - input_files'

    def delete(self, *args, **kwargs):
        for fi in self.files.all():
            os.remove(fi.upload_file.path)
        return super(InputFile, self).delete(*args, **kwargs)

class QCFiles(models.Model):
    upload_file = models.FileField(upload_to='uploads/qc/%Y/%m/%d/', null=False, blank=False)

class QC(models.Model):
    status_choices = (
        ("NEW", "NEW"),
        ("DONE", "DONE"),
    )
    input_file = models.ForeignKey(InputFile, on_delete=models.CASCADE)
    qc_files = models.ManyToManyField('QCFiles')
    quality_control = models.FileField(upload_to='uploads/qc/%Y/%m/%d/', null=False, blank=False)
    status = models.CharField(max_length=4,
                  choices=status_choices,
                  default="NEW")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.input_file.slug, self.status)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'qc'
        verbose_name_plural = '2 - qc'
    
    def delete(self, *args, **kwargs):
        for fi in self.qc_files.all():
            os.remove(fi.upload_file.path)
        os.remove(self.quality_control.path)
        return super(QC, self).delete(*args, **kwargs)

class GCFiles(models.Model):
    upload_file = models.FileField(upload_to='uploads/gc/%Y/%m/%d/', null=False, blank=False)

class GroupComparison(models.Model):
    status_choices = (
        ("NEW", "NEW"),
        ("DONE", "DONE"),
    )
    qc = models.ForeignKey(QC, on_delete=models.CASCADE)
    gc_files = models.ManyToManyField('GCFiles')
    status = models.CharField(max_length=4,
                  choices=status_choices,
                  default="NEW")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.qc.input_file.slug, self.status)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'GroupComparison'
        verbose_name_plural = '3 - GroupComparisons'

class VCFiles(models.Model):
    upload_file = models.FileField(upload_to='uploads/volcano/%Y/%m/%d/', null=False, blank=False)

class GeVolcano(models.Model):
    status_choices = (
        ("NEW", "NEW"),
        ("DONE", "DONE"),
    )
    group_comparison = models.ForeignKey(GroupComparison, on_delete=models.CASCADE)
    vc_files = models.ManyToManyField('VCFiles')
    status = models.CharField(max_length=4,
                  choices=status_choices,
                  default="NEW")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} -> {}".format(self.group_comparison.qc.input_file.slug, self.status)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'GeVolcano'
        verbose_name_plural = '4 - GeVolcanos'
