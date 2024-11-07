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
        if call_request.get('_content'):
            call_request = call_request['_content']
            call_request = call_request.split(",")
            call_request_dict = {}
            call_request_dict = Response(status=status.HTTP_404_NOT_FOUND)
            for c in call_request:
                c = c.split(":")
                call_request_dict[c[0]] = c[1]
                call_request = call_request_dict

        try:
            if (
                call_request['call_id'] and
                call_request['start'] and
                call_request['end'] and
                call_request['source'] and
                call_request['destination']
            ):
                if (
                        len(call_request['source']) > 11 or
                        len(call_request['source']) < 10 or
                        len(call_request['destination']) > 11 or
                        len(call_request['destination']) < 10
                     ):
                    return Response({"error":
                                     "the telephone number must contain "
                                     "10 or 11 digits with the area code"
                                     },
                                    status=status.HTTP_400_BAD_REQUEST)

                callStart = CallStart(call_id=call_request['call_id'],
                                      timestamp=call_request['start'],
                                      source=call_request['source'],
                                      destination=call_request['destination'])

                callEnd = CallEnd(timestamp=call_request['end'],
                                  call_id=callStart
                                  )
                try:
                    callStart.save()
                    callEnd.save()
                except DatabaseError:
                    return Response({"error":
                                     "'call_id' field already"
                                     "exists in the table"
                                     },
                                    status=status.HTTP_400_BAD_REQUEST)
                return Response(status=status.HTTP_201_CREATED)
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except ValidationError:
            return Response({"error":
                             "fields are incorrect", "data": call_request
                             },
                            status=status.HTTP_400_BAD_REQUEST)
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
        try:
            serializerEnd = CallEndSerializer(call_end, many=True)
            if month is None or year is None:
                try:
                    call_start = CallStart.objects.get(
                        call_id=serializerEnd.data[0]['call_id']
                        )
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
                    serializerEnd.data[0]["timestamp"], dataStart
                    )

                telephoneBillObject["call_price"] = calculate_price(
                    serializerEnd.data[0]["timestamp"], dataStart
                    )

                return Response(telephoneBillObject)
        except DatabaseError:
            return Response(status=status.HTTP_400_BAD_REQUEST)
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
    minute_day = 0
    minuteTotal = 0

    if diff.days > 0:
        minute_day = minute_day_taxa(HOURS_MIN, HOURS_MAX, diff.days)

        if hrStart > HOURS_MIN and hrStart < HOURS_MAX:
            diff_seconds = time_seconds(HOURS_MAX)-time_seconds(hrStart)
            minutesStart = math.floor(diff_seconds/60)
            minutesStart *= TAXA_CALL

        if hrEnd > HOURS_MIN:
            diff_seconds = time_seconds(hrEnd)-time_seconds(HOURS_MIN)
            minutesEnd = math.floor(diff_seconds/60)
            if hrEnd > HOURS_MAX:
                diff_seconds = time_seconds(hrEnd)-time_seconds(HOURS_MAX)
                minutesEndTemp = math.floor(diff_seconds/60)
                minutesEnd -= minutesEndTemp
            minutesEnd *= TAXA_CALL
        minuteTotal = minutesStart + minutesEnd + minute_day
    else:
        if hrStart > HOURS_MIN and hrEnd < HOURS_MAX:
            diff_seconds = time_seconds(hrEnd)-time_seconds(hrStart)
            minuteTotal = math.floor(diff_seconds/60)
            minuteTotal *= TAXA_CALL
        elif hrEnd < HOURS_MAX and hrEnd > HOURS_MIN:
            diff_seconds = time_seconds(hrEnd)-time_seconds(HOURS_MIN)
            minuteTotal = math.floor(diff_seconds/60)
            minuteTotal *= TAXA_CALL
        elif hrStart > HOURS_MIN and hrStart < HOURS_MAX:
            diff_seconds = time_seconds(HOURS_MAX)-time_seconds(hrStart)
            minuteTotal = math.floor(diff_seconds/60)
            minuteTotal *= TAXA_CALL
        elif hrStart < HOURS_MIN and hrEnd > HOURS_MAX:
            diff_seconds = time_seconds(HOURS_MAX)-time_seconds(HOURS_MIN)
            minuteTotal = math.floor(diff_seconds/60)
            minuteTotal *= TAXA_CALL

    price = minuteTotal + FIXED_TAXA

    return f"R$ {price:.2f}"


def minute_day_taxa(h_min, h_max, days):
    day_minute_taxa = 0
    if days > 1:
        days += -1
        diff_seconds = (86400 - (time_seconds(h_max)
                        - time_seconds(h_min)))
        convert_minutes = diff_seconds / 60
        day_minute_taxa = (convert_minutes * days)

    return day_minute_taxa


def time_seconds(t):
    return t.hour * 3600 + t.minute * 60 + (t.second / 60)


def calculate_duration(dataEnd, dataStart):
    dataEnd = datetime.strptime(dataEnd, "%Y-%m-%dT%H:%M:%SZ")
    dataEnd = dataEnd.replace(tzinfo=timezone.utc)
    
    print(dataEnd)
    print(dataStart)

    difference = dataEnd - dataStart
    total_seconds = difference.total_seconds()
    hours = int(total_seconds // 3600)
    minutes = (difference.seconds % 3600) // 60
    seconds = difference.seconds % 60
    difference_time = f'{hours}h{minutes}m{seconds}s'
    return difference_time
