from rest_framework import renderers, views
from rest_framework.request import Request
from rest_framework.response import Response

from packages.modules import npm
from packages.serializers import PackageSerializer


# idea: Add docstrings to classes and methods
class PackageView(views.APIView):
    renderer_classes = [renderers.JSONRenderer]

    # idea: Why does this method take the `request` if it's not used?
    # review: you don't need to default to None for a string
    def get(self, request: Request, package_name: str, range: str | None = None):  # review: Rename range (reserved keyword) and use Optional[str]
        # review: you should also check for empty string here
        if range is None:
            range = "*"

        # review: add exception handling / logging
        package_info = npm.get_package(package_name, range)
        serializer = PackageSerializer(package_info)
        return Response(serializer.data)
