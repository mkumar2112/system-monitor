from django.db import models

class Computer(models.Model):
    name = models.CharField(max_length=200, unique=True) 
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    os_name = models.CharField(max_length=200, null=True, blank=True)
    os_version = models.CharField(max_length=200, null=True, blank=True)
    processor_name = models.CharField(max_length=200, null=True, blank=True)
    physical_cores = models.IntegerField(null=True, blank=True)
    logical_cores = models.IntegerField(null=True, blank=True)
    max_frequency_mhz = models.FloatField(null=True, blank=True)
    ram_gb = models.FloatField(null=True, blank=True)
    total_storage_gb = models.FloatField(null=True, blank=True)
    used_storage_gb = models.FloatField(null=True, blank=True)
    free_storage_gb = models.FloatField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.ip_address})"
    
class ProcessInfo(models.Model):
    computer = models.ForeignKey(Computer, on_delete=models.CASCADE, related_name="processes")
    pid = models.IntegerField()
    name = models.CharField(max_length=200, null=True, blank=True)
    user = models.CharField(max_length=200, null=True, blank=True)
    status = models.CharField(max_length=100, null=True, blank=True)
    memory = models.FloatField(null=True, blank=True)  # MB
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, null=True, blank=True, related_name="children"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.pid} - {self.name}"
