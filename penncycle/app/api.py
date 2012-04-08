def get_stats(request):
  print 'in get_stats'
  # Creating the data
  description = {"name": ("string", "Name"),
                 "salary": ("number", "Salary"),
                 "full_time": ("boolean", "Full Time Employee")}
  data = [{"name": "Mike", "salary": (10000, "$10,000"), "full_time": True},
          {"name": "Jim", "salary": (800, "$800"), "full_time": False},
          {"name": "Alice", "salary": (12500, "$12,500"), "full_time": True},
          {"name": "Bob", "salary": (7000, "$7,000"), "full_time": True}]

  # Loading it into gviz_api.DataTable
  data_table = gviz_api.DataTable(description)
  data_table.LoadData(data)

  # Creating a JavaScript code string
  # jscode = data_table.ToJSCode("jscode_data",
   #                            columns_order=("name", "salary", "full_time"),
   #                            order_by="salary")
  # Creating a JSon string
  json = data_table.ToJSon(columns_order=("name", "salary", "full_time"), order_by="salary")

  # Putting the JS code and JSon string into the template
  #jsondump = data_table.ToJSonResponse(columns_order=("name", "salary", "full_time"), order_by="salary")
  #print jsondump

  return HttpResponse(json, content_type="application/json")
