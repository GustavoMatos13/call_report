from django.db import models
from api_rest.models.callStart import CallStart


class CallEnd(models.Model):
    id = models.AutoField(primary_key=True)
    call_type = models.CharField(max_length=7, default='END')
    timestamp = models.DateTimeField()
    call_id = models.OneToOneField(CallStart, on_delete=models.CASCADE,
                                   to_field='call_id', unique=True)

    def __str__(self):
        return (
            f"type call: {self.call_type} call code:"
            f"{self.call_id.call_id} at: {self.timestamp}"
            )
