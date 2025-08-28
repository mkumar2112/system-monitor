from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from django.shortcuts import render
from .models import Computer, ProcessInfo
from .serializers import *

@api_view(["POST"])
def upload_system_data(request):
    """
    Receive system info and process info from a client computer.
    """
    data = request.data

    # 1. Computer info
    comp_data = data.get("computer")
    computer, _ = Computer.objects.get_or_create(
        name=comp_data["name"],
        defaults={
            "ip_address": comp_data.get("ip_address"),
            "os_name": comp_data.get("os_name"),
            "os_version": comp_data.get("os_version"),
            "processor_name": comp_data.get("processor_name"),
            "physical_cores": comp_data.get("physical_cores"),
            "logical_cores": comp_data.get("logical_cores"),
            "max_frequency_mhz": comp_data.get("max_frequency_mhz"),
            "ram_gb": comp_data.get("ram_gb"),
            "total_storage_gb": comp_data.get("total_storage_gb"),
            "used_storage_gb": comp_data.get("used_storage_gb"),
            "free_storage_gb": comp_data.get("free_storage_gb"),
        }
    )

    # Optional: clear old processes for this computer
    ProcessInfo.objects.filter(computer=computer).delete()

    # 2. Process info
    processes = data.get("processes", [])
    pid_map = {}
    for p in processes:
        proc_obj = ProcessInfo.objects.create(
            computer=computer,
            pid=p["pid"],
            name=p.get("name"),
            user=p.get("user"),
            status=p.get("status"),
            memory=p.get("memory"),
        )
        pid_map[p["pid"]] = proc_obj

    # Link parent-child
    for p in processes:
        pid = p["pid"]
        parent_pid = p.get("parent")
        if parent_pid and parent_pid in pid_map:
            child = pid_map[pid]
            child.parent = pid_map[parent_pid]
            child.save()

    return Response({"message": f"Data received for computer {computer.name}"})



class ComputerListView(generics.ListAPIView):
    queryset = Computer.objects.all()
    serializer_class = ComputerSerializer


class Home:
    def dashboard(request):
        return render(request, "page.html")