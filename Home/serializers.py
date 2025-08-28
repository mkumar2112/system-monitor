from rest_framework import serializers
from .models import Computer, ProcessInfo

class ProcessInfoSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = ProcessInfo
        fields = ['pid', 'name', 'user', 'status', 'memory', 'children']

    def get_children(self, obj):
        return ProcessInfoSerializer(obj.children.all(), many=True).data

class ComputerSerializer(serializers.ModelSerializer):
    processes = ProcessInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Computer
        fields = [
            'name', 'ip_address', 'os_name', 'os_version',
            'processor_name', 'physical_cores', 'logical_cores', 'max_frequency_mhz',
            'ram_gb', 'total_storage_gb', 'used_storage_gb', 'free_storage_gb',
            'processes'
        ]
