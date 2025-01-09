#!/usr/bin/env python3
import cgi
import json
import pymysql

# Parse form data
form = cgi.FieldStorage()

# Debug: Print form field values
debug_info = {}
for field in form.keys():
    value = form.getvalue(field)
    debug_info[field] = value

# Convert 'sort_id' field to integer if possible
if 'sort_id' in debug_info:
    try:
        debug_info['sort_id'] = int(debug_info['sort_id'])
    except ValueError:
        pass  # Leave it as string if conversion fails

# Prepare JSON response
response = {}

# Check if 'sort_id' and other fields are present
if 'sort_id' in debug_info:
    # Execute the update statement
    try:
        # Connect to the database
        connection = pymysql.connect(
            host='bioed.bu.edu',
            user='astoicad',
            password='astoicad',
            db='Team_4',
            port=4253
        )

        # Update data in the database
        with connection.cursor() as cursor:
            sql = "UPDATE sort SET hatch_date = %s, sort_date = %s, line_name = %s, marker_color = %s, marker_location = %s, fl_ratio = %s, fl_total = %s, notes = %s WHERE sort_id = %s"
            cursor.execute(sql, (debug_info.get('hatch_date', None), debug_info.get('sort_date', None), debug_info.get('line_name', None), debug_info.get('marker_color', None), debug_info.get('marker_location', None), debug_info.get('fl_ratio', None), debug_info.get('fl_total', None), debug_info.get('notes', None), debug_info['sort_id']))
            connection.commit()

        # Update the response
        response["success"] = True
        response["message"] = "Data updated successfully"
    except Exception as e:
        response["success"] = False
        response["error"] = "Failed to update data: {}".format(str(e))
    finally:
        # Close the database connection
        if 'connection' in locals() and connection.open:
            connection.close()
else:
    response["success"] = False
    response["error"] = "Missing 'sort_id' field in form data"

# Output JSON response
print("Content-type: application/json\n")
print(json.dumps(response))

