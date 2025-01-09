#!/usr/bin/env python3
import cgi
import json
import pymysql

# Connect to the database
connection = pymysql.connect(
    host='',
    user='',
    password='',
    db='',
    port=
)

# Function to get sort data for a given sort_id from the database
def get_sort_data_by_sort_id(sort_id):
    try:
        with connection.cursor() as cursor:
            # Parse sort_id as integer
            sort_id = int(sort_id)
            
            sql = "SELECT hatch_date, sort_date, line_name, marker_color, marker_location, fl_ratio, fl_total, notes FROM sort WHERE sort_id = %s"
            cursor.execute(sql, (sort_id,))
            result = cursor.fetchone()
            if result:
                return {
                    "hatch_date": result[0].isoformat(),
                    "sort_date": result[1].isoformat(),
                    "line_name": result[2],
                    "marker_color": result[3],
                    "marker_location": result[4],
                    "fl_ratio": float(result[5]),
                    "fl_total": int(result[6]),
                    "notes": result[7]
                }
            else:
                return None
    except Exception as e:
        # Handle database errors
        print("Failed to fetch data:", e)
        return None

# Main function to handle the CGI request
def main():
    # Set content type to JSON
    print("Content-type: application/json\n")
    
    # Get sort_id parameter from the query string
    form = cgi.FieldStorage()
    sort_id = form.getvalue('sort_id')
    
    # Check if sort_id is not None and can be parsed as an integer
    if sort_id is not None and sort_id.isdigit():
        # Fetch the data for the given sort_id
        sort_data = get_sort_data_by_sort_id(sort_id)
        
        # Prepare JSON response
        if sort_data:
            print(json.dumps(sort_data))
        else:
            print(json.dumps({"error": "Sort data not found for sort_id {}".format(sort_id)}))
    else:
        print(json.dumps({"error": "Invalid sort_id: {}".format(sort_id)}))

if __name__ == "__main__":
    main()

