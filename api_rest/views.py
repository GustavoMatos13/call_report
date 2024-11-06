from datetime import datetime, timezone, time
from django.db import DatabaseError
from django.forms import ValidationError
import math

from api_rest.models.callStart import CallStart
from api_rest.models.callEnd import CallEnd
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from api_rest.serializers import CallEndSerializer


@api_view(['POST'])
def post_call_record(request):
    if request.method == 'POST':
        call_request = request.data
        if (
            call_request['call_id'] and
            call_request['start'] and
            call_request['end'] and
            call_request['source'] and
            call_request['destination']
        ):

            callStart = CallStart(call_id=call_request['call_id'],
                                  timestamp=call_request['start'],
                                  source=call_request['source'],
                                  destination=call_request['destination'])
            callEnd = CallEnd(timestamp=call_request['start'])
            try:
                callStart.save()
                callEnd.save()
            except DatabaseError:
                return Response({"error":
                                "'call_id' field already exists in the table"},
                                status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def get_call_record(request, source, month=None, year=None):
    try:
        if month is None or year is None:
            call_end = CallEnd.objects.filter(
                call_id__source=source
                ).order_by('-timestamp')

        if month is not None and year is not None:
            call_end = CallEnd.objects.filter(
                call_id__source=source, timestamp__year=year,
                timestamp__month=month
                )
    except ValidationError:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializerEnd = CallEndSerializer(call_end, many=True)
        if month is None or year is None:
            return Response(serializerEnd.data[0])
        else:
            telephoneBill = []
            for call in serializerEnd.data:
                try:
                    call_start = CallStart.objects.get(call_id=call['call_id'])
                except CallStart.DoesNotExist:
                    return Response(status=status.HTTP_404_NOT_FOUND)
                except CallStart.MultipleObjectsReturned:
                    return Response(status=status.HTTP_404_NOT_FOUND)

                telephoneBillObject = {}
                telephoneBillObject["destination"] = call_start.destination

                dataStart = call_start.timestamp
                telephoneBillObject["call_start_date"] = dataStart.date()
                telephoneBillObject["call_start_time"] = dataStart.time()

                telephoneBillObject["call_duration"] = calculate_duration(
                    call["timestamp"], dataStart
                    )

                telephoneBillObject["call_price"] = calculate_price(
                    call["timestamp"], dataStart
                    )
                telephoneBill.append(telephoneBillObject)

            return Response(telephoneBill)
    return Response(status=status.HTTP_400_BAD_REQUEST)


def calculate_price(dataEnd, dataStart):
    FIXED_TAXA = 0.36
    TAXA_CALL = 0.09
    HOURS_MIN = time(6, 00, 00)
    HOURS_MAX = time(22, 00, 00)
    dataEnd = datetime.strptime(dataEnd, "%Y-%m-%dT%H:%M:%SZ")
    dataEnd = dataEnd.replace(tzinfo=timezone.utc)
    hrStart = dataStart.time()
    hrEnd = dataEnd.time()
    diff = dataEnd - dataStart
    minutesStart = 0
    minutesEnd = 0

    if hrStart > HOURS_MIN and hrStart < HOURS_MAX:
        diff_seconds = time_to_seconds(HOURS_MAX) - time_to_seconds(hrStart)
        minutesStart = math.floor(diff_seconds/60)

    if hrEnd > HOURS_MIN and hrEnd < HOURS_MAX:
        diff_seconds = time_to_seconds(HOURS_MAX) - time_to_seconds(hrEnd)
        minutesEnd = math.floor(diff_seconds/60)

    minute_day = minute_day_taxa(HOURS_MIN, HOURS_MAX, diff.days)

    minuteTotal = minutesStart + minutesEnd + minute_day

    price = (minuteTotal * TAXA_CALL) + FIXED_TAXA

    return f"R$ {price:.2f}"


def minute_day_taxa(h_min, h_max, days):
    day_minute_taxa = 0
    if days > 1:
        days += -1
        diff_seconds = (86400 - (time_to_seconds(h_max)
                        - time_to_seconds(h_min)))
        convert_minutes = diff_seconds / 60
        day_minute_taxa = convert_minutes * days

    return day_minute_taxa


def time_to_seconds(t):
    return t.hour * 3600 + t.minute * 60 + (t.second / 60)


def calculate_duration(dataEnd, dataStart):
    dataEnd = datetime.strptime(dataEnd, "%Y-%m-%dT%H:%M:%SZ")
    dataEnd = dataEnd.replace(tzinfo=timezone.utc)

    difference = dataEnd - dataStart
    total_seconds = difference.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = (difference.seconds % 3600) // 60
    seconds = difference.seconds % 60
    difference_time = f'{hours}h{minutes}m{seconds}s'
    return difference_time
