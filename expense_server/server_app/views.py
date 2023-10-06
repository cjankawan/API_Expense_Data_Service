from django.shortcuts import render

import csv
from datetime import datetime
from django.http import JsonResponse
from rest_framework.decorators import api_view
import json

# Create your views here.
def csv_to_dicts(file_path):
    list_of_dicts = []
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            list_of_dicts.append(dict(row))
    return list_of_dicts

file_path = 'expense_CSV/expenses.csv'
data = csv_to_dicts(file_path)

def index(request):
    return render(request, 'index.html')

@api_view(['GET'])
def expense_by_type(request):
    amount_by = {}
    for i in data:
        data_type = i['expense_type']
        try:
            amount = float(i['amount'])
            if data_type in amount_by:
                amount_by[data_type].append(amount)
            else:
                amount_by[data_type] = [amount]
        except ValueError:
            pass
    total_expenses_by_type = {}
    for key, value in amount_by.items():
        total_sum = sum(value)
        total_sum = round(total_sum,2)
        total_expenses_by_type[key] = total_sum
    try:
        total_expenses_by_type['None'] = total_expenses_by_type.pop('')
    except:
        pass
    json_data = json.dumps(total_expenses_by_type)
    return JsonResponse(json_data,safe=False)

@api_view(['GET'])
def monthly_expenses(self):
    expenses_monthly = {}
    for i in data:
        try:
            date = i['expense_date']
            date = datetime.strptime(date, "%Y-%m-%d")
            month = date.month
            amount = float(i['amount'])
            if month in expenses_monthly:
                expenses_monthly[month].append(amount)
            else:
                expenses_monthly[month] = [amount]
        except:
            pass
    total_monthly = {}
    for key, value in expenses_monthly.items():
        sum_amount = sum(value)
        sum_amount = round(sum_amount, 2)
        total_monthly[key] = sum_amount
    json_data = json.dumps(total_monthly)
    return JsonResponse(json_data,safe=False)

@api_view(['GET'])
def detailed_breakdown(delf):
    expenses_type = set()
    for i in data:
        x = i['expense_type']
        expenses_type.add(x)

    breakdown_list = {}
    for x in expenses_type:
        if x == '':
            continue
        else:
            method_list = {}
            for i in data:
                expense_type = i['expense_type']
                amount = i['amount']
                payment_method = i['payment_method']
                if expense_type != x:
                    continue
                elif amount == '' or expense_type == '' or payment_method == '':
                    continue
                else:
                    amount = float(amount)
                    if payment_method in method_list:
                        method_list[payment_method].append(amount)
                    else:
                        method_list[payment_method]=[amount]
                
            sum_method_list = {}
            for key, value in method_list.items():
                sum_amount = sum(value)
                sum_amount = round(sum_amount, 2)
                sum_method_list[key] = sum_amount
                
            breakdown_list[x] = sum_method_list

    json_data = json.dumps(breakdown_list)
    return JsonResponse(json_data,safe=False)


