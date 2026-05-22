import logging
from django.apps import apps
from django.db import models
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

logger = logging.getLogger(__name__)

@method_decorator(csrf_exempt, name='dispatch')
class GenericAdminCRUDView(APIView):
    """
    A single robust, generic administrative API endpoint to perform CRUD 
    on any model in the system. Perfect for clean decoupled frontends.
    """
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def _serialize_object(self, obj):
        row = {}
        for field in obj._meta.fields:
            val = getattr(obj, field.name)
            if isinstance(field, (models.ImageField, models.FileField)):
                try:
                    row[field.name] = val.url if (val and val.name) else None
                except ValueError:
                    row[field.name] = None
            elif isinstance(field, models.ForeignKey) and val:
                row[field.name] = val.id
            elif isinstance(field, (models.DateField, models.DateTimeField)) and val:
                row[field.name] = val.isoformat()
            else:
                row[field.name] = val
        
        if obj._meta.model_name == 'pagesection' and hasattr(obj, 'content_items'):
            row['content_items'] = [self._serialize_object(item) for item in obj.content_items.all()]
        return row

    def post(self, request, *args, **kwargs):
        action = request.data.get('action')  # 'list', 'create', 'update', 'delete', 'fetch'
        model_label = request.data.get('model')  # e.g., 'homepage.PageSection'
        
        if not action or not model_label:
            return Response(
                {"error": "Missing action or model label parameters."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            app_label, model_name = model_label.split('.')
            model_class = apps.get_model(app_label, model_name)
        except Exception as e:
            return Response(
                {"error": f"Invalid model label: {model_label}. Error: {str(e)}"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        # 1. LIST ACTION
        if action == 'list':
            queryset = model_class.objects.all()
            
            # Apply optional filters
            filters = {}
            for key, val in request.data.items():
                if key.startswith('filter_'):
                    field_name = key.replace('filter_', '')
                    filters[field_name] = val
            if filters:
                queryset = queryset.filter(**filters)

            if hasattr(model_class, 'order'):
                queryset = queryset.order_by('order')
            elif hasattr(model_class, 'created_at'):
                queryset = queryset.order_by('-created_at')
            elif hasattr(model_class, 'id'):
                queryset = queryset.order_by('id')

            data = [self._serialize_object(obj) for obj in queryset]
            return Response(data, status=status.HTTP_200_OK)

        # 2. FETCH ACTION
        if action == 'fetch':
            obj_id = request.data.get('id')
            if not obj_id:
                return Response({"error": "Missing object ID for fetch."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                obj = model_class.objects.get(id=obj_id)
                return Response(self._serialize_object(obj), status=status.HTTP_200_OK)
            except model_class.DoesNotExist:
                return Response({"error": "Object not found."}, status=status.HTTP_444_NOT_FOUND)

        # 3. DELETE ACTION
        if action == 'delete':
            obj_id = request.data.get('id')
            if not obj_id:
                return Response({"error": "Missing object ID for deletion."}, status=status.HTTP_400_BAD_REQUEST)
            try:
                obj = model_class.objects.get(id=obj_id)
                obj.delete()
                return Response({"success": True, "message": "Deleted successfully."}, status=status.HTTP_200_OK)
            except model_class.DoesNotExist:
                return Response({"error": "Object not found."}, status=status.HTTP_444_NOT_FOUND)

        # 4. CREATE OR UPDATE ACTION
        if action in ['create', 'update']:
            obj_id = request.data.get('id')
            instance = None
            
            if action == 'update':
                if not obj_id:
                    return Response({"error": "Missing object ID for update."}, status=status.HTTP_400_BAD_REQUEST)
                try:
                    instance = model_class.objects.get(id=obj_id)
                except model_class.DoesNotExist:
                    return Response({"error": f"Object with ID {obj_id} not found."}, status=status.HTTP_444_NOT_FOUND)
            else:
                instance = model_class()

            # Iterate over fields to populate from request
            for field in model_class._meta.fields:
                if field.name in ['id', 'created_at', 'updated_at']:
                    continue

                # Handle files
                if isinstance(field, (models.ImageField, models.FileField)):
                    if field.name in request.FILES:
                        setattr(instance, field.name, request.FILES[field.name])
                    elif request.data.get(f'remove_{field.name}') == 'true':
                        file_attr = getattr(instance, field.name)
                        if file_attr:
                            file_attr.delete(save=False)
                        setattr(instance, field.name, None)
                    continue

                # Handle foreign key fields
                if isinstance(field, models.ForeignKey):
                    fk_id = request.data.get(field.name)
                    if fk_id:
                        try:
                            related_model = field.remote_field.model
                            related_instance = related_model.objects.get(id=fk_id)
                            setattr(instance, field.name, related_instance)
                        except related_model.DoesNotExist:
                            return Response(
                                {"error": f"Related object {field.name} with ID {fk_id} not found."},
                                status=status.HTTP_400_BAD_REQUEST
                            )
                    elif field.null:
                        setattr(instance, field.name, None)
                    continue

                # Handle boolean fields
                if isinstance(field, models.BooleanField):
                    val = request.data.get(field.name)
                    if val is not None:
                        is_true = str(val).lower() in ['true', '1', 'yes', 'on']
                        setattr(instance, field.name, is_true)
                    continue

                # Handle regular fields
                if field.name in request.data:
                    val = request.data.get(field.name)
                    if val == '' and field.null:
                        val = None
                    setattr(instance, field.name, val)

            try:
                instance.save()
                return Response(self._serialize_object(instance), status=status.HTTP_200_OK)
            except Exception as e:
                return Response(
                    {"error": f"Failed to save record: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({"error": f"Invalid action: {action}"}, status=status.HTTP_400_BAD_REQUEST)
