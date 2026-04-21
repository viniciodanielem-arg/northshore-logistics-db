import re
from datetime import datetime
from database.db import get_connection


ALLOWED_SHIPMENT_STATUSES = {
    "In Transit",
    "Delivered",
    "Delayed",
    "Returned to Warehouse",
    "Failed Delivery"
}

ALLOWED_PAYMENT_STATUSES = {
    "Pending",
    "Partially Paid",
    "Paid",
    "Overdue",
    "Cancelled"
}

ALLOWED_ASSIGNMENT_STATUSES = {
    "Scheduled",
    "Dispatched",
    "In Progress",
    "Completed",
    "Cancelled"
}

ALLOWED_INCIDENT_STATUSES = {
    "Open",
    "Investigating",
    "Resolved",
    "Closed"
}

ALLOWED_VEHICLE_STATUSES = {
    "Available",
    "In Use",
    "Under Maintenance",
    "Out of Service"
}


def validate_required(value, field_name):
    if value is None or not str(value).strip():
        raise ValueError(f"{field_name} is required.")


def validate_positive_number(value, field_name, allow_zero=False):
    try:
        number = float(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid number.")

    if allow_zero:
        if number < 0:
            raise ValueError(f"{field_name} cannot be negative.")
    else:
        if number <= 0:
            raise ValueError(f"{field_name} must be greater than 0.")

    return number


def validate_integer(value, field_name, allow_zero=False):
    try:
        number = int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{field_name} must be a valid whole number.")

    if allow_zero:
        if number < 0:
            raise ValueError(f"{field_name} cannot be negative.")
    else:
        if number <= 0:
            raise ValueError(f"{field_name} must be greater than 0.")

    return number


def validate_date(date_text, field_name, allow_blank=False):
    if allow_blank and (date_text is None or not str(date_text).strip()):
        return

    validate_required(date_text, field_name)

    try:
        datetime.strptime(date_text, "%Y-%m-%d")
    except ValueError:
        raise ValueError(f"{field_name} must be in YYYY-MM-DD format.")


def validate_email(email, field_name="Email", allow_blank=True):
    if allow_blank and (email is None or not str(email).strip()):
        return

    validate_required(email, field_name)

    pattern = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
    if not re.match(pattern, email):
        raise ValueError(f"{field_name} is not valid.")


def validate_phone(phone, field_name="Phone", allow_blank=True):
    if allow_blank and (phone is None or not str(phone).strip()):
        return

    validate_required(phone, field_name)

    pattern = r"^[0-9+\-\s()]{7,20}$"
    if not re.match(pattern, phone):
        raise ValueError(f"{field_name} is not valid.")


def validate_choice(value, field_name, allowed_values):
    validate_required(value, field_name)
    if value not in allowed_values:
        allowed_list = ", ".join(sorted(allowed_values))
        raise ValueError(f"{field_name} must be one of: {allowed_list}.")


def validate_text_length(value, field_name, max_length):
    if value is None:
        return
    if len(str(value)) > max_length:
        raise ValueError(f"{field_name} must be at most {max_length} characters long.")


def record_exists(table_name, id_field, record_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT 1 FROM {table_name} WHERE {id_field} = ?"
    cursor.execute(query, (record_id,))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists


def validate_record_exists(table_name, id_field, record_id, field_name):
    if not record_exists(table_name, id_field, record_id):
        raise ValueError(f"{field_name} {record_id} does not exist.")

def validate_time(time_text, field_name, allow_blank=True):
    if allow_blank and (time_text is None or not str(time_text).strip()):
        return

    validate_required(time_text, field_name)

    try:
        datetime.strptime(time_text, "%H:%M")
    except ValueError:
        raise ValueError(f"{field_name} must be in HH:MM format.")