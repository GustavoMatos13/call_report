from django.db import models


class CallStart(models.Model):

    id = models.AutoField(primary_key=True)
    call_type = models.CharField(max_length=7, default='START')
    timestamp = models.DateTimeField()
    source = models.CharField(max_length=15)
    destination = models.CharField(max_length=15)
    call_id = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return (
            f"type call: {self.call_type} call code: {self.call_id}"
            f"from: {self.source} to: {self.destination} at: {self.timestamp}"
            )
