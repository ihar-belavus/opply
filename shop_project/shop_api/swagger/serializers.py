from rest_framework import serializers


class DefaultErrorSerializer(serializers.Serializer):
    detail = serializers.CharField()


class DefaultValueSerializerMixin:
    default_values: dict

    def get_fields(self):
        fields = super().get_fields()
        for field_name, field in fields.items():
            if default := self.default_values.get(field_name):
                default = default() if callable(default) else default
                field.default = default
        return fields


class DefaultValueSerializer(DefaultValueSerializerMixin, serializers.Serializer):
    pass


class DefaultValueModelSerializer(DefaultValueSerializerMixin, serializers.Serializer):
    pass
