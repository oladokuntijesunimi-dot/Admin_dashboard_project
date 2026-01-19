from flask import Flask, render_template, jsonify, send_file, request
from flask_cors import CORS
import pandas as pd
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# --- Improvements for Portability and Accuracy ---
ATTENDANCE_FILE = "office_attendance.csv" 
DATABASE_FOLDER = "employee_database"


def get_employee_list():
    """
    Get employee names dynamically by counting subdirectories (folders)
    within the DATABASE_FOLDER.
    """
    if not os.path.exists(DATABASE_FOLDER):
        return []
    
    all_entries = os.listdir(DATABASE_FOLDER)
    
    # Filter for entries that are directories (folders)
    employees = [
        entry for entry in all_entries 
        if os.path.isdir(os.path.join(DATABASE_FOLDER, entry))
    ]
    
    return sorted(employees)


# Setting a global list is fine, but it will be overridden by calls
# inside the routes to ensure the most current data.
EMPLOYEES = get_employee_list()


# --- New robust function to read attendance data ---
def read_attendance_data():
    """
    Safely reads the attendance CSV, handling cases where the file 
    is missing, empty, or unreadable by returning a safe, empty DataFrame
    with guaranteed column names. It also handles common header variations
    and standardizes the date format.
    """
    # Define the required column structure
    safe_df = pd.DataFrame(columns=['Employee', 'Date', 'Time', 'Status'])

    if not os.path.exists(ATTENDANCE_FILE):
        return safe_df
    
    try:
        # Read the CSV, explicitly skipping blank lines (to handle trailing empty rows)
        df = pd.read_csv(ATTENDANCE_FILE, skip_blank_lines=True)

        # Handle common column name mismatch: 'Employee Name' vs 'Employee'
        if 'Employee Name' in df.columns:
            df.rename(columns={'Employee Name': 'Employee'}, inplace=True)
        
        # Check if essential columns are present after possible rename
        if 'Employee' not in df.columns or 'Date' not in df.columns:
            # If columns are missing (e.g., bad header row or empty file), return safe_df
            print(f"Warning: Attendance file '{ATTENDANCE_FILE}' exists but is missing required columns.")
            return safe_df

        # --- IMPORTANT FIX: Standardize Date Format ---
        if 'Date' in df.columns and not df.empty:
            # Convert 'Date' column to datetime objects, inferring the format (e.g., 12/2/2025)
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce', infer_datetime_format=True)
            # Format back to the desired string format (YYYY-MM-DD) for consistent comparison with `datetime.now()`
            df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')
            # Drop rows where date conversion failed (resulting in NaT)
            df.dropna(subset=['Date'], inplace=True)

        return df

    except pd.errors.EmptyDataError:
        # File exists but contains no data (is empty)
        print(f"Warning: Attendance file '{ATTENDANCE_FILE}' is empty.")
        return safe_df
    except Exception as e:
        # Catch other potential errors during file read (e.g., malformed format)
        print(f"Warning: Could not read attendance file due to an error: {e}")
        return safe_df


@app.route('/')
def home():
    return render_template('Admin_frontend.html')


@app.route('/api/stats')
def get_stats():
    try:
        # Always fetch the latest list of employees inside the route function
        employees = get_employee_list()
        
        # Use the robust reader function
        df = read_attendance_data()
        
        # This format is now consistent with the format applied in read_attendance_data()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if not df.empty:
            # These lines are now safe because df is guaranteed to have the columns or be empty
            today_attendance = df[df['Date'] == today]
            present = len(today_attendance['Employee'].unique())
        else:
            present = 0
        
        total = len(employees) # Use the fresh employee list (folder count)
        absent = total - present
        rate = (present / total * 100) if total > 0 else 0
        
        return jsonify({
            'success': True,
            'data': {
                'totalEmployees': total,
                'presentToday': present,
                'absentToday': absent,
                'attendanceRate': round(rate, 1)
            }
        })
    except Exception as e:
        # Catch unexpected errors, but the primary CSV error is now handled above
        print(f"Error in get_stats: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/attendance/today')
def get_today_attendance():
    try:
        employees = get_employee_list() 
        
        # Use the robust reader function
        df = read_attendance_data()
        
        # This format is now consistent with the format applied in read_attendance_data()
        today = datetime.now().strftime('%Y-%m-%d')
        
        if not df.empty:
            today_df = df[df['Date'] == today].drop_duplicates(
                subset=['Employee'], 
                keep='last'
            )
            records = today_df.to_dict('records')
        else:
            records = []
        
        present_names = [r['Employee'] for r in records]
        
        for emp in employees: # Use the fresh employee list
            if emp not in present_names:
                records.append({
                    'Employee': emp,
                    'Date': '-',
                    'Time': '-',
                    'Status': 'Absent'
                })
        
        return jsonify({'success': True, 'data': records})
    except Exception as e:
        print(f"Error in get_today_attendance: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500


@app.route('/api/employees')
def get_employees():
    try:
        employees = get_employee_list() 

        # Use the robust reader function
        df = read_attendance_data()
        
        today = datetime.now().strftime('%Y-%m-%d')
        
        if not df.empty:
            today_attendance = df[df['Date'] == today]
            present_list = today_attendance['Employee'].unique().tolist()
        else:
            present_list = []
        
        employee_data = []
        # Folder names are used as employee names
        for idx, emp in enumerate(employees, start=1000): 
            employee_data.append({
                'id': idx,
                'name': emp,
                'displayName': emp.replace('_', ' '),
                'status': 'Present' if emp in present_list else 'Absent'
            })
        
        return jsonify({'success': True, 'data': employee_data})
    except Exception as e:
        print(f"Error in get_employees: {e}")
        return jsonify({'success': False, 'error': str(e)}), 500

if __name__ == '__main__':
    
    startup_employees = get_employee_list()
    
    print("\n" + "=" * 60)
    print("        ATTENDANCE DASHBOARD SERVER")
    print("=" * 60)
    print("\n✅ Server starting...")
    print(f"📊 Dashboard: http://localhost:5000")
    print(f"🔌 API: http://localhost:5000/api")
    print(f"\n📁 Employees loaded (by Folder Count): {len(startup_employees)}")
    
    if len(startup_employees) > 0:
        print("   Employees:")
        for emp in startup_employees:
            print(f"   • {emp}")
    else:
        print(f"   ⚠️  WARNING: No employee folders found in '{DATABASE_FOLDER}'")
    
    print("\n🔐 Login: admin / admin123")
    print("\n" + "=" * 60 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=8090)